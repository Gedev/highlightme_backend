DIFFICULTY_MAP = {
    1: "LFR",
    2: "Flex",
    3: "Normal",
    4: "Heroic",
    5: "Mythic"
}


def get_difficulty_name(difficulty_value):
    return DIFFICULTY_MAP.get(difficulty_value, "Unknown Difficulty")
