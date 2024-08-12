from collections import Counter


def highlight_class_distribution(events_data):
    """
    Highlight both homogeneous and non-homogeneous class distributions,
    with rarity based on the number of classes present and their distribution.
    """

    # Extract the composition of the players
    composition = events_data['data']['reportData']['report']['table']['data']['composition']
    print("Composition : ", composition)

    # Count the occurrence of each class in the raid
    class_counts = Counter(player['type'] for player in composition)

    values = list(class_counts.values())

    for value in values:
        if value != values[0]:
            return check_non_homogeneous_distribution(class_counts)

    total_players = len(composition)

    # Define the thresholds for different homogeneous distributions
    thresholds = {
        'half': total_players // 2,
        'third': total_players // 3,
        'quarter': total_players // 4,
        'quintile': total_players // 5
    }

    # Check for homogeneous distribution first
    for label, threshold in thresholds.items():
        matching_classes = [cls for cls, count in class_counts.items() if count == threshold]

        if len(matching_classes) > 6:
            rarity = 'Common'
        elif len(matching_classes) == 2 and label == 'half':
            rarity = 'Legendary'
        elif len(matching_classes) == 3 or len(matching_classes) == 4:
            rarity = 'Epic'
        elif len(matching_classes) == 5 or len(matching_classes) == 6:
            rarity = 'Rare'
        else:
            return None  # Add a default value for rarity to avoid uninitialized usage

        if len(matching_classes) > 1:
            return {
                'highlight_type': f'homogeneous_{label}_classes',
                'description': f"Classes are evenly distributed in {label}s: {', '.join(matching_classes)}",
                'classes': matching_classes,
                'highlight_value': len(matching_classes),
                'rarity': rarity,
                'img': f'{label}_classes.png'
            }

    # If no homogeneous distribution is found, check for non-homogeneous
    return check_non_homogeneous_distribution(class_counts)


def check_non_homogeneous_distribution(class_counts):
    """
    Check for non-homogeneous class distributions.
    """

    # Sort the class counts by the number of players in descending order
    sorted_class_counts = sorted(class_counts.items(), key=lambda x: x[1], reverse=True)

    total_classes = len(class_counts)
    rarity = 'Common'  # Initialize rarity with a default value
    if total_classes == 2:
        rarity = 'Legendary'
    elif total_classes == 3 or total_classes == 4:
        rarity = 'Epic'
    elif total_classes == 5 or total_classes == 6:
        rarity = 'Rare'
    else:
        return None

    # Create a description that includes all classes
    description_parts = [f"{count} {cls}" for cls, count in sorted_class_counts]
    description = " and ".join(description_parts)

    return {
        'highlight_type': 'non_homogeneous_class_distribution',
        'description': f"Non-homogeneous distribution: {description}.",
        'classes': [cls for cls, _ in sorted_class_counts],
        'highlight_value': total_classes,
        'rarity': rarity,
        'img': 'non_homogeneous_classes.png'
    }


# Usage example
if __name__ == "__main__":
    datas = {
        'data': {
            'reportData': {
                'report': {
                    'table': {
                        'data': {
                            'composition': [
                                {'name': 'Player1', 'type': 'Paladin'},
                                {'name': 'Player2', 'type': 'Paladin'},
                                {'name': 'Player3', 'type': 'Paladin'},
                                {'name': 'Player4', 'type': 'Paladin'},
                                {'name': 'Player5', 'type': 'Paladin'},
                                {'name': 'Player6', 'type': 'Paladin'},
                                {'name': 'Player7', 'type': 'Paladin'},
                                {'name': 'Player8', 'type': 'Paladin'},
                                {'name': 'Player9', 'type': 'Paladin'},
                                {'name': 'Player10', 'type': 'Paladin'},
                                {'name': 'Player11', 'type': 'Warrior'},
                                {'name': 'Player12', 'type': 'Warrior'},
                                {'name': 'Player13', 'type': 'Warrior'},
                                {'name': 'Player14', 'type': 'Warrior'},
                                {'name': 'Player15', 'type': 'Warrior'},
                                {'name': 'Player16', 'type': 'Warrior'},
                                {'name': 'Player17', 'type': 'Warrior'},
                                {'name': 'Player18', 'type': 'Warrior'},
                                {'name': 'Player19', 'type': 'Warrior'},
                                {'name': 'Player20', 'type': 'Warrior'}
                            ]
                        }
                    }
                }
            }
        }
    }

    highlight = highlight_class_distribution(datas)
    print(highlight)

