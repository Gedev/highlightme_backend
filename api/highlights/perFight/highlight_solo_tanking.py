from api.utils.difficulties import DIFFICULTY_MAP


def highlight_solo_tanking(events_data, global_info_data):
    fights = global_info_data['data']['reportData']['report']['fightsEncounters']
    highlights = []

    for fight in fights:
        difficulty_id = fight['difficulty']
        difficulty = DIFFICULTY_MAP.get(difficulty_id, "Unknown")
        if difficulty == "LFR":
            continue

        player_details = events_data['data']['reportData']['report'].get(f'playerDetails_{fight["id"]}', {}).get('data', {}).get('playerDetails', {})
        tanks = player_details.get('tanks', [])

        if len(tanks) == 1 and tanks[0].get('name'):
            rarity = "Common"
            if difficulty == 'Normal':
                rarity = "Bronze"
            elif difficulty == 'Heroic':
                rarity = "Argent"
            elif difficulty == 'Mythic':
                rarity = "Légendaire"

            highlights.append({
                "player": tanks[0]['name'],
                "difficulty": difficulty,
                "fight_id": fight['id'],
                "rarity": rarity,
                "description": f"{tanks[0]['name']} was the solo tank in a {difficulty} difficulty fight",
                "img": "solo_tank.png"
            })

    return highlights if highlights else None
