def highlight_death_counts_per_fight(datas, global_info_data):
    # Récupérer les combats
    fights = global_info_data['data']['reportData']['report']['fightsEncounters']
    death_events = datas['data']['reportData']['report']['deathEvents']['data']
    composition = datas['data']['reportData']['report']['table']['data']['composition']

    # Créer un dictionnaire pour mapper targetID aux noms des joueurs
    target_id_to_name = {player['id']: player['name'] for player in composition}

    # Dictionnaire pour stocker les décès par joueur par combat
    deaths_by_fight = {}

    # Initialiser le dictionnaire deaths_by_fight pour chaque combat
    for fight in fights:
        fight_id = fight['id']
        deaths_by_fight[fight_id] = {}

    # Compter les décès par joueur par combat
    for event in death_events:
        fight_id = event['fight']
        target_id = event['targetID']

        # Récupérer le nom du joueur, s'il n'existe pas, ajouter un log pour vérifier l'erreur potentielle
        player_name = target_id_to_name.get(target_id)
        if player_name is None:
            player_name = f"Unknown (ID: {target_id})"

        if fight_id not in deaths_by_fight:
            deaths_by_fight[fight_id] = {}

        if player_name not in deaths_by_fight[fight_id]:
            deaths_by_fight[fight_id][player_name] = 0

        deaths_by_fight[fight_id][player_name] += 1

    # Générer les highlights pour chaque combat
    highlights = []

    for fight_id, deaths in deaths_by_fight.items():
        for player, count in deaths.items():
            if count == 3:
                rarity = 'Rare'
                if count == 4:
                    rarity = 'Epic'
                elif count == 5:
                    rarity = 'Legendary'

                highlight = {
                    "fight_id": fight_id,
                    "player": player,
                    "highlight_value": count,
                    "description": f"{player} died {count} times in fight {fight_id}",
                    "img": "Gnomish-grave-digger.jpg",
                    "rarity": rarity
                }
                highlights.append(highlight)

    return highlights if highlights else None



# Exemple d'utilisation
if __name__ == "__main__":
    datas = {
        'data': {
            'reportData': {
                'report': {
                    'fights': [
                        {'encounterID': 2820, 'id': 1, 'startTime': 139055, 'endTime': 308750},
                        {'encounterID': 2709, 'id': 2, 'startTime': 443449, 'endTime': 676923}
                    ],
                    'deathEvents': [
                        {'timestamp': 622411, 'type': 'death', 'sourceID': -1, 'targetID': 5, 'abilityGameID': 0, 'fight': 1, 'killerID': 40, 'killingAbilityGameID': 422776},
                        {'timestamp': 882234, 'type': 'death', 'sourceID': -1, 'targetID': 14, 'abilityGameID': 0, 'fight': 1, 'killerID': 37, 'killingAbilityGameID': 421960},
                        {'timestamp': 882234, 'type': 'death', 'sourceID': -1, 'targetID': 14, 'abilityGameID': 0, 'fight': 1, 'killerID': 37, 'killingAbilityGameID': 421960},
                        {'timestamp': 882234, 'type': 'death', 'sourceID': -1, 'targetID': 14, 'abilityGameID': 0, 'fight': 1, 'killerID': 37, 'killingAbilityGameID': 421960},
                        {'timestamp': 882234, 'type': 'death', 'sourceID': -1, 'targetID': 14, 'abilityGameID': 0, 'fight': 2, 'killerID': 37, 'killingAbilityGameID': 421960},
                        {'timestamp': 882234, 'type': 'death', 'sourceID': -1, 'targetID': 14, 'abilityGameID': 0, 'fight': 2, 'killerID': 37, 'killingAbilityGameID': 421960},
                        {'timestamp': 882234, 'type': 'death', 'sourceID': -1, 'targetID': 14, 'abilityGameID': 0, 'fight': 2, 'killerID': 37, 'killingAbilityGameID': 421960},
                        {'timestamp': 882234, 'type': 'death', 'sourceID': -1, 'targetID': 14, 'abilityGameID': 0, 'fight': 2, 'killerID': 37, 'killingAbilityGameID': 421960},
                        {'timestamp': 882234, 'type': 'death', 'sourceID': -1, 'targetID': 14, 'abilityGameID': 0, 'fight': 2, 'killerID': 37, 'killingAbilityGameID': 421960},
                        # Ajoutez d'autres événements de décès pour tester
                    ],
                    'table': {
                        'data': {
                            'composition': [
                                {'name': 'Player1', 'id': 14, 'guid': 205961504, 'type': 'Druid', 'specs': [{'spec': 'Restoration', 'role': 'healer'}]},
                                {'name': 'Player2', 'id': 2, 'guid': 205961505, 'type': 'Warrior', 'specs': [{'spec': 'Protection', 'role': 'tank'}]},
                                {'name': 'Player3', 'id': 3, 'guid': 205961506, 'type': 'Mage', 'specs': [{'spec': 'Fire', 'role': 'dps'}]},
                                {'name': 'Player4', 'id': 4, 'guid': 205961507, 'type': 'Hunter', 'specs': [{'spec': 'Marksmanship', 'role': 'dps'}]},
                                # Ajoutez d'autres joueurs pour tester
                            ]
                        }
                    }
                }
            }
        }
    }

    # TODO: ADD GLOBAL INFO DATA

    result = highlight_death_counts_per_fight(datas)
    for key, highlights in result.items():
        print(key)
        for highlight in highlights:
            print(highlight)
