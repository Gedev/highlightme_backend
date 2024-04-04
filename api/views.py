import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

import requests
import random

report_id = 'FR4pHbB8XktYqGzZ'
api_key = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI5Yjg0MTZjYS1kODU4LTRmMjItOTQxMS1jMjBjNWE3OGQzOGIiLCJqdGkiOiJlZGJkM2RlNjQ0ZjQzYzkxNzU3N2Y2NTVmYzU3NTg5OGNjZTE3YWExYWQ1MmRlMTM4YzRmMjUxMzg2NGJjZDRiYWE1MDE1M2E5ZGI2Mzg5ZCIsImlhdCI6MTcwOTk4NTE1MS4yNzU4MTIsIm5iZiI6MTcwOTk4NTE1MS4yNzU4MTUsImV4cCI6MTc0MTA4OTE1MS4yNjcyNTksInN1YiI6IiIsInNjb3BlcyI6WyJ2aWV3LXVzZXItcHJvZmlsZSIsInZpZXctcHJpdmF0ZS1yZXBvcnRzIl19.IQrvKFJqR0g1ltu8j868s9Y7ackDtPN7J0cq7P99tWbBsPXivNKaI31VrmbCTzcvxiA_ZnRn3iyB-TbhQOluSeoGejNrjsupFuMCDpVjgi_p9ZzDRYW54K7U-O9UPtVJF5ItbL3rQRn3NZLFKlbwh7WFm-e6IGLbpBK9bhZ3Br-sE-bG6rW9LWWW_NssMam6qqtHg3mFFlAxyiw8Q3rQn7chWIuH30O6nozYprsiqO4-aPT0Ms9zkeTmgV0qN3aoZDeXZXFnSSC8H9bBEc9ppC-UvnxsnSkLSoSvF1RmVkl_lGGtJw-FL30k1sbTm236BMX9seoVUT1E7Uk6xtbS98HcnayvgSdR1vK-giBx69UvkMpLXSxTYbwSYoR1D8trvdoo5Bq3OmFyJb8yRwLTem0Iq4-X4JEUmRL-IymapOe0pMSCcyfQ3sstmRps3w0zbFZoks-641d1pnIP2rDPYDILOC7D4D6WLP-DojCPnwMHg_o6LCYspd4YxwWPb5IYS4r0MDB0ewPr3rKN2ADOsZvgU-gzr3sMRojfBzMIHCSVlsUNVwOkee3oSfsjICHgOwkpP5IihaFEYRskrb_xKFMmKv-VxAwRJApoJWTCmIq1BL5Ao8w7L3gsDKDvHqf2JEHwCibZ4JG3QVBbnCWGY6k-uN7ii-D5PAlJXjntT4Y'

# Set up the API URL
api_url = 'https://www.warcraftlogs.com/api/v2'

# Set up the headers for the API request
headers = {
    'Authorization': 'Bearer ' + settings.WARCRAFTLOGS_OAUTH.get('access_token', ''),
    'Content-Type': 'application/json',
}

# code = input(("Enter report code: ")) # Example of code : n6rqwa7ZHjWvY84K
warcraftlogcode = ""


# print("\033[36m ",  + "\033[0m ")
#
print(headers, settings.WARCRAFTLOGS_OAUTH)
@csrf_exempt
def index(request):
    warcraftlogcode = json.loads(request.body)
    print("\033[36m warcraftlogcode : ", warcraftlogcode, "\033[0m ")
    warcraftlogcode = warcraftlogcode['wl_report_code']

    list_humoristic_sentence = ["Il a ramassé les objets comme s'il était en mode aspirateur à butin.",
    "Il est tellement bien loti qu'il pourrait ouvrir sa propre boutique de chance.",
    "Ce gars est refait à la sauce de la victoire, avec une pincée de talent et beaucoup de bol.",
    "Il a pillé cette partie comme s'il était le roi des chapardeurs.",
    "Il a lové les trésors comme s'il était un écureuil de jeu vidéo.",
    "Ce joueur a ramassé plus de butin qu'un pirate dans une caverne remplie de pièces d'or.",
    "Il est reparti avec plus de trésors que le sac sans fond d'un magicien.",
    "Ce type a récupéré tant de choses qu'il a besoin d'un camion de déménagement virtuel.",
    "Il a attrapé les récompenses comme s'il était doté d'une compétence de super aimant.",
    "Ce joueur est tellement bien pourvu qu'il pourrait donner des leçons de chance à la loterie."]

    list_healthstones_humoristic_sentence = ["Accro à la pierre de soin"]

    datas = {'query': f'''{{ reportData {{
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
    print(datas)

    response = requests.post(api_url, headers=headers, json=datas)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        datas = response.json()
        print("▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄")
        print("▓\033[1m Title : \033[0m" + datas['data']['reportData']['report'].get('title'),
              "▓\033[1m Uploaded By : \033[0m" + "\033[36m" + datas['data']['reportData']['report']['owner'].get(
                  'name') + "\033[0m ▓")
        print("▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀")
    else:
        print(f'Error fetching fight data: {response.status_code} - {response.text}')
        print("warcraftlogcode :", warcraftlogcode)

    # GET PLAYERS DATA MAP
    playersMap = {}

    for role in ['tanks', 'healers', 'dps']:
        for player in datas['data']['reportData']['report']['playerDetails']['data']['playerDetails'][role]:
            playersMap[player['id']] = player
    print("\033[36m PlayersMap : ", playersMap, "\033[0m ")
    max_upgrade = 0
    player_dict = {}
    max_player_id = None

    # GET DIFFERENCE ITEMS LEVEL AFTER RAID
    for key, values in playersMap.items():
        min_level = values["minItemLevel"]
        max_level = values["maxItemLevel"]
        difference = max_level - min_level

        if difference > max_upgrade:
            max_upgrade = difference
            max_player_id = key

        print("Joueur", key, "Différence de niveau :", difference)

        # Ajout de l'ID du joueur et de la différence au dictionnaire
        # Création du dictionnaire avec la clé-valeur du joueur ayant la plus grande différence

    print("max upgrade found : ", max_upgrade)

    if max_player_id is not None:
        player_dict[max_player_id] = {
            'difference': max_upgrade,
            'name': playersMap[max_player_id]['name'],
            'humoristic_sentence': random.choice(list_humoristic_sentence)
        }

    # Choix aléatoire d'une phrase de la liste
    print("Dictionnaire clé-valeur :")
    print(player_dict)

    print("-----------------------------------------------------------------")
    print("---------------------- HEALTHSTONE USE --------------------------")
    print("-----------------------------------------------------------------")

    healthStonesUsed = {}
    print("Use of healthstone during the raid :")

    for event in datas['data']['reportData']['report']['healthStone']['data']:
        playerID = event['sourceID']
        healthStonesUsed.setdefault(playerID, 0)
        healthStonesUsed[playerID] += 1

    print(healthStonesUsed)

    max_healthStones_used = 0
    player_dict_max_hs = {}
    max_player_id_hsUsed = None

    for playerID, healthStone in healthStonesUsed.items():
        if healthStone > max_healthStones_used:
            max_healthStones_used = healthStone
            max_player_id_hsUsed = playerID

        print(playersMap[playerID]['name'], "used ", healthStone, "healthStone")

    if max_player_id_hsUsed is not None:
        player_dict_max_hs[max_player_id] = {
            'max_healthStones_used': max_healthStones_used,
            'name': playersMap[max_player_id_hsUsed]['name'],
            'humoristic_sentence': random.choice(list_healthstones_humoristic_sentence)
        }

    print(player_dict_max_hs)

    print("-----------------------------------------------------------------")
    print("---------------------- COUNT OF DEATHS --------------------------")
    print("-----------------------------------------------------------------")

    print("--------------- Encounters & Trash fights -------------------")

    deathByPlayer = {}
    dict_playerWithMaxDeath = {}
    max_player_death = 0
    max_player_death_id = None

    i = 1
    first_players_to_die = {}

    for event in datas['data']['reportData']['report']['death']['data']:
        playerID = event['targetID']
        deathByPlayer.setdefault(playerID, 0)
        deathByPlayer[playerID] += 1

        fight_id = event['fight']
        if fight_id not in first_players_to_die:
            first_players_to_die[fight_id] = {
                'fight': fight_id,
                'timestamp': event['timestamp'],
                'targetID': event['targetID']
            }

    # Tri décroissant morts
    newDict = {k: v for k, v in sorted(deathByPlayer.items(), key=lambda item: item[1], reverse=True)}
    print("\nnewDict sorted: ", newDict)

    print(newDict.items())
    for playerID, death in newDict.items():
        print(playersMap[playerID]['name'], death, "deaths")
        if max_player_death < death:
            max_player_death = death
            max_player_death_id = playerID

    if max_player_death_id is not None:
        dict_playerWithMaxDeath[max_player_death_id] = {
            'max_player_death': max_player_death,
            'name': playersMap[max_player_death_id]['name']
        }
    print("max player death :", max_player_death)

    print("Death events :", datas['data']['reportData']['report']['death']['data'])
    print("first players to die :", first_players_to_die)

    return JsonResponse({'hello': 'worldd', "maxupgrade": player_dict, **playersMap, **datas, "playerWithMaxHsUsed": player_dict_max_hs, "deaths": dict_playerWithMaxDeath})
