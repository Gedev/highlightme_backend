# api/utils/data_fetcher.py
import json
import logging

import requests

from highlightme import settings
from .MOCK_data_loader import load_mock_data
from .query_builder import QueryBuilder

API_URL = 'https://www.warcraftlogs.com/api/v2'

logger = logging.getLogger('highlightme')


# FETCH all the required data (PREREQUISITES) to create the SECOND QUERY to the API
def fetch_global_info(warcraftlogcode, headers):
    query = f'''
    {{
        reportData {{
            report(code: "{warcraftlogcode}") {{
                code
                title
                guild {{
                    name
                }}
                owner {{
                    name
                }}
                region {{
                    name
                }}
                fightsEncounters : fights(killType: Kills) {{
                    encounterID
                    id
                    startTime
                    endTime
                    difficulty
                    friendlyPlayers
                    gameZone {{
                        name
                    }}
                }}
                zone {{
                    name
                }}
                rankedCharacters {{
                    guilds {{
                        name
                    }}
                name
                id
                }}
            }}
        }}
    }}
    '''
    # print("Query global info : ", query)
    # RESPONSE
    response = requests.post(API_URL, headers=headers, json={'query': query})
    response.encoding = 'utf-8'
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error fetching global info: {response.status_code} - {response.text}")


def fetch_events(warcraftlogcode, headers, fights, raid_difficulty):
    # DEVELOPEMENT MODE
    if settings.DEBUG:
        return load_mock_data('mock_events.json')

    query_builder = QueryBuilder(warcraftlogcode, headers['Authorization'].split(' ')[1])

    fight_ids = []

    for fight in fights:
        start_time = fight['startTime']
        end_time = fight['endTime']
        fight_id = fight['id']
        encounter_id = fight['encounterID']
        difficulty = fight['difficulty']

        # Ajouter l'ID du combat à la liste
        fight_ids.append(fight_id)

        query_builder.add_fight(start_time, end_time, fight_id, raid_difficulty)
        query_builder.add_encounter(encounter_id, difficulty)

    graphql_query = query_builder.build_query(raid_difficulty, fight_ids)

    # RESPONSE
    response = requests.post(API_URL, headers=headers, json={'query': graphql_query})
    response.encoding = 'utf-8'
    if response.status_code == 200:
        try:
            data = response.json()
            if 'errors' in data:
                logger.error(f"GraphQL errors: {data['errors']}")
                raise Exception(f"GraphQL errors: {data['errors']}")
            return data
        except json.JSONDecodeError as json_err:
            logger.error(f"JSONDecodeError: {json_err} - Response: {response.text}")
            raise
    else:
        logger.error(f"Error fetching events: {response.status_code} - {response.text}")
        raise Exception(f"Error fetching events: {response.status_code} - {response.text}")
