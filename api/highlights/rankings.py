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
    Additionally, highlight any player achieving 99% in their primary role.
    """
    # Access the ranking data
    dpsRankings = events_data.get('data', {}).get('reportData', {}).get('report', {}).get('dpsRankings', {}).get('data', [])
    hpsRankings = events_data.get('data', {}).get('reportData', {}).get('report', {}).get('hpsRankings', {}).get('data', [])

    # Check if rankings are empty
    if not dpsRankings and not hpsRankings:
        print("No ranking data available.")
        return None, None, [], []

    # Dictionary to hold sum of rankPercents and count for each player
    player_stats = {}

    # Lists to hold players with legendary parses and fight highlights
    legendary_parses = []
    fight_highlights = []

    # Process DPS Rankings
    for fight in dpsRankings:
        # Access roles
        roles = fight.get('roles', {})
        fight_id = fight.get('fightID')
        boss_name = fight_names.get(fight['encounter']['id'], "Unknown Boss")

        # Iterate through each role and collect legendary parses
        for role_name, role_data in roles.items():
            for character in role_data.get('characters', []):
                player_name = character.get('name', 'Unknown')
                rank_percent = character.get('rankPercent', 0)  # Default to 0 if not available
                bracket_percent = character.get('bracketPercent', 0)  # Default to 0 if not available

                # Initialize player entry if it doesn't exist
                if player_name not in player_stats:
                    player_stats[player_name] = {
                        'dps_rank_percent_sum': 0,
                        'dps_bracket_percent_sum': 0,
                        'hps_rank_percent_sum': 0,
                        'hps_bracket_percent_sum': 0,
                        'dps_count': 0,
                        'hps_count': 0,
                        'total_legendary_parses': 0,
                        'best_legendary_parse': 0
                    }

                # Update the player's stats for DPS
                player_stats[player_name]['dps_rank_percent_sum'] += rank_percent
                player_stats[player_name]['dps_bracket_percent_sum'] += bracket_percent
                player_stats[player_name]['dps_count'] += 1

                # Collect legendary parses
                if rank_percent >= 95:
                    legendary_parses.append({
                        'name': player_name,
                        'metric': 'dps',
                        'rank_percent': rank_percent,
                        'role': role_name,
                        'class': character.get('class', 'Unknown'),
                        'spec': character.get('spec', 'Unknown'),
                        'boss_name': boss_name
                    })
                    # Update total and best legendary parse
                    player_stats[player_name]['total_legendary_parses'] += 1
                    player_stats[player_name]['best_legendary_parse'] = max(player_stats[player_name]['best_legendary_parse'], rank_percent)

                if bracket_percent >= 95:
                    legendary_parses.append({
                        'name': player_name,
                        'metric': 'dps',
                        'rank_percent': bracket_percent,
                        'role': role_name,
                        'class': character.get('class', 'Unknown'),
                        'spec': character.get('spec', 'Unknown'),
                        'boss_name': boss_name
                    })
                    # Update total and best legendary parse
                    player_stats[player_name]['total_legendary_parses'] += 1
                    player_stats[player_name]['best_legendary_parse'] = max(player_stats[player_name]['best_legendary_parse'], bracket_percent)

                # Highlight if a DPS character achieves 99% in DPS
                if role_name == 'dps' and rank_percent == 99:
                    fight_highlights.append({
                        'name': player_name,
                        'metric': 'dps',
                        'rank_percent': rank_percent,
                        'role': role_name,
                        'class': character.get('class', 'Unknown'),
                        'spec': character.get('spec', 'Unknown'),
                        'boss_name': boss_name,
                        'highlight': '99% DPS Performance'
                    })

    # Process HPS Rankings
    for fight in hpsRankings:
        # Access roles
        roles = fight.get('roles', {})
        fight_id = fight.get('fightID')
        boss_name = fight_names.get(fight['encounter']['id'], "Unknown Boss")

        # Iterate through each role and collect legendary parses
        for role_name, role_data in roles.items():
            for character in role_data.get('characters', []):
                player_name = character.get('name', 'Unknown')
                rank_percent = character.get('rankPercent', 0)  # Default to 0 if not available
                bracket_percent = character.get('bracketPercent', 0)  # Default to 0 if not available

                # Initialize player entry if it doesn't exist
                if player_name not in player_stats:
                    player_stats[player_name] = {
                        'dps_rank_percent_sum': 0,
                        'dps_bracket_percent_sum': 0,
                        'hps_rank_percent_sum': 0,
                        'hps_bracket_percent_sum': 0,
                        'dps_count': 0,
                        'hps_count': 0,
                        'total_legendary_parses': 0,
                        'best_legendary_parse': 0
                    }

                # Update the player's stats for HPS
                player_stats[player_name]['hps_rank_percent_sum'] += rank_percent
                player_stats[player_name]['hps_bracket_percent_sum'] += bracket_percent
                player_stats[player_name]['hps_count'] += 1

                # Collect legendary parses
                if rank_percent >= 95:
                    legendary_parses.append({
                        'name': player_name,
                        'metric': 'hps',
                        'rank_percent': rank_percent,
                        'role': role_name,
                        'class': character.get('class', 'Unknown'),
                        'spec': character.get('spec', 'Unknown'),
                        'boss_name': boss_name
                    })
                    # Update total and best legendary parse
                    player_stats[player_name]['total_legendary_parses'] += 1
                    player_stats[player_name]['best_legendary_parse'] = max(player_stats[player_name]['best_legendary_parse'], rank_percent)

                if bracket_percent >= 95:
                    legendary_parses.append({
                        'name': player_name,
                        'metric': 'hps',
                        'rank_percent': bracket_percent,
                        'role': role_name,
                        'class': character.get('class', 'Unknown'),
                        'spec': character.get('spec', 'Unknown'),
                        'boss_name': boss_name
                    })
                    # Update total and best legendary parse
                    player_stats[player_name]['total_legendary_parses'] += 1
                    player_stats[player_name]['best_legendary_parse'] = max(player_stats[player_name]['best_legendary_parse'], bracket_percent)

                # Highlight if a Healer character achieves 99% in HPS
                if role_name == 'healers' and rank_percent == 99:
                    fight_highlights.append({
                        'name': player_name,
                        'metric': 'hps',
                        'rank_percent': rank_percent,
                        'role': role_name,
                        'class': character.get('class', 'Unknown'),
                        'spec': character.get('spec', 'Unknown'),
                        'boss_name': boss_name,
                        'highlight': '99% HPS Performance'
                    })

    # Determine the player with the best average DPS parse
    best_dps_player = None
    best_dps_average_rank_percent = 0

    for player_name, stats in player_stats.items():
        dps_count = stats['dps_count']
        avg_dps_rank_percent = stats['dps_rank_percent_sum'] / dps_count if dps_count > 0 else 0

        # Check if this player has the best average DPS rank percent
        if avg_dps_rank_percent > best_dps_average_rank_percent:
            best_dps_average_rank_percent = avg_dps_rank_percent
            best_dps_player = {
                'name': player_name,
                'avg_rank_percent': avg_dps_rank_percent
            }

    # Determine the player with the best average HPS parse
    best_hps_player = None
    best_hps_average_rank_percent = 0

    for player_name, stats in player_stats.items():
        hps_count = stats['hps_count']
        avg_hps_rank_percent = stats['hps_rank_percent_sum'] / hps_count if hps_count > 0 else 0

        # Check if this player has the best average HPS rank percent
        if avg_hps_rank_percent > best_hps_average_rank_percent:
            best_hps_average_rank_percent = avg_hps_rank_percent
            best_hps_player = {
                'name': player_name,
                'avg_rank_percent': avg_hps_rank_percent
            }

    # Display the best player DPS PARSES information
    if best_dps_player:
        print("\nBest DPS Player:")
        print(f"  Name: {best_dps_player['name']}")
        print(f"  Average Rank Percent: {best_dps_player['avg_rank_percent']:.2f}%")
    else:
        print("No player DPS data available.")

    # Display the best player HPS PARSES information
    if best_hps_player:
        print("\nBest HPS Player:")
        print(f"  Name: {best_hps_player['name']}")
        print(f"  Average Rank Percent: {best_hps_player['avg_rank_percent']:.2f}%")
    else:
        print("No player HPS data available.")

    # Display legendary parses summary
    print("\nLegendary Parses Summary:")
    for player_name, stats in player_stats.items():
        if stats['total_legendary_parses'] > 0:
            print(f"  Name: {player_name}, Total Legendary Parses: {stats['total_legendary_parses']}, Best Legendary Parse: {stats['best_legendary_parse']}%")

    # Display fight highlights for 99% achievements
    if fight_highlights:
        print("\nFight Highlights (99% Performance):")
        for highlight in fight_highlights:
            print(f"  Name: {highlight['name']}, Metric: {highlight['metric']}, Role: {highlight['role']}, Class: {highlight['class']}, Spec: {highlight['spec']}, Rank Percent: {highlight['rank_percent']}%, Boss: {highlight['boss_name']}, Highlight: {highlight['highlight']}")
    else:
        print("No fight highlights found.")

    return best_dps_player, best_hps_player, legendary_parses, fight_highlights





