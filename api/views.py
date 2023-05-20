import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import requests

report_id = 'FR4pHbB8XktYqGzZ'
api_key = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI5OGEzYWZjMy1kZWUyLTQ5MDktOGY0Yy1lZmQ3ODdhZGVhNjEiLCJqdGkiOiJhNTcxZjU5ZWRjZGNhZDA1MDM1ZmY1NDc3NmVlOTE4MWNhZjJkMDlhNjg1MGE2NDVjZTc3NTBiOTdjZWZkMzc4ODM5MTRiZWJlNzhjMmM1NiIsImlhdCI6MTY3ODI4OTU0OC4xMjM1NiwibmJmIjoxNjc4Mjg5NTQ4LjEyMzU2MywiZXhwIjoxNzA5MzkzNTQ4LjExNzM3OCwic3ViIjoiIiwic2NvcGVzIjpbInZpZXctdXNlci1wcm9maWxlIiwidmlldy1wcml2YXRlLXJlcG9ydHMiXX0.xZ_mlnT-JAdAHdJVd1jJ5JjLzZ7UA9ifz86iHyjLnjr54XczYgvIAx8WE_7GgA1PuzQDy9oCzNLVfIA-8MbTnvQ6WlYYovhU7fWCQAPThvcWG7po6qBe0jG-L4NR9ox9lKGit1FuccSB32HYf22ejmt1Ke7viPKghUpr12UHb9UHjX7VITxBP5F2t9W6HCneErlo5EWX39TO6No72jpjDscygWHO9iA5XxQ6o1PjEzSxmiNVD8VF9jTgT40m-lak2h4okFzyfIG30rzMCwEcUbe06WgsadA69UGIPNJ_tf4kwI2gkAoZf1tjaUvro4xgzQHSL3E9zLn7rhYYxN26d6hGKkPiCwQiBttIyIgFCRBaEgR3nG7yxoGGhPwc-UmkW7_hA8rgQjsyZhIptFv6E7bc4B-dfraU_ED5QQ-C71HfXJZo7n9NhE0NSZQzypU3x41-R4u5DcLWWCiVru8SFbpaxUiRX4JBP779_Fvh_EaihBWg1Ct26SKpyGdfSofwD_Yye6r9if3Qezm-zjGWpkLrgc-3gFTH-VQgEnWKqojBSPdF4A1t3lnhWMihzr876heOrYzb2_oPif7LCaHnb9558r4RUIwcMoY4jW1sLpzBPdl5hdhqUlv2WcMKqo2RlJK9O-1RkpCTpXA2tzn9tjZUNqjSrBkvE0Z7MhOPdfU'

# Set up the API URL
api_url = 'https://www.warcraftlogs.com/api/v2'

# Set up the headers for the API request
headers = {
    'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI5OGEzYWZjMy1kZWUyLTQ5MDktOGY0Yy1lZmQ3ODdhZGVhNjEiLCJqdGkiOiJhNTcxZjU5ZWRjZGNhZDA1MDM1ZmY1NDc3NmVlOTE4MWNhZjJkMDlhNjg1MGE2NDVjZTc3NTBiOTdjZWZkMzc4ODM5MTRiZWJlNzhjMmM1NiIsImlhdCI6MTY3ODI4OTU0OC4xMjM1NiwibmJmIjoxNjc4Mjg5NTQ4LjEyMzU2MywiZXhwIjoxNzA5MzkzNTQ4LjExNzM3OCwic3ViIjoiIiwic2NvcGVzIjpbInZpZXctdXNlci1wcm9maWxlIiwidmlldy1wcml2YXRlLXJlcG9ydHMiXX0.xZ_mlnT-JAdAHdJVd1jJ5JjLzZ7UA9ifz86iHyjLnjr54XczYgvIAx8WE_7GgA1PuzQDy9oCzNLVfIA-8MbTnvQ6WlYYovhU7fWCQAPThvcWG7po6qBe0jG-L4NR9ox9lKGit1FuccSB32HYf22ejmt1Ke7viPKghUpr12UHb9UHjX7VITxBP5F2t9W6HCneErlo5EWX39TO6No72jpjDscygWHO9iA5XxQ6o1PjEzSxmiNVD8VF9jTgT40m-lak2h4okFzyfIG30rzMCwEcUbe06WgsadA69UGIPNJ_tf4kwI2gkAoZf1tjaUvro4xgzQHSL3E9zLn7rhYYxN26d6hGKkPiCwQiBttIyIgFCRBaEgR3nG7yxoGGhPwc-UmkW7_hA8rgQjsyZhIptFv6E7bc4B-dfraU_ED5QQ-C71HfXJZo7n9NhE0NSZQzypU3x41-R4u5DcLWWCiVru8SFbpaxUiRX4JBP779_Fvh_EaihBWg1Ct26SKpyGdfSofwD_Yye6r9if3Qezm-zjGWpkLrgc-3gFTH-VQgEnWKqojBSPdF4A1t3lnhWMihzr876heOrYzb2_oPif7LCaHnb9558r4RUIwcMoY4jW1sLpzBPdl5hdhqUlv2WcMKqo2RlJK9O-1RkpCTpXA2tzn9tjZUNqjSrBkvE0Z7MhOPdfU',
    'Content-Type': 'application/json',
}

# code = input(("Enter report code: ")) # Example of code : n6rqwa7ZHjWvY84K
warcraftlogcode = ""


@csrf_exempt
def index(request):
    warcraftlogcode = json.loads(request.body)
    warcraftlogcode = warcraftlogcode['text']


    data = {'query': f'''{{ reportData {{
        report(code: "{warcraftlogcode}") {{
            title
            table(startTime: 0, endTime: 99999999999)
            owner {{
                name
            }}
            healthStone: events(
                dataType: Healing
                startTime: 0
                endTime: 999999999
                abilityID: 6262
            ) {{
                data
            }},
            death: events(
                dataType: Deaths
                startTime: 0
                endTime: 999999999
            ) {{
                data
            }},
            playerDetails(startTime:0, endTime: 99999999)
        }}
        }}}}
        '''}
    print(data)

    response = requests.post(api_url, headers=headers, json=data)
    datas = response.json()
    print("warcraftlogcode :", warcraftlogcode)

    return JsonResponse({'hello': 'worldd', **datas})
