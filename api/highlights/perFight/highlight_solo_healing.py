from api.utils.difficulties import DIFFICULTY_MAP


# 1 healer sur le raid
# Mais 1 report n'est pas forcément que dans 1 seule difficulté, il est donc important de séparer les difficultés.
# Mais si l'on sépare les difficultés, ['table']['data']['composition'] n'est plus fiable étant donné que cela comprends tous les joueurs du début à la fin

# Par fight : si 1 seul healer
#            1. Build une query des playerDetails pour chaque fight
# Par raid : 1. Spliter les données pour séparer les difficultés
#            2. Associer chaque joueur à son Id pour chaque fight de cette difficulté
#            3. Calculer le nombre de fight fait avec 1 healer pour attribuer la rareté du highlight

def highlight_solo_heal(events_data, global_info_data):
    fights = global_info_data['data']['reportData']['report']['fightsEncounters']
    highlights = []

    for fight in fights:
        difficulty_id = fight['difficulty']
        difficulty = DIFFICULTY_MAP.get(difficulty_id, "Unknown")
        if difficulty == "LFR":
            continue

        player_details = events_data['data']['reportData']['report'].get(f'playerDetails_{fight["id"]}', {}).get('data',
                                                                                                                 {}).get(
            'playerDetails', {})
        healers = player_details.get('healers', [])

        if len(healers) == 1 and healers[0].get('name'):
            rarity = "Common"
            if difficulty == 'Normal':
                rarity = "Bronze"
            elif difficulty == 'Heroic':
                rarity = "Argent"
            elif difficulty == 'Mythic':
                rarity = "Légendaire"

            highlights.append({
                "player": healers[0]['name'],
                "difficulty": difficulty,
                "fight_id": fight['id'],
                "rarity": rarity,
                "description": f"{healers[0]['name']} was the solo healer in a {difficulty} difficulty fight",
                "img": "solo_heal.png"
            })

    return highlights if highlights else None
