from api.highlights.perFight.highlight_death_counts_per_fight import highlight_death_counts_per_fight
from api.highlights.perFight.highlight_solo_healing import highlight_solo_heal
from api.highlights.perFight.highlight_solo_tanking import highlight_solo_tanking
from api.highlights.perReport.highlight_death_from_potion import highlight_potion_death
from api.highlights.perReport.highlight_died_the_most_times import highlight_died_the_most_times
from api.highlights.perReport.highlight_first_death_per_raid import highlight_first_death_per_raid
from api.highlights.perReport.highlight_less_trash_damage import highlight_less_trash_damage
from api.highlights.perReport.highlight_max_healthstones import highlight_max_healthstones
from api.highlights.perReport.highlight_pull_before_tanks import highlight_pull_before_tanks
from api.highlights.perReport.highlight_lava_death import highlight_lava_death
from api.highlights.perReport.highlight_same_race import highlight_same_race_players


# api/highlight_factory.py


def create_highlights(events_data, global_info_data):
    # Generate highlights
    min_player, min_total = highlight_less_trash_damage(events_data)
    most_potions_player, most_healthstones_player = highlight_max_healthstones(events_data)
    pull_before_tanks_highlights = highlight_pull_before_tanks(events_data, global_info_data)
    most_deaths_player_highlight = highlight_died_the_most_times(events_data)

    # Generate highlights for special deaths
    lava_death_highlight = highlight_lava_death(events_data)
    potion_death_highlight = highlight_potion_death(events_data)
    death_counts_highlights = highlight_death_counts_per_fight(events_data, global_info_data)
    first_death_highlights = highlight_first_death_per_raid(events_data, global_info_data)

    # Special Comp
    solo_heal_highlight = highlight_solo_heal(events_data, global_info_data)
    solo_tanking_highlight = highlight_solo_tanking(events_data, global_info_data)
    same_race_highlights = highlight_same_race_players(events_data)

    # Return the highlights
    highlights = {}

    if pull_before_tanks_highlights is not None:
        highlights["pull_before_tanks"] = {
            "player": pull_before_tanks_highlights["playerName"],
            "fight": pull_before_tanks_highlights["pullCount"],
            "sourceID": pull_before_tanks_highlights["playerID"],
            "description": "Player pulled before tank the most",
            "img": "Gnomish-grave-digger.jpg"
        }

    if highlight_less_trash_damage is not None:
        highlights["less_trash_damage"] = {
            "player": min_player,
            "highlight_value": min_total,
            "description": "Less Trash Damage",
            "img": "less_damage_trash.png"
        }
    else:
        print("No less trash damage")

    if most_deaths_player_highlight is not None:
        highlights["max_deaths"] = {
            "player": most_deaths_player_highlight["playerName"],
            "highlight_value": most_deaths_player_highlight["deathCount"],
            "description": most_deaths_player_highlight["description"],
            "img": "Gnomish-grave-digger.jpg"
        }
    else:
        print("No most deaths")

    if lava_death_highlight["lavaDeathCount"] > 0:
        highlights["lava_death"] = {
            "player": lava_death_highlight["playerName"],
            "highlight_value": lava_death_highlight["lavaDeathCount"],
            "description": lava_death_highlight["description"],
            "img": "lava_death.png"
        }
    else:
        print("No lava death")

    if potion_death_highlight["potionDeathCount"] > 0:
        highlights["potion_death"] = {
            "player": potion_death_highlight["playerName"],
            "highlight_value": potion_death_highlight["potionDeathCount"],
            "description": potion_death_highlight["description"],
            "img": "potion_death.png"
        }
    else:
        print("No potion death")

    if most_potions_player is not None:
        highlights['max_potions'] = {
            'player': most_potions_player['name'],
            'highlight_value': most_potions_player['potionUse'],
            'description': 'Max Potions',
            'img': 'elf_drinking_potion.png'
        }

    if most_healthstones_player is not None:
        highlights['max_healthstones'] = {
            'player': most_healthstones_player['name'],
            'highlight_value': most_healthstones_player['healthstoneUse'],
            'description': 'Max Health stones used',
            'img': 'elf-drinking.jpg'
        }

    # Ajouter les highlights des morts par combat
    for key, death_highlights in death_counts_highlights.items():
        if death_highlights:
            highlights[key] = death_highlights

    if first_death_highlights:
        highlights["first_death"] = first_death_highlights
    else:
        print("No first death highlight")

    if solo_tanking_highlight is not None:
        highlights["solo_tanking"] = solo_tanking_highlight
    else:
        print("No solo tanking highlight")

    if solo_heal_highlight is not None:
        highlights["solo_healing"] = solo_heal_highlight
    else:
        print("No solo healing highlight")

    for highlight in same_race_highlights:
        highlights[f"same_race_{highlight['race']}"] = {
            "players": highlight['players'],
            "highlight_value": highlight['highlight_value'],
            "description": highlight['description'],
            "img": "race_highlight.png"
        }

    print("=== HIGLIGHTS === \n", highlights)
    return highlights
