import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import requests
import random

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


# print("\033[36m ",  + "\033[0m ")
#

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

    return JsonResponse({'hello': 'worldd', "maxupgrade": player_dict, **playersMap, **datas})
