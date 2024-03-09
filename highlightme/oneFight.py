from collections import defaultdict

import requests

report_id = 'FR4pHbB8XktYqGzZ'
api_key = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI5Yjg0MTZjYS1kODU4LTRmMjItOTQxMS1jMjBjNWE3OGQzOGIiLCJqdGkiOiJlZGJkM2RlNjQ0ZjQzYzkxNzU3N2Y2NTVmYzU3NTg5OGNjZTE3YWExYWQ1MmRlMTM4YzRmMjUxMzg2NGJjZDRiYWE1MDE1M2E5ZGI2Mzg5ZCIsImlhdCI6MTcwOTk4NTE1MS4yNzU4MTIsIm5iZiI6MTcwOTk4NTE1MS4yNzU4MTUsImV4cCI6MTc0MTA4OTE1MS4yNjcyNTksInN1YiI6IiIsInNjb3BlcyI6WyJ2aWV3LXVzZXItcHJvZmlsZSIsInZpZXctcHJpdmF0ZS1yZXBvcnRzIl19.IQrvKFJqR0g1ltu8j868s9Y7ackDtPN7J0cq7P99tWbBsPXivNKaI31VrmbCTzcvxiA_ZnRn3iyB-TbhQOluSeoGejNrjsupFuMCDpVjgi_p9ZzDRYW54K7U-O9UPtVJF5ItbL3rQRn3NZLFKlbwh7WFm-e6IGLbpBK9bhZ3Br-sE-bG6rW9LWWW_NssMam6qqtHg3mFFlAxyiw8Q3rQn7chWIuH30O6nozYprsiqO4-aPT0Ms9zkeTmgV0qN3aoZDeXZXFnSSC8H9bBEc9ppC-UvnxsnSkLSoSvF1RmVkl_lGGtJw-FL30k1sbTm236BMX9seoVUT1E7Uk6xtbS98HcnayvgSdR1vK-giBx69UvkMpLXSxTYbwSYoR1D8trvdoo5Bq3OmFyJb8yRwLTem0Iq4-X4JEUmRL-IymapOe0pMSCcyfQ3sstmRps3w0zbFZoks-641d1pnIP2rDPYDILOC7D4D6WLP-DojCPnwMHg_o6LCYspd4YxwWPb5IYS4r0MDB0ewPr3rKN2ADOsZvgU-gzr3sMRojfBzMIHCSVlsUNVwOkee3oSfsjICHgOwkpP5IihaFEYRskrb_xKFMmKv-VxAwRJApoJWTCmIq1BL5Ao8w7L3gsDKDvHqf2JEHwCibZ4JG3QVBbnCWGY6k-uN7ii-D5PAlJXjntT4Y'

# Set up the API URL
api_url = 'https://www.warcraftlogs.com/api/v2'

# Set up the headers for the API request
headers = {
    'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI5Yjg0MTZjYS1kODU4LTRmMjItOTQxMS1jMjBjNWE3OGQzOGIiLCJqdGkiOiJlZGJkM2RlNjQ0ZjQzYzkxNzU3N2Y2NTVmYzU3NTg5OGNjZTE3YWExYWQ1MmRlMTM4YzRmMjUxMzg2NGJjZDRiYWE1MDE1M2E5ZGI2Mzg5ZCIsImlhdCI6MTcwOTk4NTE1MS4yNzU4MTIsIm5iZiI6MTcwOTk4NTE1MS4yNzU4MTUsImV4cCI6MTc0MTA4OTE1MS4yNjcyNTksInN1YiI6IiIsInNjb3BlcyI6WyJ2aWV3LXVzZXItcHJvZmlsZSIsInZpZXctcHJpdmF0ZS1yZXBvcnRzIl19.IQrvKFJqR0g1ltu8j868s9Y7ackDtPN7J0cq7P99tWbBsPXivNKaI31VrmbCTzcvxiA_ZnRn3iyB-TbhQOluSeoGejNrjsupFuMCDpVjgi_p9ZzDRYW54K7U-O9UPtVJF5ItbL3rQRn3NZLFKlbwh7WFm-e6IGLbpBK9bhZ3Br-sE-bG6rW9LWWW_NssMam6qqtHg3mFFlAxyiw8Q3rQn7chWIuH30O6nozYprsiqO4-aPT0Ms9zkeTmgV0qN3aoZDeXZXFnSSC8H9bBEc9ppC-UvnxsnSkLSoSvF1RmVkl_lGGtJw-FL30k1sbTm236BMX9seoVUT1E7Uk6xtbS98HcnayvgSdR1vK-giBx69UvkMpLXSxTYbwSYoR1D8trvdoo5Bq3OmFyJb8yRwLTem0Iq4-X4JEUmRL-IymapOe0pMSCcyfQ3sstmRps3w0zbFZoks-641d1pnIP2rDPYDILOC7D4D6WLP-DojCPnwMHg_o6LCYspd4YxwWPb5IYS4r0MDB0ewPr3rKN2ADOsZvgU-gzr3sMRojfBzMIHCSVlsUNVwOkee3oSfsjICHgOwkpP5IihaFEYRskrb_xKFMmKv-VxAwRJApoJWTCmIq1BL5Ao8w7L3gsDKDvHqf2JEHwCibZ4JG3QVBbnCWGY6k-uN7ii-D5PAlJXjntT4Y',
    'Content-Type': 'application/json',
}

# code = input(("Enter report code: ")) # Example of code : n6rqwa7ZHjWvY84K

data = {'query': f'''{{ reportData {{
        report(code: "FR4pHbB8XktYqGzZ") {{
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

# Make the API request
response = requests.post(api_url, headers=headers, json=data)


# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()
    print("▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄")
    print("▓\033[1m Title : \033[0m" + data['data']['reportData']['report'].get('title'),
          "▓\033[1m Uploaded By : \033[0m" + "\033[36m" + data['data']['reportData']['report']['owner'].get(
              'name') + "\033[0m ▓")
    print("▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀")
else:
    print(f'Error fetching fight data: {response.status_code} - {response.text}')


playersMap = {}

for role in ['tanks', 'healers', 'dps']:
    for player in data['data']['reportData']['report']['playerDetails']['data']['playerDetails'][role]:
        playersMap[player['id']] = player
print("PlayersMap : ", playersMap)


# countofDeaths = defaultdict(int)
# print("DEATHS RECAP :")
# # Print out the fight details
# for items in data['data']['reportData']['report']['table']['data']['deathEvents']:
#     countofDeaths[items.get('name')] += 1


print("-----------------------------------------------------------------")
print("---------------------- COUNT OF DEATHS --------------------------")
print("-----------------------------------------------------------------")

print("--------------- Encounters & Trash fights -------------------")

deathByPlayer = {}

for event in data['data']['reportData']['report']['death']['data']:
    playerID = event['targetID']
    deathByPlayer.setdefault(playerID, 0)
    deathByPlayer[playerID] += 1

# Tri décroissant morts
newDict = {k: v for k, v in sorted(deathByPlayer.items(), key=lambda item: item[1], reverse=True)}
print("\nnewDict sorted: ", newDict)

print(newDict.items())
for playerID, death in newDict.items():
    print(playersMap[playerID]['name'], death, "deaths")

print("\nConclusion : \033[0;31;40m Maximilian cheat \033[0;31;40m")


# print("-----------------------------------------------------------------")
# print("---------------------- HEALTHSTONE USE --------------------------")
# print("-----------------------------------------------------------------")
#
# healthStonesUsed = {}
# print("Use of healthstone during the raid :")
#
# for event in data['data']['reportData']['report']['healthStone']['data']:
#     playerID = event['sourceID']
#     healthStonesUsed.setdefault(playerID, 0)
#     healthStonesUsed[playerID] += 1
#
# print(healthStonesUsed)
#
# for playerID, healthStone in healthStonesUsed.items():
#     print(playersMap[playerID]['name'], "used ", healthStone, "healthStone")
#
#
# print("-----------------------------------------------------------------")
# print("---------------------- POTION USE --------------------------")
# print("-----------------------------------------------------------------")
#
# # potionUsed = {}
#
# print("Use of potions during the raid :")
#
# for event in data['data']['reportData']['report']['potion']['data']:
#     playerID = event['sourceID']
#     healthStonesUsed.setdefault(playerID, 0)
#     healthStonesUsed[playerID] += 1
#
# print(healthStonesUsed)
#
# for playerID, healthStone in healthStonesUsed.items():
#     print(playersMap[playerID]['name'], "used ", healthStone, "healthStone")
