def highlight_less_trash_damage(events_data):
    # Identifier les healers
    healers = {healer['name'] for healer in events_data['data']['reportData']['report']['table']['data']['playerDetails']['healers']}

    # Initialiser les variables pour trouver le joueur avec le total le plus bas parmi les non-healers
    min_total = float('inf')
    min_player = None

    # Parcourir les entrées pour trouver le joueur avec le total le plus bas parmi les non-healers
    for entry in events_data['data']['reportData']['report']['table']['data']['damageDone']:
        if entry['name'] not in healers:
            if entry['total'] < min_total:
                min_total = entry['total']
                min_player = entry['name']

    print(f"Le joueur non-healer ayant fait le moins de dégâts est {min_player} avec un total de {min_total} dégâts.")
    return min_player, min_total