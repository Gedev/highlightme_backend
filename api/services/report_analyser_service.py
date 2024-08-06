# api/services/report_analysis.py
from collections import defaultdict
from api.utils.difficulties import DIFFICULTY_MAP

def analyze_report(fights):
    """
    Analyze the fights in a report, grouping them by difficulty.

    Args:
    - fights (list): A list of dictionaries containing information about each fight.

    Returns:
    - grouped_fights (dict): A dictionary where keys are difficulty names and values are lists of fights.
    """
    # Dictionary to group fights by difficulty
    grouped_fights = defaultdict(list)

    # Iterate through each fight and organize them by difficulty
    for fight in fights:
        difficulty = fight.get('difficulty')
        encounter_id = fight.get('encounterID')

        # Map the difficulty using the DIFFICULTY_MAP
        difficulty_name = DIFFICULTY_MAP.get(difficulty, 'Unknown Difficulty')

        # Append fight details to the corresponding difficulty group
        fight['boss_name'] = encounter_id  # Store ID for now, replace with names later
        grouped_fights[difficulty_name].append(fight)

    # Print the summary for debugging purposes
    for difficulty_name, fights in grouped_fights.items():
        encounter_names = ', '.join(set(str(fight['boss_name']) for fight in fights))
        print(f"{difficulty_name} avec {len(fights)} combats : {encounter_names}")

    return grouped_fights
