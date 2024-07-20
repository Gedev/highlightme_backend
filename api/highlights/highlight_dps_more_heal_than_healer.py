def highlight_dps_more_heal_than_healer(datas):
    # Identifier les rôles
    HEALER_ROLE = 'healer'
    DPS_ROLE = 'dps'

    # Récupérer les événements de guérison et les événements de décès
    heal_events = datas['data']['reportData']['report']['table']['data']['healing']
    death_events = datas['data']['reportData']['report']['table']['data']['deathEvents']

    # Dictionnaire pour stocker la guérison totale par joueur
    total_healing_by_player = {}

    # Compter la guérison de chaque joueur
    for event in heal_events:
        player_name = event['name']
        healing_done = event['total']
        if player_name not in total_healing_by_player:
            total_healing_by_player[player_name] = 0
        total_healing_by_player[player_name] += healing_done

    # Dictionnaire pour stocker les décès par joueur
    deaths_by_player = {event['name']: event for event in death_events}

    # Trouver les healers et vérifier s'ils sont morts
    healer_healing = {}
    dps_healing = {}

    for player, healing in total_healing_by_player.items():
        player_info = next(p for p in datas['data']['reportData']['report']['table']['data']['composition'] if p['name'] == player)
        role = player_info['specs'][0]['role']

        if role == HEALER_ROLE:
            if player not in deaths_by_player:
                healer_healing[player] = healing
        elif role == DPS_ROLE:
            dps_healing[player] = healing

    # Comparer la guérison des DPS à celle des healers
    highlights = []

    for dps, dps_heal in dps_healing.items():
        for healer, healer_heal in healer_healing.items():
            if dps_heal > healer_heal:
                highlights.append({
                    "dpsPlayer": dps,
                    "dpsHealing": dps_heal,
                    "healerPlayer": healer,
                    "healerHealing": healer_heal,
                    "description": f"{dps} did more healing ({dps_heal}) than {healer} ({healer_heal})"
                })

    return highlights

# Exemple d'utilisation
if __name__ == "__main__":
    datas = {
        'data': {
            'reportData': {
                'report': {
                    'table': {
                        'data': {
                            'healing': [
                                {'name': 'DPS1', 'id': 4, 'guid': 205961506, 'type': 'Mage', 'total': 5000},
                                {'name': 'Healer1', 'id': 1, 'guid': 205961504, 'type': 'Druid', 'total': 10000000},
                                {'name': 'DPS2', 'id': 5, 'guid': 205961507, 'type': 'Hunter', 'total': 13000},
                                {'name': 'Healer2', 'id': 2, 'guid': 205961505, 'type': 'Priest', 'total': 12000},
                                # Ajoutez d'autres événements de guérison pour tester
                            ],
                            'deathEvents': [
                                {'name': 'Healer1', 'id': 1, 'guid': 205961504, 'type': 'Druid', 'deathTime': 20000},
                                # Ajoutez d'autres événements de décès pour tester
                            ],
                            'composition': [
                                {'name': 'DPS1', 'id': 4, 'guid': 205961506, 'type': 'Mage', 'specs': [{'spec': 'Fire', 'role': 'dps'}]},
                                {'name': 'Healer1', 'id': 1, 'guid': 205961504, 'type': 'Druid', 'specs': [{'spec': 'Restoration', 'role': 'healer'}]},
                                {'name': 'DPS2', 'id': 5, 'guid': 205961507, 'type': 'Hunter', 'specs': [{'spec': 'Marksmanship', 'role': 'dps'}]},
                                {'name': 'Healer2', 'id': 2, 'guid': 205961505, 'type': 'Priest', 'specs': [{'spec': 'Holy', 'role': 'healer'}]},
                                # Ajoutez d'autres joueurs pour tester
                            ]
                        }
                    }
                }
            }
        }
    }

    result = highlight_dps_more_heal_than_healer(datas)
    for highlight in result:
        print(highlight)
