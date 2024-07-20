def highlight_pull_before_tanks(events_data, global_info_data):
    fights = global_info_data['data']['reportData']['report']['fightsEncounters']
    players = events_data['data']['reportData']['report']['table']['data']['composition']

    # Créer un dictionnaire pour mapper les sourceID aux noms des joueurs
    id_to_name = {player['id']: player['name'] for player in players}
    tanks = {player['id'] for player in players if any(spec['role'] == 'tank' for spec in player['specs'])}

    # Dictionnaire pour compter le nombre de pulls de chaque joueur
    pull_counts = {}

    # Parcourir les sections d'événements (event_1, event_2, etc.)
    for i, fight in enumerate(fights, start=1):
        fight_id = fight['id']
        event_key = f'event_{i}'
        if event_key in events_data['data']['reportData']['report']:
            fight_events = events_data['data']['reportData']['report'][event_key]['data']
            damage_events = [event for event in fight_events if event['type'] == 'damage']

            if damage_events:
                first_damage_event = min(damage_events, key=lambda e: e['timestamp'])
                source_id = first_damage_event['sourceID']

                # Vérifier si le joueur n'est pas un tank
                if source_id not in tanks:
                    if source_id not in pull_counts:
                        pull_counts[source_id] = 0
                    pull_counts[source_id] += 1

    # Trouver le joueur qui a pull le plus de fois
    if pull_counts:
        max_pulls_player = max(pull_counts, key=pull_counts.get)
        max_pulls_count = pull_counts[max_pulls_player]
        max_pulls_name = id_to_name.get(max_pulls_player, "Unknown")
    else:
        max_pulls_player = None
        max_pulls_count = 0
        max_pulls_name = "Unknown"

    # Retourner le joueur qui a pull le plus souvent avant les tanks
    return {
        "playerID": max_pulls_player,
        "playerName": max_pulls_name,
        "pullCount": max_pulls_count
    }

if __name__ == "__main__":
    events_data = {
        'data': {
            'reportData': {
                'report': {
                    'title': 'Amirdrassil HM FULL',
                    'guild': {'name': 'Evenly'},
                    'owner': {'name': 'Generald'},
                    'table': {
                        'data': {
                            'totalTime': 4810911,
                            'itemLevel': 479.85589599609375,
                            'composition': [
                                {'name': 'Joflamme', 'id': 1, 'guid': 205961504, 'type': 'Druid', 'specs': [{'spec': 'Restoration', 'role': 'healer'}]},
                                {'name': 'Generald', 'id': 6, 'guid': 205961505, 'type': 'Warrior', 'specs': [{'spec': 'Protection', 'role': 'tank'}]},
                                {'name': 'DPS1', 'id': 4, 'guid': 205961506, 'type': 'Mage', 'specs': [{'spec': 'Fire', 'role': 'dps'}]},
                                {'name': 'DPS2', 'id': 5, 'guid': 205961507, 'type': 'Hunter', 'specs': [{'spec': 'Marksmanship', 'role': 'dps'}]}
                            ]
                        }
                    },
                    'event_1': {
                        'data': [
                            {'timestamp': 139348, 'type': 'damage', 'sourceID': 6, 'targetID': 16, 'abilityGameID': 1, 'fight': 1, 'buffs': '396092.393438.360827.1126.371172.378762.', 'hitType': 1, 'amount': 7444, 'mitigated': 3190, 'unmitigatedAmount': 10634},
                            {'timestamp': 139350, 'type': 'damage', 'sourceID': 4, 'targetID': 16, 'abilityGameID': 1, 'fight': 1, 'buffs': '396092.393438.360827.1126.371172.378762.', 'hitType': 1, 'amount': 5000, 'mitigated': 2000, 'unmitigatedAmount': 7000}
                        ]
                    },
                    'event_2': {
                        'data': [
                            {'timestamp': 443450, 'type': 'damage', 'sourceID': 5, 'targetID': 17, 'abilityGameID': 2, 'fight': 2, 'buffs': '396092.393438.360827.1126.371172.378762.', 'hitType': 1, 'amount': 6000, 'mitigated': 2500, 'unmitigatedAmount': 8500},
                            {'timestamp': 443451, 'type': 'damage', 'sourceID': 6, 'targetID': 17, 'abilityGameID': 2, 'fight': 2, 'buffs': '396092.393438.360827.1126.371172.378762.', 'hitType': 1, 'amount': 7000, 'mitigated': 3000, 'unmitigatedAmount': 10000}
                        ]
                    }
                }
            }
        }
    }

    global_info_data = {
        'data': {
            'reportData': {
                'report': {
                    'title': 'Amirdrassil HM FULL',
                    'guild': {'name': 'Evenly'},
                    'owner': {'name': 'Generald'},
                    'fights': [
                        {'encounterID': 0, 'id': 1, 'startTime': 12446, 'endTime': 15462},
                        {'encounterID': 2820, 'id': 2, 'startTime': 139055, 'endTime': 308750}
                    ],
                    'table': {
                        'data': {
                            'totalTime': 4810911,
                            'itemLevel': 479.85589599609375,
                            'composition': [
                                {'name': 'Joflamme', 'id': 1, 'guid': 205961504, 'type': 'Druid', 'specs': [{'spec': 'Restoration', 'role': 'healer'}]},
                                {'name': 'Generald', 'id': 6, 'guid': 205961505, 'type': 'Warrior', 'specs': [{'spec': 'Protection', 'role': 'tank'}]},
                                {'name': 'DPS1', 'id': 4, 'guid': 205961506, 'type': 'Mage', 'specs': [{'spec': 'Fire', 'role': 'dps'}]},
                                {'name': 'DPS2', 'id': 5, 'guid': 205961507, 'type': 'Hunter', 'specs': [{'spec': 'Marksmanship', 'role': 'dps'}]}
                            ]
                        }
                    }
                }
            }
        }
    }

    highlight = highlight_pull_before_tanks(events_data, global_info_data)
    print(f"Player who pulled before tank the most: {highlight['playerName']} (ID: {highlight['playerID']}) with {highlight['pullCount']} pulls")
