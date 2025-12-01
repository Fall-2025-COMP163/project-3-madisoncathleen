"""
COMP 163 - Project 3: Quest Chronicles
Game Data Module - Starter Code

Name: Madison Wilkins

AI Usage: [Document any AI assistance used]

This module handles loading and validating game data from text files.
"""

import os
from custom_exceptions import (
    InvalidDataFormatError,
    MissingDataFileError,
    CorruptedDataError
)

# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================

def load_quests(filename="data/quests.txt"):

    # ok BET so first we pulling up with the reading of the file.
    
    try:
        with open(filename, "r") as f:
            try:
                content = f.read()
            except Exception:
                raise CorruptedDataError("This file is unreadable or corrupted.")
    except FileNotFoundError:
        raise MissingDataFileError(f"File '{filename}' not found.")
    
    # BOOM we sptting the content into blocks by double newlines >_<
    
    meows = [meow.strip() for meow in content.split("\n\n") if meow.strip()]

    quests = {}

    required_fields = [
        "QUEST_ID", "TITLE", "DESCRIPTION",
        "REWARD_XP", "REWARD_GOLD", "REQUIRED_LEVEL",
        "PREREQUISITE"
    ]

    # and then we parsin' 

    for meow in meows:
        lines = meow.split("\n")
        quest_data = {}

        for line in lines:
            if ":" not in line:
                raise InvalidDataFormatError(f"Invalid line: {line}")

            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()

            quest_data[key] = value

        # makin sure all required fields valid and converted correctly yurrrp
        
        for req in required_fields:
            if req not in quest_data:
                raise InvalidDataFormatError(f"Missing field {req} in {meow}")
        try:
            reward_xp = int(quest_data["REWARD_XP"])
            reward_gold = int(quest_data["REWARD_GOLD"])
            required_level = int(quest_data["REQUIRED_LEVEL"])
        except ValueError:
            raise InvalidDataFormatError("XP, Gold, or Level field is invalid.")
        prerequisite = quest_data["PREREQUISITE"]
        # Build final quest dict entry
        quests[quest_data["QUEST_ID"]] = {
            "title": quest_data["TITLE"],
            "description": quest_data["DESCRIPTION"],
            "reward_xp": reward_xp,
            "reward_gold": reward_gold,
            "required_level": required_level,
            "prerequisite": prerequisite
        }

    return quests

def load_items(filename="data/items.txt"):
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        raise MissingDataFileError(f"Item file '{filename}' not found.")
    except Exception:
        raise CorruptedDataError(f"Item file '{filename}' is unreadable or corrupted.")
    
    item = {}
    now_meow = []
    # lookin through each line in the file yup yup
    for line in lines:
        stripped = line.strip()
        if stripped == "":
            if now_meow:
                item_dict = parse_item_block(now_meow)
                validate_item_data(item_dict)
                item[item_dict['item_id']] = item_dict
                now_meow = []
        else:
            now_meow.append(stripped)

    # goin through last block if therre is one

    if now_meow:
        item_dict = parse_item_block(now_meow)
        validate_item_data(item_dict)
        item[item_dict['item_id']] = item_dict

    return item

def validate_quest_data(quest_dict):
    neededmeows = [
        "quest_id",
        "title",
        "description",
        "reward_xp",
        "reward_gold",
        "required_level",
        "prerequisite"
    ]
    for meowz in neededmeows:
        if meowz not in quest_dict:
            raise InvalidDataFormatError(f"Missing field in {meowz}.")
        
    needednumericmeows = ["reward_xp", "reward_gold", "required_level"]

    for key in needednumericmeows:
        if not isinstance(quest_dict[key], int):
            raise InvalidDataFormatError(f"Field '{key}' must be an integer.")
    return True

def validate_item_data(item_dict):
    neededmeows = [
        "item_id",
        "name",
        "type",
        "effect",
        "cost",
        "description"
    ]
    for meowz in neededmeows:
        if meowz not in item_dict:
            raise InvalidDataFormatError(f"Missing field in {meowz}.")
    valid_types = {"weapon", "armor", "consumable"}

    if item_dict["type"] not in valid_types:
        raise InvalidDataFormatError(f"Invalid item type: {item_dict['type']}")
    
    #Cost must be a real integer
    if not isinstance(item_dict["cost"], int):
        raise InvalidDataFormatError("Cost must be an integer.")
    
    #Effect must be in the format stat_name:value
    if ":" not in item_dict["effect"]:
        raise InvalidDataFormatError("Effect must be printed as 'stat_name:value'.")
    return True

def create_default_data_files():
    
    if not os.path.exists("data"):
        os.makedirs("data")

    # makes quests.txt
    if not os.path.exists("data/quests.txt"):
        try:
            with open("data/quests.txt", "w") as f:
                f.write(
"""QUEST_ID: slay_goblin
TITLE: Slay the Goblin
DESCRIPTION: A goblin threatens the village.
REWARD_XP: 100
REWARD_GOLD: 50
REQUIRED_LEVEL: 1
PREREQUISITE: NONE

"""
                )
        except Exception:
            raise CorruptedDataError("Cannot initiate data file quests.txt")

    # makes items.txt
    if not os.path.exists("data/items.txt"):
        try:
            with open("data/items.txt", "w") as f:
                f.write(
"""ITEM_ID: iron_sword
NAME: Iron Sword
TYPE: weapon
EFFECT: strength: 5
COST: 50
DESCRIPTION: Basic melee weapon.

"""
                )
        except Exception:
            raise CorruptedDataError("Cannot initiate data file items.txt")


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_quest_block(lines):

    # reading, splitting cleaning, and conversion >_<

    quest = {}
    for line in lines:
        if ":" not in line:
            raise InvalidDataFormatError(f"Line missing ':'")
        key, value = line.split(":", 1)
        key = key.strip().lower()
        value = value.strip()

        quest[key] = value
    try:
        quest["reward_xp"] = int(quest["reward_xp"])
        quest["reward_gold"] = int(quest["reward_gold"])
        quest["required_level"] = int(quest["required_level"])
    except Exception:
        raise InvalidDataFormatError("Int field is invalid")
    return quest

def parse_item_block(lines):
    # legit bSICALLY the same thing as parse_quest_block but for items

    item = {}
    for line in lines:
        if ": " not in line:
            raise InvalidDataFormatError("Item line missing ': ' separator")

        key, value = line.split(": ", 1)

        key = key.strip().lower()
        value = value.strip()

        item[key] = value
    try:
        item["cost"] = int(item["cost"])
    except Exception:
        raise InvalidDataFormatError("Item cost must be an integer")

    return item


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== GAME DATA MODULE TEST ===")
    
    # Test creating default files
    # create_default_data_files()
    
    # Test loading quests
    # try:
    #     quests = load_quests()
    #     print(f"Loaded {len(quests)} quests")
    # except MissingDataFileError:
    #     print("Quest file not found")
    # except InvalidDataFormatError as e:
    #     print(f"Invalid quest format: {e}")
    
    # Test loading items
    # try:
    #     items = load_items()
    #     print(f"Loaded {len(items)} items")
    # except MissingDataFileError:
    #     print("Item file not found")
    # except InvalidDataFormatError as e:
    #     print(f"Invalid item format: {e}")

