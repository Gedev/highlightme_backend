def highlight_same_race_players(events_data):
    players = events_data['data']['reportData']['report']['table']['data']['composition']

    total_players = len(players)

    race_groups = {}
    for player in players:
        race = player['race']
        name = player['name']
        if race not in race_groups:
            race_groups[race] = []
        race_groups[race].append(name)

    # Trouver les races avec plus d'un joueur
    highlights = []
    for race, names in race_groups.items():
        if len(names) > 1:
            percentage = (len(names) / total_players) * 100
            rarity = determine_rarity(percentage)

            highlight = {
                'race': race,
                'players': names,
                'highlight_value': len(names),
                'percentage': round(percentage, 2),
                'rarity': rarity,
                'description': f"{len(names)} joueurs de race {race} ({round(percentage, 2)}% du raid) : {', '.join(names)}"
            }
            highlights.append(highlight)

    return highlights


def determine_rarity(percentage):
    if percentage >= 50:
        return "Légendaire"
    elif 30 <= percentage < 50:
        return "Épique"
    elif 15 <= percentage < 30:
        return "Rare"
    else:
        return "Commun"
