import json
import logging
import sys

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from highlightme.enums.creation_status import CreationStatus
from .highlight_factory import create_highlights
from .highlights.rankings import display_player_parses, calculate_best_parse_averages
from .utils.data_fetcher import fetch_global_info, fetch_events

from api.models import HighlightDetails, Highlight, CREATION_STATUS, IndividualHighlight
from .utils.MOCK_data_loader import load_mock_data
from .utils.debug_encoding import inspect_data
from .utils.log_highlight_creation import log_creation
from .utils.query_builder import QueryBuilder

logger = logging.getLogger('highlightme')

# Set up the API URL
api_url = 'https://www.warcraftlogs.com/api/v2'

# Set up the headers for the API request
headers = {
    'Authorization': 'Bearer ' + settings.WARCRAFTLOGS_OAUTH.get('access_token', ''),
    'Content-Type': 'application/json',
}

print("Settings Warcraftlogs_oauth :", settings.WARCRAFTLOGS_OAUTH.get('access_token', ''))

# code = input(("Enter report code: ")) # Example of code : n6rqwa7ZHjWvY84K


@csrf_exempt
def index(request):
    print("Index called")
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

        # print(json.dumps(global_info_data, ensure_ascii=False, indent=2))

        # Extract combat durations
        fights = global_info_data['data']['reportData']['report']['fightsEncounters']
        report_owner = global_info_data['data']['reportData']['report']['owner']
        guild_name = global_info_data['data']['reportData']['report']['guild']
        realm = global_info_data['data']['reportData']['report']['region']['name']
        combat_durations = [{
            "encounterID": fight['encounterID'],
            "fightID": fight['id'],
            "startTime": fight['startTime'],
            "endTime": fight['endTime']
        } for fight in fights]

        # Fetch events data
        try:
            if settings.DEBUG:
                events_data = load_mock_data(f"{warcraftlogcode}/mock_events.json")
                print("DEBUG MODE : mock_events.json stored in events_data")
            else:
                events_data = fetch_events(warcraftlogcode, headers, combat_durations)

            # Extract boss names from the response
            boss_names = {}
            for key, value in events_data['data'].items():
                if key.startswith("encounter_"):
                    encounter_data = value.get('encounter', {})
                    encounter_id = encounter_data.get('id')
                    boss_name = encounter_data.get('name', 'Unknown Boss')
                    boss_names[encounter_id] = boss_name
            print(boss_names)

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

            # Save individual highlights to the database
            save_individual_highlights(warcraftlogcode, player_stats)
            display_player_parses(events_data)
        except Exception as e:
            logger.error(f'Error fetching events data: {e}')
            return JsonResponse({'error': f'Error fetching events data: {str(e)}'}, status=500)

        # Inspect player names for encoding issues
        players = [player['name'] for player in events_data.get('players', [])]
        inspect_data(players)

        # print(events_data)
        # Create highlights
        highlights = create_highlights(events_data, global_info_data)

        # TODO: Revert DB transaction when error
        # Save highlights to the database
        for highlight_type, details in highlights.items():
            try:
                if isinstance(details, list):
                    for detail in details:
                        HighlightDetails.objects.create(
                            report_id=warcraftlogcode,
                            type_id=Highlight.objects.get(name=highlight_type).id,
                            fight_id=detail['fight_id'],
                            player_name=detail['player'],
                            title=f"{highlight_type.replace('_', ' ').title()}",
                            description=detail['description'],
                            img=detail['img']
                        )
                        log_creation(discord_pseudo, report_owner, realm, highlight_type, guild_name, CreationStatus.CREATED.value)
                else:
                    HighlightDetails.objects.create(
                        report_id=warcraftlogcode,
                        type_id=Highlight.objects.get(name=highlight_type).id,
                        player_name=details['player'],
                        title=f"{highlight_type.replace('_', ' ').title()}",
                        description=details['description'],
                        img=details['img']
                    )
                    log_creation(discord_pseudo, report_owner, realm, highlight_type, guild_name, CREATION_STATUS.CREATED.value)
            except Exception as e:
                logger.error(f'Error saving highlight to database: {e}')
                log_creation(discord_pseudo, report_owner, realm, highlight_type, guild_name, CREATION_STATUS.FAILED.value)
                return JsonResponse({'error': f'Error saving highlight: {str(e)}'}, status=500)
        return JsonResponse(highlights)

    except json.JSONDecodeError as json_err:
        logger.error(f'Invalid JSON received in request body: {json_err}')
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        logger.error(f'Unexpected error: {e}')
        return JsonResponse({'error': str(e)}, status=500)


def save_individual_highlights(report_id, player_stats):
    """
    Save the legendary parses information to the database for each player.
    """
    for player_name, stats in player_stats.items():
        if stats['total_legendary_parses'] > 0:
            # Create or update the individual highlight record
            highlight, created = IndividualHighlight.objects.update_or_create(
                report_id=report_id,
                player_name=player_name,
                defaults={
                    'total_legendary_parses': stats['total_legendary_parses'],
                    'best_legendary_parse': stats['best_legendary_parse']
                }
            )
            if created:
                print(f"Created new highlight for player {player_name}")
            else:
                print(f"Updated highlight for player {player_name}")




