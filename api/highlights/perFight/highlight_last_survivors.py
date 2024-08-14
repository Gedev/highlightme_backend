# api/highlights/perFight/highlight_last_survivors.py
from collections import Counter

def highlight_last_survivors(events_data, global_info):
    """
    Highlight the number of players alive at the end of the fight.
    """
    # Extract the cast events from the data
    death_events = events_data['data']['reportData']['report']['table']['data']['deathEvents']
    casts = events_data['data']['reportData']['report']['table']['data']['entries']

    # List of resurrection spell IDs (these should be the correct IDs from the game)
    resurrection_spells = {
        2006: "Resurrection",  # Priest

        61999: "Raise Ally",  # Death Knight
        20707: "Soulstone",  # Warlock
        2008: "Ancestral Spirit",  # Shaman

        391054: "Intercession",  # Paladin
        20484: "Rebirth",  # Druid
        21169: "Reincarnation",  # Shaman
    }



    return None  # Return None if no highlight is applicable