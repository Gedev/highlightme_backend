def highlight_potion_death(datas):
    # Identifier l'ID de l'ability liée à la mort par potion
    POTION_ABILITY_ID = 423416

    # Récupérer les événements de décès
    death_events = datas['data']['reportData']['report']['table']['data']['deathEvents']

    # Dictionnaire pour compter les morts par potion
    potion_death_counts = {}

    for event in death_events:
        # Vérifier si l'événement contient une ability
        if 'ability' in event and event['ability']['guid'] == POTION_ABILITY_ID:
            player_name = event['name']
            if player_name not in potion_death_counts:
                potion_death_counts[player_name] = 0
            potion_death_counts[player_name] += 1

    # Trouver le joueur avec le plus grand nombre de morts par potion
    if potion_death_counts:
        most_potion_deaths_player = max(potion_death_counts, key=potion_death_counts.get)
        most_potion_deaths_count = potion_death_counts[most_potion_deaths_player]
    else:
        most_potion_deaths_player = "Aucun joueur"
        most_potion_deaths_count = 0

    # Afficher l'ensemble des joueurs et leur nombre de morts par potion
    for player, count in potion_death_counts.items():
        print(f"{player} died from potion {count} times")

    # Retourner les résultats sous forme de dictionnaire
    return {
        "playerName": most_potion_deaths_player,
        "potionDeathCount": most_potion_deaths_count,
        "description": "Player died the most times from potion" if most_potion_deaths_count > 0 else "No deaths from potion",
        "allPotionDeaths": potion_death_counts  # Ajouter l'ensemble des décès par potion
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
                                {'name': 'Amatsukami', 'id': 14, 'guid': 133009107, 'type': 'Monk', 'deathTime': 220000, 'ability': {'name': 'Potion Overdose', 'guid': 423416}},
                                {'name': 'Darkentrall', 'id': 5, 'guid': 203651226, 'type': 'Shaman', 'deathTime': 178962, 'ability': {'name': 'Marked for Torment', 'guid': 422776}},
                                {'name': 'Lightbringer', 'id': 2, 'guid': 203651227, 'type': 'Paladin', 'deathTime': 179000, 'ability': {'name': 'Hammer of Justice', 'guid': 853}},
                                {'name': 'Darkentrall', 'id': 5, 'guid': 203651226, 'type': 'Shaman', 'deathTime': 179500, 'ability': {'name': 'Potion Overdose', 'guid': 423416}},
                                {'name': 'Heavydamage', 'id': 3, 'guid': 203651228, 'type': 'Warrior', 'deathTime': 180000, 'ability': {'name': 'Execute', 'guid': 5308}},
                                # Ajoutez d'autres événements de décès pour tester
                            ]
                        }
                    }
                }
            }
        }
    }

    result = highlight_potion_death(datas)
    print(f"Player who died the most from potion: {result['player']} with {result['potionDeathCount']} potion of withering dreams")
