"""
COMP 163 - Project 3: Quest Chronicles
Character Manager Module - Starter Code

Name: Madison Wilkins

AI Usage: assisted with making sure this file matches up with gamqe_data.py, assisted in writing code as well.

This module handles character creation, loading, and saving.
"""

import os

from custom_exceptions import (
    InvalidCharacterClassError,
    CharacterNotFoundError,
    SaveFileCorruptedError,
    InvalidSaveDataError,
    CharacterDeadError,
    InvalidDataFormatError
)


# ============================================================================
# CHARACTER MANAGEMENT FUNCTIONS
# ============================================================================

def create_character(name, character_class):

    valid = {
        "Warrior": {"health": 120, "max_health": 120, "strength": 15, "magic": 5},
        "Mage": {"health": 80, "max_health": 80, "strength": 5, "magic": 20},
        "Rogue": {"health": 100, "max_health": 100, "strength": 10, "magic": 10},
        "Cleric": {"health": 90, "max_health": 90, "strength": 7, "magic": 15}
    }
    if character_class not in valid:
        raise InvalidCharacterClassError
    stats = valid[character_class]
    return {
        "name": name,
        "class": character_class,
        "level": 1,
        "health": stats["health"],
        "max_health": stats["max_health"],
        "strength": stats["strength"],
        "magic": stats["magic"],
        "experience": 0,
        "gold": 100,
        "inventory": [],
        "active_quests": [],
        "completed_quests": [],
        "equipped_weapon": None,
        "equipped_armor": None,
    }
    

def save_character(character, save_directory="data/save_games"):
    # ok so boom we making sure the directory exist

    os.makedirs(save_directory, exist_ok=True)
    filename = f"{character['name']}_save.txt"
    filepath = os.path.join(save_directory, filename)
    inventory = ",".join(character['inventory'])
    active_quests = ",".join(character['active_quests'])
    completed_quests = ",".join(character['completed_quests'])

    if character['equipped_armor'] is None:
        equipped_armor = ''
    else:
        equipped_armor = character['equipped_armor']

    # ok so boom we writing the file now
    try:
        with open(filepath, "w") as f:

            f.write(f"NAME: {character['name']}\n")
            f.write(f"CLASS: {character['class']}\n")
            f.write(f"LEVEL: {character['level']}\n")
            f.write(f"EXPERIENCE: {character['experience']}\n")
            f.write(f"HEALTH: {character['health']}\n")
            f.write(f"MAX_HEALTH: {character['max_health']}\n")
            f.write(f"STRENGTH: {character['strength']}\n")
            f.write(f"MAGIC: {character['magic']}\n")
            f.write(f"GOLD: {character['gold']}\n")
            f.write(f"INVENTORY: {inventory}\n")
            f.write(f"ACTIVE_QUESTS: {active_quests}\n")
            f.write(f"COMPLETED_QUESTS: {completed_quests}\n")
            weapon = character['equipped_weapon'] if character['equipped_weapon'] else ''
            f.write(f"EQUIPPED_WEAPON: {weapon}\n")
            f.write(f"EQUIPPED_ARMOR: {equipped_armor}\n")
        return True
    # ok so boom hoe we catching errors
    except (IOError, PermissionError) as meowy:
        raise PermissionError(f"Failed to save character file: {meowy}")
        return False

def load_character(character_name, save_directory="data/save_games"):
    # boom we taking that file and making the filepath
    filename = f"{character_name}_save.txt"
    filepath = os.path.join(save_directory, filename)

    # im not explaining this again i done did it twice bro

    if not os.path.exists(filepath):
        raise CharacterNotFoundError(f"{character_name} not found.")
    
    try:
        with open(filepath, "r") as file:
            lines = file.readlines()
    except:
        raise SaveFileCorruptedError(f"{character_name}'s file is corrupted.")
    
    character = {}

    for line in lines:
        line = line.strip()  
        if not line: 
            continue
        if ":" not in line: 
            raise InvalidSaveDataError(f"Invalid data format in {character_name}'s file.")
        
        parts = line.split(": ", 1)
        if len(parts) == 1:  
            parts = line.split(":", 1)
        if len(parts) != 2:
            raise InvalidSaveDataError(f"Invalid data format in {character_name}'s file.")
        
        key = parts[0]
        value = parts[1].strip() 
        character[key] = value

    inventory = (
        character["INVENTORY"].split(",") if character["INVENTORY"].strip() else []
    )

    active_quests = (
        character["ACTIVE_QUESTS"].split(",") if character["ACTIVE_QUESTS"].strip() else []
    )

    completed_quests = (
        character["COMPLETED_QUESTS"].split(",") if character["COMPLETED_QUESTS"].strip() else []
    )

    
    if "EQUIPPED_WEAPON" in character:
        if character["EQUIPPED_WEAPON"]:
            equipped_weapon = character["EQUIPPED_WEAPON"]
        else:
            equipped_weapon = None
    else:
        equipped_weapon = None

    if "EQUIPPED_ARMOR" in character and character["EQUIPPED_ARMOR"].strip():
        equipped_armor = character["EQUIPPED_ARMOR"]
    else:
        equipped_armor = None

    # JUST TAKE YOUR CHARACTER BRUH
    character_dict = {
        "name": character["NAME"],
        "class": character["CLASS"],
        "level": int(character["LEVEL"]),
        "health": int(character["HEALTH"]),
        "max_health": int(character["MAX_HEALTH"]),
        "strength": int(character["STRENGTH"]),
        "magic": int(character["MAGIC"]),
        "experience": int(character["EXPERIENCE"]),
        "gold": int(character["GOLD"]),
        "inventory": inventory,
        "active_quests": active_quests,
        "completed_quests": completed_quests,
        "equipped_weapon": equipped_weapon,
        "equipped_armor": equipped_armor
    }
    return character_dict

def list_saved_characters(save_directory="data/save_games"):
   # grabbing dem character names and LINNNINGG em up

    if not os.path.exists(save_directory):
        return []
    files = os.listdir(save_directory)
    character_names = []
    for file in files:
        if file.endswith("_save.txt"):
            character_name = file[:-9] 
            character_names.append(character_name)
    return character_names

def delete_character(character_name, save_directory="data/save_games"):
    # umm. boom ? the same thing again but we go bye bye file

    filename = f"{character_name}_save.txt"
    filepath = os.path.join(save_directory, filename)
    if not os.path.exists(filepath):
        raise CharacterNotFoundError(f"{character_name} not found.")
    os.remove(filepath)

    return True
# ============================================================================
# CHARACTER OPERATIONS
# ============================================================================

def gain_experience(character, xp_amount):
    if character['health'] <= 0:
        raise CharacterDeadError(f"Character '{character['name']}' is DEAD. ")
    level_up_xp = character['level'] * 100
    character['experience'] += xp_amount

    #handles extra xp
    while character['experience'] >= level_up_xp:
        character['experience'] -= level_up_xp
        character['level'] += 1
        character['max_health'] += 10
        character['strength'] += 2
        character['magic'] += 2
        character['health'] = character['max_health']
        level_up_xp = character['level'] * 100

def add_gold(character, amount):

    character['gold'] += amount
    if character['gold'] < 0:
        raise ValueError("How poor can you possibly get?")
    return character['gold']

def heal_character(character, amount):
    preheal = character['health'] + amount
    if preheal > character['max_health']:
        healed = character['max_health'] - character['health']
        character['health'] = character['max_health']
    else:
        healed = amount
        character['health'] += amount

    return healed

def is_character_dead(character):
    if character['health'] <= 0:
        return True
    else:
        return False


def revive_character(character):
    if character['health'] <= 0:
        character['health'] = character['max_health'] // 2
        return True

# ============================================================================
# VALIDATION
# ============================================================================

def validate_character_data(character):
    valid_character = {
        "name": str,
        "class": str,
        "level": int,
        "health": int,
        "max_health": int,
        "strength": int,
        "magic": int,
        "experience": int,
        "gold": int,
        "inventory": list,
        "active_quests": list,
        "completed_quests": list,
        "equipped_weapon": (str, type(None)),
        "equipped_armor": (str, type(None))
    }

    for key, expected_type in valid_character.items():
        if key not in character:
            raise InvalidSaveDataError(f"Missing key: {key}")

        if not isinstance(character[key], expected_type):
            raise InvalidSaveDataError(f"Invalid type for {key}")

    return True

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== CHARACTER MANAGER TEST ===")
    
    # Test character creation
    # try:
    #     char = create_character("TestHero", "Warrior")
    #     print(f"Created: {char['name']} the {char['class']}")
    #     print(f"Stats: HP={char['health']}, STR={char['strength']}, MAG={char['magic']}")
    # except InvalidCharacterClassError as e:
    #     print(f"Invalid class: {e}")
    
    # Test saving
    # try:
    #     save_character(char)
    #     print("Character saved successfully")
    # except Exception as e:
    #     print(f"Save error: {e}")
    
    # Test loading
    # try:
    #     loaded = load_character("TestHero")
    #     print(f"Loaded: {loaded['name']}")
    # except CharacterNotFoundError:
    #     print("Character not found")
    # except SaveFileCorruptedError:
    #     print("Save file corrupted")

