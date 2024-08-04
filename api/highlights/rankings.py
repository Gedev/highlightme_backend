# rankings.py
#
# Rank percent = Parse %
# Bracket percent = ilvl %
#
def display_player_parses(events_data):
    """
    Display bracket and rank percentages for each player in the rankings data.
    """
    rankings = events_data.get('data', {}).get('reportData', {}).get('report', {}).get('rankings', {}).get('data', [])

    if not rankings:
        print("No ranking data available.")
        return

    # Iterate over each fight in the rankings
    for fight in rankings:
        fight_id = fight.get('fightID')
        print(f"Fight ID: {fight_id}")

        roles = fight.get('roles', {})

        # Process each role type (tanks, healers, dps)
        for role_name, role_data in roles.items():
            print(f"Role: {role_name}")

            # Iterate over each character in the role
            for character in role_data.get('characters', []):
                name = character.get('name', 'Unknown')
                char_class = character.get('class', 'Unknown')
                spec = character.get('spec', 'Unknown')
                bracket_percent = character.get('bracketPercent', 'N/A')
                rank_percent = character.get('rankPercent', 'N/A')

                print(f"  Name: {name}, Class: {char_class}, Spec: {spec}")
                print(f"  Bracket Percent: {bracket_percent}%, Rank Percent: {rank_percent}%\n")


def calculate_best_parse_averages(events_data, fight_names):
    """
    Calculate and display the player with the best average parse in the raid
    and identify those with legendary parses (95% and above), including boss names.
    """
    # Access the ranking data
    rankings = events_data.get('data', {}).get('reportData', {}).get('report', {}).get('rankings', {}).get('data', [])

    # Check if rankings is empty
    if not rankings:
        print("No ranking data available.")
        return None

    # Dictionary to hold sum of rankPercents and count for each player
    player_stats = {}

    # List to hold players with legendary parses
    legendary_parses = []

    # Iterate over each fight in the rankings
    for fight in rankings:
        # Access roles
        roles = fight.get('roles', {})
        fight_id = fight.get('fightID')
        boss_name = fight_names.get(fight['encounter']['id'], "Unknown Boss")

        # Process each role type (tanks, healers, dps)
        for role_name, role_data in roles.items():
            # Iterate over each character in the role
            for character in role_data.get('characters', []):
                player_name = character.get('name', 'Unknown')
                rank_percent = character.get('rankPercent', 0)  # Default to 0 if not available
                bracket_percent = character.get('bracketPercent', 0)  # Default to 0 if not available

                # Initialize player entry if it doesn't exist
                if player_name not in player_stats:
                    player_stats[player_name] = {
                        'rank_percent_sum': 0,
                        'bracket_percent_sum': 0,
                        'count': 0
                    }

                # Update the player's stats
                player_stats[player_name]['rank_percent_sum'] += rank_percent
                player_stats[player_name]['bracket_percent_sum'] += bracket_percent
                player_stats[player_name]['count'] += 1

                # Check for legendary parse
                if rank_percent >= 95:
                    legendary_parses.append({
                        'name': player_name,
                        'rank_percent': rank_percent,
                        'role': role_name,
                        'class': character.get('class', 'Unknown'),
                        'spec': character.get('spec', 'Unknown'),
                        'boss_name': boss_name
                    })
                if bracket_percent >= 95:
                    legendary_parses.append({
                        'name': player_name,
                        'rank_percent': bracket_percent,
                        'role': role_name,
                        'class': character.get('class', 'Unknown'),
                        'spec': character.get('spec', 'Unknown'),
                        'boss_name': boss_name
                    })

    # Determine the player with the best average parse
    best_player = None
    best_average_rank_percent = 0

    for player_name, stats in player_stats.items():
        count = stats['count']
        avg_rank_percent = stats['rank_percent_sum'] / count if count > 0 else 0
        avg_bracket_percent = stats['bracket_percent_sum'] / count if count > 0 else 0

        # print(f"Player: {player_name}, Avg Rank Percent: {avg_rank_percent:.2f}, Avg Bracket Percent: {avg_bracket_percent:.2f}")

        # Check if this player has the best average rank percent
        if avg_rank_percent > best_average_rank_percent:
            best_average_rank_percent = avg_rank_percent
            best_player = {
                'name': player_name,
                'avg_rank_percent': avg_rank_percent,
                'avg_bracket_percent': avg_bracket_percent
            }

    # Display the best player information
    if best_player:
        print("\nBest Player:")
        print(f"  Name: {best_player['name']}")
        print(f"  Average Rank Percent: {best_player['avg_rank_percent']:.2f}%")
        print(f"  Average Bracket Percent: {best_player['avg_bracket_percent']:.2f}%")
    else:
        print("No player data available.")

    # Display legendary parses
    if legendary_parses:
        print("\nLegendary Parses (95% and above):")
        for parse in legendary_parses:
            print(f"  Name: {parse['name']}, Role: {parse['role']}, Class: {parse['class']}, Spec: {parse['spec']}, Rank Percent: {parse['rank_percent']}%, Boss: {parse['boss_name']}")
    else:
        print("No legendary parses found.")

    return best_player, legendary_parses



