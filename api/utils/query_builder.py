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

    def add_fight(self, start_time, end_time, fight_id, difficulty):
        self.alias_count += 1
        alias = f"event_{self.alias_count}"  # Generate unique aliases
        query_fragment = f'''
            {alias}: events(dataType: DamageDone, startTime: {float(start_time)}, endTime: {float(end_time)}, limit: 50, difficulty : {difficulty})
                {{
                    data
                }}
            playerDetails_{fight_id}: playerDetails(startTime: {float(start_time)}, endTime: {float(end_time)}, fightIDs: [{fight_id}])
        '''
        self.query_fragments.append(query_fragment)

    def add_encounter(self, encounter_id, difficulty):
        # Create a unique alias using the encounter ID and difficulty
        alias = f"encounter_{encounter_id}_diff_{difficulty}"
        query_fragment = f'''
            {alias}: worldData {{
                encounter(id: {encounter_id}) {{
                    id
                    name
                    zone {{
                        name
                        expansion {{
                            name
                        }}
                    }}
                }}
            }}
        '''
        self.encounter_fragments.append(query_fragment)

    def build_query(self, difficulty, fightIDs):
        full_query = f'''
        {{
            reportData {{
                report(code: "{self.warcraftlogcode}") {{
                    table(fightIDs: {fightIDs}, killType: All, difficulty: {difficulty})
                    {"".join(self.query_fragments)}
                    deathEvents: events(killType: Kills, startTime: 0, endTime: 999999999, dataType: Deaths, difficulty: {difficulty}) {{
                        data
                    }}
                    dpsRankings: rankings(playerMetric: dps, difficulty: {difficulty})
                    hpsRankings: rankings(playerMetric: hps, difficulty: {difficulty})
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
