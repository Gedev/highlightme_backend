# myapp/utils/query_builder.py
import logging
import requests

logger = logging.getLogger('highlightme')

class QueryBuilder:
    def __init__(self, warcraftlogcode, access_token):
        self.warcraftlogcode = warcraftlogcode
        self.access_token = access_token
        self.query_fragments = []
        self.alias_count = 0  # Count to generate unique aliases "event"
        self.encounter_fragments = []  # To store encounter name queries

    def add_fight(self, start_time, end_time, fight_id):
        self.alias_count += 1
        alias = f"event_{self.alias_count}"  # Generate unique aliases
        query_fragment = f'''
            {alias}: events(dataType: DamageDone, startTime: {float(start_time)}, endTime: {float(end_time)}, limit: 50)
                {{
                    data
                }}
            playerDetails_{fight_id}: playerDetails(startTime: {float(start_time)}, endTime: {float(end_time)}, fightIDs: [{fight_id}])
        '''
        self.query_fragments.append(query_fragment)

    def add_encounter(self, encounter_id):
        """
        Adds a GraphQL query fragment for fetching the name of a boss using its encounter ID.
        """
        encounter_query_fragment = f'''
        encounter_{encounter_id}: worldData {{
            encounter(id: {encounter_id}) {{
                id
                name
            }}
        }}
        '''
        self.encounter_fragments.append(encounter_query_fragment)

    def build_query(self):
        full_query = f'''
        {{
            reportData {{
                report(code: "{self.warcraftlogcode}") {{
                    table(startTime: 0, endTime: 999999999, killType: All)
                    {"".join(self.query_fragments)}
                    deathEvents: events(killType: Kills, startTime: 0, endTime: 999999999, dataType: Deaths) {{
                        data
                    }}
                    dpsRankings: rankings(playerMetric: dps)
                    hpsRankings: rankings(playerMetric: hps)
                }}
            }}
            {"".join(self.encounter_fragments)}
        }}
        '''
        logger.debug(f"Generated GraphQL query: {full_query}")
        print(full_query)
        return full_query

    def fetch_data(self):
        url = 'https://www.warcraftlogs.com/api/v2'
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        }
        query = self.build_query()
        response = requests.post(url, json={'query': query}, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Query failed with status code {response.status_code}: {response.text}")
