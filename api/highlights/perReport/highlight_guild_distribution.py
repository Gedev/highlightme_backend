# api/highlights/perReport/highlight_guild_distribution.py
from collections import Counter

def highlight_guild_distribution(events_data, global_info_data):
    """
    Highlight the distribution of players by guilds in the raid.
    """

    # Extract guild names from the ranked characters
    ranked_characters = global_info_data['data']['reportData']['report']['rankedCharacters']
    guild_counts = Counter()

    for character in ranked_characters:
        if character['guilds']:
            guild_name = character['guilds'][0]['name']
            guild_counts[guild_name] += 1

    if not guild_counts:
        return None

    total_players = len(ranked_characters)
    most_common_guild, most_common_count = guild_counts.most_common(1)[0]
    others_count = total_players - most_common_count

    if others_count == 1:
        return {
            'highlight_type': 'adopted_guild',
            'description': f"Tous les joueurs sauf un sont dans la guilde {most_common_guild}.",
            'guilds': [most_common_guild],
            'highlight_value': most_common_count,
            'rarity': 'Legendary',
            'img': 'adopted_guild.png'
        }

    elif others_count == 2:
        return {
            'highlight_type': 'job_interview_guild',
            'description': f"Tous les joueurs sauf deux sont dans la guilde {most_common_guild}.",
            'guilds': [most_common_guild],
            'highlight_value': most_common_count,
            'rarity': 'Epic',
            'img': 'job_interview_guild.png'
        }

    return None
