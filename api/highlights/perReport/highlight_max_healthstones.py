# highlight_max_healthstones.py

def highlight_max_healthstones(events_data):
    most_potions_player = {'name': '', 'potionUse': 0}
    most_healthstones_player = {'name': '', 'healthstoneUse': 0}

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

    player_roles = ['dps', 'healers', 'tanks']
    for role in player_roles:
        players = events_data['data']['reportData']['report']['table']['data']['playerDetails'].get(role, [])
        analyze_players(players)

    if most_potions_player['name']:
        print(f"Le joueur ayant utilisé le plus de potions est {most_potions_player['name']} avec {most_potions_player['potionUse']} potions.")
    else:
        print("Aucun joueur n'a utilisé de potions.")

    if most_healthstones_player['name']:
        print(f"Le joueur ayant utilisé le plus de healthstones est {most_healthstones_player['name']} avec {most_healthstones_player['healthstoneUse']} healthstones.")
    else:
        print("Aucun joueur n'a utilisé de healthstones.")

    if not most_potions_player['name']:
        most_potions_player = None

    if not most_healthstones_player['name']:
        most_healthstones_player = None

    return most_potions_player, most_healthstones_player
