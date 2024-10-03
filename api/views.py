import json
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.db import transaction

from highlightme.enums.creation_status import CreationStatus
from highlightme.settings import ENVIRONMENT
from .highlight_factory import create_highlights
from .highlights.rankings import display_player_parses, calculate_best_parse_averages
from .services.report_analyser_service import analyze_report
from .utils.data_fetcher import fetch_global_info, fetch_events

from api.models import HighlightDetails, Highlight, CREATION_STATUS, IndividualHighlight
from .utils.MOCK_data_loader import load_mock_data
from .utils.debug_encoding import inspect_data
from .utils.difficulties import DIFFICULTY_MAP
from .utils.log_highlight_creation import log_creation
from .utils.logger_console import print_start_message

logger = logging.getLogger('highlightme')

# Set up the API URL
api_url = 'https://www.warcraftlogs.com/api/v2'

# Set up the headers for the API request
headers = {
    'Authorization': 'Bearer ' + settings.WARCRAFTLOGS_OAUTH.get('access_token', ''),
    'Content-Type': 'application/json',
}

print("Settings Warcraftlogs_oauth :", settings.WARCRAFTLOGS_OAUTH.get('access_token', ''))

@csrf_exempt
@transaction.atomic
def index(request):
    print_start_message("HIGHLIGHT PROCESS : START")
    print(ENVIRONMENT)
    try:
        request_data = json.loads(request.body.decode('utf-8'))
        warcraftlogcode = request_data.get('wl_report_code')
        discord_pseudo = request_data.get('discord_pseudo')

        if not warcraftlogcode:
            logger.error('warcraftlogcode is required but not provided')
            return JsonResponse({'error': 'warcraftlogcode is required'}, status=400)

        # Fetch global info
        if settings.DEBUG:
            global_info_data = load_mock_data(f"{warcraftlogcode}/mock_global_info.json")
            print("DEBUG MODE : Reading mock_global_info.json")
        else:
            global_info_data = fetch_global_info(warcraftlogcode, headers)

        # Extract combat durations and fights
        fights = global_info_data['data']['reportData']['report']['fightsEncounters']
        report_owner = global_info_data['data']['reportData']['report']['owner']
        guild_name = global_info_data['data']['reportData']['report']['guild']
        realm = global_info_data['data']['reportData']['report']['region']['name']
        zone_name = global_info_data['data']['reportData']['report']['zone']['name']

        # Analyze report and get fights grouped by difficulty
        grouped_fights = analyze_report(fights)

        # Fetch and process all highlights
        all_highlights, lowest_difficulty = process_all_difficulties(warcraftlogcode, grouped_fights, global_info_data, report_owner, guild_name, realm, zone_name, discord_pseudo)

        return JsonResponse({'status': 'success',
                             'highlights': all_highlights,
                             'lowest_difficulty': lowest_difficulty,
                             })

    except json.JSONDecodeError as json_err:
        logger.error(f'Invalid JSON received in request body: {json_err}')
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        logger.error(f'Unexpected error: {e}')
        return JsonResponse({'error': str(e)}, status=500)


def process_all_difficulties(warcraftlogcode, grouped_fights, global_info_data, report_owner, guild_name, realm, zone_name, discord_pseudo):
    all_highlights = {}
    lowest_difficulty = None

    for difficulty_name, difficulty_fights in grouped_fights.items():
        try:
            if settings.DEBUG:
                events_data = load_mock_data(f"{warcraftlogcode}/mock_events.json")
                print(f"DEBUG MODE : mock_events.json stored in events_data for {difficulty_name}")
            else:
                difficulty = next(iter(difficulty_fights), {}).get('difficulty', None)
                print(difficulty)
                if difficulty is None:
                    logger.error(f"Could not determine difficulty for fights: {difficulty_fights}")
                    raise ValueError('Difficulty not found for fights')
                else:
                    if lowest_difficulty is None or difficulty < lowest_difficulty:
                        lowest_difficulty = difficulty

                events_data = fetch_events(warcraftlogcode, headers, difficulty_fights, difficulty)

            highlights = process_highlights_for_difficulty(events_data, global_info_data, difficulty_name, warcraftlogcode, difficulty, report_owner, guild_name, realm, zone_name, discord_pseudo)

            # Append to all_highlights to keep track of all processed highlights
            all_highlights[difficulty_name] = highlights

        except Exception as e:
            logger.error(f'Error processing highlights for difficulty {difficulty_name}: {e}')
            raise  # Propagate the exception to trigger rollback

    return all_highlights, lowest_difficulty


def process_highlights_for_difficulty(events_data, global_info_data, difficulty_name, warcraftlogcode, difficulty, report_owner, guild_name, realm, zone_name, discord_pseudo):
    # Extract boss names from the response for the current difficulty
    boss_names = {}
    for key, value in events_data['data'].items():
        if key.startswith("encounter_"):
            encounter_data = value.get('encounter', {})
            encounter_id = encounter_data.get('id')
            boss_name = encounter_data.get('name', 'Unknown Boss')
            boss_names[encounter_id] = boss_name
    print(f"Boss names for {difficulty_name}: {boss_names}")

    # Calculate parses and highlights
    best_dps_player, best_hps_player, legendary_parses, fight_highlights = calculate_best_parse_averages(events_data, boss_names)

    # Prepare player stats for saving to the database
    player_stats = {}
    for parse in legendary_parses:
        player_name = parse['name']
        rank_percent = parse['rank_percent']

        if player_name not in player_stats:
            player_stats[player_name] = {
                'total_legendary_parses': 0,
                'best_legendary_parse': 0
            }

        # Update the stats
        player_stats[player_name]['total_legendary_parses'] += 1
        player_stats[player_name]['best_legendary_parse'] = max(player_stats[player_name]['best_legendary_parse'], rank_percent)

    # Convert difficulty_name to its corresponding integer value
    difficulty_id = {v: k for k, v in DIFFICULTY_MAP.items()}.get(difficulty_name, None)

    # Save individual highlights to the database
    save_individual_highlights(warcraftlogcode, player_stats, difficulty_id)
    display_player_parses(events_data)

    # Create highlights for the current difficulty
    highlights = create_highlights(events_data, global_info_data, difficulty_name)

    # Save highlights to the database for each difficulty
    for highlight_type, details in highlights.items():
        try:
            if isinstance(details, list):
                for detail in details:
                    HighlightDetails.objects.create(
                        report_id=warcraftlogcode,
                        type_id=Highlight.objects.get(name=highlight_type).id,
                        fight_id=detail['fight_id'],
                        player_name=detail['player'],
                        player_class=detail['player_class'],
                        title=f"{highlight_type.replace('_', ' ').title()}",
                        description=detail['description'],
                        img=detail['img'],
                        difficulty=difficulty_id,
                        zone_name=zone_name,
                        highlight_value=details['highlight_value']
                    )
                    log_creation(discord_pseudo, report_owner, realm, highlight_type, guild_name, CreationStatus.CREATED.value)
            else:
                HighlightDetails.objects.create(
                    report_id=warcraftlogcode,
                    type_id=Highlight.objects.get(name=highlight_type).id,
                    player_name=details['player'],
                    player_class=details['player_class'],
                    title=f"{highlight_type.replace('_', ' ').title()}",
                    description=details['description'],
                    img=details['img'],
                    difficulty=difficulty_id,
                    zone_name=zone_name,
                    highlight_value=details['highlight_value']
                )
                log_creation(discord_pseudo, report_owner, realm, highlight_type, guild_name, CREATION_STATUS.CREATED.value)
        except Exception as e:
            logger.error(f'Error saving highlight to database: {e}')
            log_creation(discord_pseudo, report_owner, realm, highlight_type, guild_name, CREATION_STATUS.FAILED.value)
            raise  # Propagate the exception to trigger rollback

    return highlights


def save_individual_highlights(report_id, player_stats, difficulty_id):
    """
    Save the legendary parses information to the database for each player.
    """
    for player_name, stats in player_stats.items():
        if stats['total_legendary_parses'] > 0:
            # Create or update the individual highlight record
            highlight, created = IndividualHighlight.objects.update_or_create(
                report_id=report_id,
                player_name=player_name,
                difficulty=difficulty_id,
                defaults={
                    'total_legendary_parses': stats['total_legendary_parses'],
                    'best_legendary_parse': stats['best_legendary_parse']
                }
            )
            if created:
                print(f"Created new highlight for player {player_name}")
            else:
                print(f"Updated highlight for player {player_name}")
