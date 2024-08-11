def highlight_pull_before_tanks(events_data, global_info_data):
    fights = global_info_data['data']['reportData']['report']['fightsEncounters']
    players = events_data['data']['reportData']['report']['table']['data']['composition']

    # Create a dictionary to map sourceID to player names
    id_to_name = {player['id']: player['name'] for player in players}
    tanks = {player['id'] for player in players if any(spec['role'] == 'tank' for spec in player['specs'])}

    # Dictionary to count the number of pulls for each player
    pull_counts = {}

    # Iterate over event sections (event_1, event_2, etc.)
    for i, fight in enumerate(fights, start=1):
        fight_id = fight['id']
        event_key = f'event_{i}'
        if event_key in events_data['data']['reportData']['report']:
            fight_events = events_data['data']['reportData']['report'][event_key]['data']
            damage_events = [event for event in fight_events if event['type'] == 'damage']

            if damage_events:
                first_damage_event = min(damage_events, key=lambda e: e['timestamp'])
                source_id = first_damage_event['sourceID']

                # Check if the player is not a tank
                if source_id not in tanks:
                    if source_id not in pull_counts:
                        pull_counts[source_id] = 0
                    pull_counts[source_id] += 1

    # Find the player who pulled the most times before the tanks
    if pull_counts:
        max_pulls_player = max(pull_counts, key=pull_counts.get)
        max_pulls_count = pull_counts[max_pulls_player]
        max_pulls_name = id_to_name.get(max_pulls_player, "Unknown")
    else:
        max_pulls_player = None
        max_pulls_count = 0
        max_pulls_name = "Unknown"

    if max_pulls_player is not None and max_pulls_name != "Unknown":
        return {
            "playerID": max_pulls_player,
            "playerName": max_pulls_name,
            "pullCount": max_pulls_count,
            "description": f"{max_pulls_name} pulled before the tanks the most with {max_pulls_count} pulls",
            "img": "Gnomish-grave-digger.jpg",
            "highlight_value": max_pulls_count
        }
    else:
        return None
