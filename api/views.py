import json
import logging

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from highlightme.enums.creation_status import CreationStatus
from .highlight_factory import create_highlights
from .utils.data_fetcher import fetch_global_info, fetch_events

from api.models import HighlightDetails, Highlight
from .utils.MOCK_data_loader import load_mock_data
from .utils.log_highlight_creation import log_creation

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
        request_data = json.loads(request.body)
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

        # Extract combat durations
        fights = global_info_data['data']['reportData']['report']['fightsEncounters']
        report_owner = global_info_data['data']['reportData']['report']['owner']
        guild_name = global_info_data['data']['reportData']['report']['guild']
        realm = global_info_data['data']['reportData']['report']['region']['name']
        print(fights)
        combat_durations = [{"encounterID": fight['encounterID'], "fightID": fight['id'], "startTime": fight['startTime'], "endTime": fight['endTime']} for fight in fights]

        # Fetch events data
        try:
            if settings.DEBUG:
                events_data = load_mock_data(f"{warcraftlogcode}/mock_events.json")
                print("DEBUG MODE : mock_events.json stored in events_data")
            else:
                events_data = fetch_events(warcraftlogcode, headers, combat_durations)
        except Exception as e:
            logger.error(f'Error fetching events data: {e}')
            return JsonResponse({'error': f'Error fetching events data: {str(e)}'}, status=500)
        print(events_data)

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
                else:
                    HighlightDetails.objects.create(
                        report_id=warcraftlogcode,
                        type_id=Highlight.objects.get(name=highlight_type).id,
                        player_name=details['player'],
                        title=f"{highlight_type.replace('_', ' ').title()}",
                        description=details['description'],
                        img=details['img']
                    )
                    log_creation(discord_pseudo, report_owner, realm, highlight_type, guild_name, CreationStatus.CREATED.value)
            except Exception as e:
                logger.error(f'Error saving highlight to database: {e}')
            return JsonResponse({'error': f'Error saving highlight: {str(e)}'}, status=500)
        return JsonResponse(highlights)

    except json.JSONDecodeError as json_err:
        logger.error(f'Invalid JSON received in request body: {json_err}')
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        logger.error(f'Unexpected error: {e}')
        return JsonResponse({'error': str(e)}, status=500)







