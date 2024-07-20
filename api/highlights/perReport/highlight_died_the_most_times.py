def highlight_died_the_most_times(datas):

    death_events = datas['data']['reportData']['report']['table']['data']['deathEvents']

    # Dictionnaire pour compter le nombre de décès de chaque joueur
    death_counts = {}

    for event in death_events:
        player_name = event['name']
        if player_name not in death_counts:
            death_counts[player_name] = 0
        death_counts[player_name] += 1

    # Trouver le joueur avec le plus grand nombre de décès
    if death_counts:
        most_deaths_player = max(death_counts, key=death_counts.get)
        most_deaths_count = death_counts[most_deaths_player]
    else:
        most_deaths_player = None
        most_deaths_count = 0

    # Retourner les résultats sous forme de dictionnaire
    return {
        "playerName": most_deaths_player,
        "deathCount": most_deaths_count,
        "description": "Player died the most times"
    }

# Exemple d'utilisation
if __name__ == "__main__":
    datas = {
        'data': {
            'reportData': {
                'report': {
                    'table': {
                        'data': {
                            'deathEvents': [
                                {'name': 'Darkentrall', 'id': 5, 'guid': 203651226, 'type': 'Shaman', 'deathTime': 178962, 'ability': {'name': 'Marked for Torment', 'guid': 422776}},
                                {'name': 'Lightbringer', 'id': 2, 'guid': 203651227, 'type': 'Paladin', 'deathTime': 179000, 'ability': {'name': 'Hammer of Justice', 'guid': 853}},
                                {'name': 'Darkentrall', 'id': 5, 'guid': 203651226, 'type': 'Shaman', 'deathTime': 179500, 'ability': {'name': 'Lightning Bolt', 'guid': 403}},
                                {'name': 'Heavydamage', 'id': 3, 'guid': 203651228, 'type': 'Warrior', 'deathTime': 180000, 'ability': {'name': 'Execute', 'guid': 5308}},
                                # Ajoutez d'autres événements de décès pour tester
                            ]
                        }
                    }
                }
            }
        }
    }

    result = highlight_died_the_most_times(datas)
    print(f"Player who died the most: {result['player']} with {result['deathCount']} deaths")