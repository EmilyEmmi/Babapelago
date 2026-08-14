# Words that are auto-unlocked when using the "start with default words" option
DEFAULT_WORDS = ("Baba", "Is", "You", "Flag", "Win", "Wall", "Stop", "Rock", "Push")

# List of words that appear prior to ???
EARLY_WORDS = ("Sink", "Skull", "Defeat", "Lava", "And",
                    "Star", "Crab", "Keke", "Love", "Move",
                    "Pillar", "Jelly", "Key", "Open", "Door",
                    "Shut", "Hedge", "Belt", "Shift", "End",
                    "Rose", "Red", "Violet", "Blue", "Water",
                    "Float", "Text", "Robot", "Bolt", "Hot",
                    "Cog", "Weak", "Has", "Box", "Melt",
                    "Ghost", "Tele", "Pull", "Ice", "Leaf",
                    "Fence", "Not", "Me", "Tree", "Up",
                    "Right", "Bug", "Fungus", "Swap", "Empty",
                    "Cloud", "Anni", "Best", "Rocket", "UFO",
                    "Moon", "Fall", "Dust", "On", "Grass",
                    "Make", "Hand", "Fruit", "All", "More",
                    "Word", "Sleep", "Cliff", "Bat", "Group",
                    "Fire", "Facing", "Lonely", "Bird", "Sun",
                    "Tile")

# List of words past the top gate and prior to ???
TOP_GATE_WORDS = ("Level", "Orb", "Hide", "Bonus")

# List of words that first appear in ??? + ABC
FLOWER_WORDS = ("Write", "A", "AB", "B", "BA", "C", "E", "G", "H", "L", "M", "N", "O", "R", "S", "T", "V", "W")

# List of words that first appear in Depths
DEPTHS_WORDS = ("Down", "Left")

# List of words in Meta
META_WORDS = ("Near", "Cursor", "I")

# List of words in Center (The End and Gallery only)
CENTER_WORDS = ("Cake", "Done", "Image", "F", "U", "X")

# Words that are always filler
FILLER_WORDS = ("Anni", "Best", "Down", "Left", "Hedge", "Cliff", "Line")

# Every single word, including both progression and filler
ALL_WORDS = (DEFAULT_WORDS + EARLY_WORDS + TOP_GATE_WORDS + FLOWER_WORDS + DEPTHS_WORDS + META_WORDS + CENTER_WORDS)

# All progression words
ALL_PROG_WORDS = tuple(set(ALL_WORDS) - set(FILLER_WORDS))

# Function to get the available words given the area access
def get_active_words(world):
    curr_words = DEFAULT_WORDS + EARLY_WORDS
    area_access = world.options.area_access
    if area_access < 4 and world.options.level_shuffle == 2:
        area_access = 4 # The End and Gallery don't shuffle, so they could still be filler

    if area_access >= 1:
        curr_words += TOP_GATE_WORDS
    if area_access >= 2:
        curr_words += FLOWER_WORDS
    if area_access >= 3:
        curr_words += DEPTHS_WORDS
    if area_access >= 4:
        curr_words += META_WORDS
    if area_access >= 5:
        curr_words += CENTER_WORDS
    return curr_words