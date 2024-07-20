def highlight_death_from_personal_ability(personal_ability):
    # Identifier l'ID de l'ability liée à la mort par potion
    BURNING_RUSH_ABILITY_ID = 111400

    # Récupérer les événements de décès
    death_events = datas['data']['reportData']['report']['table']['data']['deathEvents']

    # Dictionnaire pour compter les morts par potion
    burning_rush_death_counts = {}

    for event in death_events:
        if event['ability']['guid'] == BURNING_RUSH_ABILITY_ID:
            player_name = event['name']
            if player_name not in burning_rush_death_counts:
                burning_rush_death_counts[player_name] = 0
            burning_rush_death_counts[player_name] += 1

    # Trouver le joueur avec le plus grand nombre de morts par potion
    if burning_rush_death_counts:
        death_by_personal_ability_player = max(burning_rush_death_counts, key=burning_rush_death_counts.get)
        most_death_count = burning_rush_death_counts[death_by_personal_ability_player]
    else:
        death_by_personal_ability_player = "Aucun joueur"
        most_death_count = 0

    # Afficher l'ensemble des joueurs et leur nombre de morts par potion
    for player, count in burning_rush_death_counts.items():
        print(f"{player} died from potion {count} times")

    # Retourner les résultats sous forme de dictionnaire
    return {
        "playerName": death_by_personal_ability_player,
        "potionDeathCount": most_death_count,
        "description": "Player died the most times from potion" if most_death_count > 0 else "No deaths from personal ability",
        "allPotionDeaths": burning_rush_death_counts  # Ajouter l'ensemble des décès par potion
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
                                {'name': 'Heavydamage', 'id': 3, 'guid': 203651228, 'type': 'Warlock', 'deathTime': 180000, 'ability': {'name': 'Burning Rush', 'guid': 111400}},
                                # Ajoutez d'autres événements de décès pour tester
                            ]
                        }
                    }
                }
            }
        }
    }

    result = highlight_death_from_personal_ability(datas)
    print(f"Player who died from his own spell: {result['playerName']} with BURNING_RUSH")
