from collections import defaultdict

import requests

report_id = 'FR4pHbB8XktYqGzZ'
api_key = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI5Yjg0MTZjYS1kODU4LTRmMjItOTQxMS1jMjBjNWE3OGQzOGIiLCJqdGkiOiIzNWU2Yzc1MmU4MTcxOGExODc0Zjc1NDIwNmMxZTAxNmQ1NDFhZWIzZWFhZGJhNGFlYjAwNDgwOTU0ZDgyOGVlMGVmMjcwMDQ1NDQ1YTM1MSIsImlhdCI6MTcwOTkxNjI5NS4wMjg4NDgsIm5iZiI6MTcwOTkxNjI5NS4wMjg4NTEsImV4cCI6MTc0MTAyMDI5NS4wMjA1ODMsInN1YiI6IiIsInNjb3BlcyI6WyJ2aWV3LXVzZXItcHJvZmlsZSIsInZpZXctcHJpdmF0ZS1yZXBvcnRzIl19.PwEgJjxr89jMzmnHFSD2xUwe02LIFD173f9p2KzTwXJ7MeAb9-IZb0NkigaarJEj6QYy6pRmCtx0JrphSwVfUv9IOmzZmysS7pNYELXLvYG27g7m_5UnuW8gIvNfQJF045tlAbAmeeGah5V67MuuirIyaOUV7QPdzHOTbmOn9b8h3MTv3fg41VvxqiPwruGvHPBSBM9D67CFjMLAfXlful6KEn0aZ3lXlx5xo0Brh5fzUHuZpvCKLZgJ-v4vucpefHPnzzKv7z4YKRQi_lgHinxP324Ntfp2jqj3ujWyuiGBYRyBnUUaEvjXxG6vXPkuX6xcdaYsCjkgnwu9QJWohHGBfelr3j65HrSl9l9VOcWjsjNIVLmQPngUu7nNcwRI4MzWg0B0TI-1m2P2eFIsXH2fEYMxyvFrpFSg7rfc8K7zc3PDHw2FP8-bn4iUk5_s480Mo4YZBHamOK5ZOz6jf0cW8RfC-fV6XXzyiIeV6OQMKsQv844pqsaxh_MPCPXd7RpdT_MxIJ_xevOvVs2i-DtmSAXfI6dQTQAN1d6E7ScbGwAwhQBkmUakJfbAABywApixxIBIlWLaoaGn6Qxek5FVh2nYhMek8ZcndxlJz1MaOKpXsq_AAA9YxLf2TEKA9Hb1mxiG_FkzrQtL-9gqleiszWQuTDlZrvK7Chjt8Dw'
# Set up the API URL
api_url = f'https://www.warcraftlogs.com/api/v2'

# Set up the headers for the API request
headers = {
    'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI5Yjg0MTZjYS1kODU4LTRmMjItOTQxMS1jMjBjNWE3OGQzOGIiLCJqdGkiOiIzNWU2Yzc1MmU4MTcxOGExODc0Zjc1NDIwNmMxZTAxNmQ1NDFhZWIzZWFhZGJhNGFlYjAwNDgwOTU0ZDgyOGVlMGVmMjcwMDQ1NDQ1YTM1MSIsImlhdCI6MTcwOTkxNjI5NS4wMjg4NDgsIm5iZiI6MTcwOTkxNjI5NS4wMjg4NTEsImV4cCI6MTc0MTAyMDI5NS4wMjA1ODMsInN1YiI6IiIsInNjb3BlcyI6WyJ2aWV3LXVzZXItcHJvZmlsZSIsInZpZXctcHJpdmF0ZS1yZXBvcnRzIl19.PwEgJjxr89jMzmnHFSD2xUwe02LIFD173f9p2KzTwXJ7MeAb9-IZb0NkigaarJEj6QYy6pRmCtx0JrphSwVfUv9IOmzZmysS7pNYELXLvYG27g7m_5UnuW8gIvNfQJF045tlAbAmeeGah5V67MuuirIyaOUV7QPdzHOTbmOn9b8h3MTv3fg41VvxqiPwruGvHPBSBM9D67CFjMLAfXlful6KEn0aZ3lXlx5xo0Brh5fzUHuZpvCKLZgJ-v4vucpefHPnzzKv7z4YKRQi_lgHinxP324Ntfp2jqj3ujWyuiGBYRyBnUUaEvjXxG6vXPkuX6xcdaYsCjkgnwu9QJWohHGBfelr3j65HrSl9l9VOcWjsjNIVLmQPngUu7nNcwRI4MzWg0B0TI-1m2P2eFIsXH2fEYMxyvFrpFSg7rfc8K7zc3PDHw2FP8-bn4iUk5_s480Mo4YZBHamOK5ZOz6jf0cW8RfC-fV6XXzyiIeV6OQMKsQv844pqsaxh_MPCPXd7RpdT_MxIJ_xevOvVs2i-DtmSAXfI6dQTQAN1d6E7ScbGwAwhQBkmUakJfbAABywApixxIBIlWLaoaGn6Qxek5FVh2nYhMek8ZcndxlJz1MaOKpXsq_AAA9YxLf2TEKA9Hb1mxiG_FkzrQtL-9gqleiszWQuTDlZrvK7Chjt8Dw',
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
