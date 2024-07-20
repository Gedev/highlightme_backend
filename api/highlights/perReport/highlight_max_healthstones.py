def highlight_max_healthstones(events_data):
    # Initialiser les variables pour suivre les joueurs
    most_potions_player = {'name': '', 'potionUse': 0}
    most_healthstones_player = {'name': '', 'healthstoneUse': 0}

    # Fonction pour analyser les joueurs dans une liste spécifique
    def analyze_players(players):
        nonlocal most_potions_player, most_healthstones_player
        for player in players:
            name = player.get('name', '')
            potion_use = player.get('potionUse', 0)
            healthstone_use = player.get('healthstoneUse', 0)

            if potion_use > most_potions_player['potionUse']:
                most_potions_player['name'] = name
                most_potions_player['potionUse'] = potion_use

            if healthstone_use > most_healthstones_player['healthstoneUse']:
                most_healthstones_player['name'] = name
                most_healthstones_player['healthstoneUse'] = healthstone_use

    # Parcourir les listes "dps", "healers" et "tanks"
    player_roles = ['dps', 'healers', 'tanks']
    for role in player_roles:
        players = events_data['data']['reportData']['report']['table']['data']['playerDetails'].get(role, [])
        analyze_players(players)

    # Afficher les résultats
    print(f"Le joueur ayant utilisé le plus de potions est {most_potions_player['name']} avec {most_potions_player['potionUse']} potions.")
    print(f"Le joueur ayant utilisé le plus de healthstones est {most_healthstones_player['name']} avec {most_healthstones_player['healthstoneUse']} healthstones.")
    return most_potions_player, most_healthstones_player
