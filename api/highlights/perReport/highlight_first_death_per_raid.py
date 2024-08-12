from collections import defaultdict

def highlight_first_death_per_raid(events_data, global_info_data):
    fights = global_info_data['data']['reportData']['report']['fightsEncounters']
    death_events = events_data['data']['reportData']['report']['deathEvents']['data'] #TODO : use events instead of deathEvents
    composition = events_data['data']['reportData']['report']['table']['data']['composition']

    # Mapper les IDs des joueurs aux noms
    target_id_to_name = {player['id']: player['name'] for player in composition}

    first_death_counts = defaultdict(int)
    total_fights = len(fights)

    for fight in fights:
        fight_id = fight['id']
        fight_start_time = fight['startTime']
        fight_end_time = fight['endTime']

        # Filtrer les événements pour ce combat
        fight_deaths = [
            event for event in death_events
            if event['type'] == 'death' and fight_start_time <= event['timestamp'] <= fight_end_time
        ]

        # Trouver le premier mort
        if fight_deaths:
            first_death_event = min(fight_deaths, key=lambda x: x['timestamp'])
            first_dead_player = target_id_to_name.get(first_death_event['targetID'], "Unknown")
            first_death_counts[first_dead_player] += 1

    # Trouver le joueur avec le pourcentage le plus élevé de premières morts
    top_player = None
    top_percentage = 0

    for player, count in first_death_counts.items():
        percentage = (count / total_fights) * 100
        if percentage >= 70 and percentage > top_percentage:
            top_player = player
            top_percentage = percentage

    if top_player:
        rarity = "Common"
        if top_percentage == 100:
            rarity = "Argent"
        elif top_percentage >= 80:
            rarity = "Bronze"

        highlight = {
            "player": top_player,
            "firstDeathCount": first_death_counts[top_player],
            "totalFights": total_fights,
            "percentage": top_percentage,
            "highlight_value": top_percentage,
            "rarity": rarity,
            "description": f"{top_player} died first in {first_death_counts[top_player]} out of {total_fights} fights ({top_percentage:.2f}%)",
            "img": "Gnomish-grave-digger.jpg"
        }

        return highlight
    else:
        return {}
