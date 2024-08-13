def highlight_lava_death(datas, global_info):
    # Identifier l'ID de l'ability liée à la mort par lave
    LAVA_ABILITY_ID = 372339

    # Récupérer les événements de décès
    death_events = datas['data']['reportData']['report']['table']['data']['deathEvents']

    # Dictionnaire pour compter les morts par lave
    lava_death_counts = {}

    for event in death_events:
        # Vérifier si l'événement contient une ability
        if 'ability' in event and event['ability']['guid'] == LAVA_ABILITY_ID:
            player_name = event['name']
            if player_name not in lava_death_counts:
                lava_death_counts[player_name] = 0
            lava_death_counts[player_name] += 1

    # Trouver le joueur avec le plus grand nombre de morts par lave
    if lava_death_counts:
        most_lava_deaths_player = max(lava_death_counts, key=lava_death_counts.get)
        most_lava_deaths_count = lava_death_counts[most_lava_deaths_player]
    else:
        most_lava_deaths_player = "Aucun joueur"
        most_lava_deaths_count = 0

    # Afficher l'ensemble des joueurs et leur nombre de morts par lave
    for player, count in lava_death_counts.items():
        print(f"{player} died from lava {count} times")

    # Retourner les résultats sous forme de dictionnaire
    return {
        "player": most_lava_deaths_player,
        "lavaDeathCount": most_lava_deaths_count,
        "description": "Player died the most times from lava" if most_lava_deaths_count > 0 else "No deaths from lava",
        "allLavaDeaths": lava_death_counts  # Ajouter l'ensemble des décès par lave
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
                                {'name': 'Amatsukami', 'id': 14, 'guid': 133009107, 'type': 'Monk', 'deathTime': 217936, 'ability': {'name': 'Flaming Pestilence', 'guid': 421960}},
                                {'name': 'Amatsukami', 'id': 14, 'guid': 133009107, 'type': 'Monk', 'deathTime': 220000, 'ability': {'name': 'Lava Burst', 'guid': 372339}},
                                {'name': 'Darkentrall', 'id': 5, 'guid': 203651226, 'type': 'Shaman', 'deathTime': 178962, 'ability': {'name': 'Marked for Torment', 'guid': 372339}},
                                {'name': 'Lightbringer', 'id': 2, 'guid': 203651227, 'type': 'Paladin', 'deathTime': 179000, 'ability': {'name': 'Hammer of Justice', 'guid': 853}},
                                {'name': 'Darkentrall', 'id': 5, 'guid': 203651226, 'type': 'Shaman', 'deathTime': 179500, 'ability': {'name': 'Lava Burst', 'guid': 372339}},
                                {'name': 'Heavydamage', 'id': 3, 'guid': 203651228, 'type': 'Warrior', 'deathTime': 180000, 'ability': {'name': 'Execute', 'guid': 5308}},
                                {'name': 'Kamihate', 'id': 3, 'guid': 210582175, 'type': 'Warlock', 'deathTime': 242083, 'icon': 'Warlock-Demonology'}  # Mort due à l'environnement
                                # Ajoutez d'autres événements de décès pour tester
                            ]
                        }
                    }
                }
            }
        }
    }
    # TODO: Handle equality death count

    result = highlight_lava_death(datas)
    print(f"Player who died the most from lava: {result['player']} with {result['lavaDeathCount']} lava deaths")
