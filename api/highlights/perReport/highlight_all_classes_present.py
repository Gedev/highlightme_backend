from api.enums.character_classes import CharacterClass

def highlight_all_classes_present(events_data, global_info):
    """
    Highlight the group of players if all different classes are represented.
    """

    players = events_data['data']['reportData']['report']['table']['data']['playerDetails']['players']

    all_classes = {cls.value for cls in CharacterClass}

    present_classes = set()

    for player in players:
        player_class = player['class']
        present_classes.add(player_class)

    if all_classes.issubset(present_classes):
        highlight = {
            'highlight_type': 'all_classes_present',
            'description': 'All classes are represented in this raid.',
            'present_classes': list(present_classes),
            'missing_classes': [],
            'highlight_value': len(players),
            'rarity': 'Common',
            'img': 'all_classes.png'
        }
    else:
        missing_classes = all_classes - present_classes
        highlight = {
            'highlight_type': 'missing_classes',
            'description': f'The following classes are missing: {", ".join(missing_classes)}.',
            'present_classes': list(present_classes),
            'missing_classes': list(missing_classes),
            'highlight_value': len(players),
            'rarity': 'Uncommon',
            'img': 'missing_classes.png'
        }

    return highlight
