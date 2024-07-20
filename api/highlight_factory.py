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

# api/highlight_factory.py


def create_highlights(events_data, global_info_data):
    # Generate highlights
    min_player, min_total = highlight_less_trash_damage(events_data)
    most_potions_player, most_healthstones_player = highlight_max_healthstones(events_data)

    # Générer les highlights pour "pull avant le tank"
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

    # Return the highlights
    highlights = {
        "less_trash_damage": {
            "player": min_player,
            "total": min_total,
            "description": "Less Trash Damage",
            "img": "less_damage_trash.png"
        },
        "max_healthstones": {
            "player": most_healthstones_player['name'],
            "healthstoneUse": most_healthstones_player['healthstoneUse'],
            "description": "Max Health stones used",
            "img": "elf-drinking.jpg"
        },
        "max_potions": {
            "player": most_potions_player['name'],
            "potionUse": most_potions_player['potionUse'],
            "description": "Max Potions",
            "img": "elf_drinking_potion.png"
        },
        "pull_before_tanks":
        {
            "player": pull_before_tanks_highlights["playerName"],
            "fight": pull_before_tanks_highlights["pullCount"],
            "sourceID": pull_before_tanks_highlights["playerID"],
            "description": "Player pulled before tank the most",
            "img": "Gnomish-grave-digger.jpg"
        },
        "max_deaths":
        {
            "player": most_deaths_player_highlight["playerName"],
            "deathCount": most_deaths_player_highlight["deathCount"],
            "description": most_deaths_player_highlight["description"],
            "img": "Gnomish-grave-digger.jpg"
        }
    }

    # Ajouter le highlight "special death" si des joueurs sont morts de lave
    if lava_death_highlight["lavaDeathCount"] > 0:
        highlights["lava_death"] = {
            "player": lava_death_highlight["playerName"],
            "deathCount": lava_death_highlight["lavaDeathCount"],
            "description": lava_death_highlight["description"],
            "img": "lava_death.png"
        }
    else:
        print("No lava death")

    # Ajouter le highlight "potion death" si des joueurs sont morts de potion
    if potion_death_highlight["potionDeathCount"] > 0:
        highlights["potion_death"] = {
            "player": potion_death_highlight["playerName"],
            "deathCount": potion_death_highlight["potionDeathCount"],
            "description": potion_death_highlight["description"],
            "img": "potion_death.png"
        }
    else:
        print("No potion death")

    # Ajouter les highlights des morts par combat
    for key, death_highlights in death_counts_highlights.items():
        if death_highlights:
            highlights[key] = death_highlights

    if first_death_highlights:
        highlights["first_death"] = first_death_highlights
    else:
        print("No first death highlight")

    if solo_tanking_highlight:
        highlights["solo_tanking"] = solo_tanking_highlight
    else:
        print("No solo tanking highlight")

    # Add new highlights
    if solo_heal_highlight:
        highlights["solo_healing"] = solo_heal_highlight
    else:
        print("No solo healing highlight")


    print("=== HIGLIGHTS === \n", highlights)
    return highlights

