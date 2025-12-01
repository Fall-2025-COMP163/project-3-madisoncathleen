"""
COMP 163 - Project 3: Quest Chronicles
Inventory System Module - Starter Code

Name: MADISON WILKINS BRO

AI Usage: [Document any AI assistance used]

This module handles inventory management, item usage, and equipment.
"""

from custom_exceptions import (
InventoryFullError,
ItemNotFoundError,
InsufficientResourcesError,
InvalidItemTypeError
)

MAX_INVENTORY_SIZE = 20

# ============================================================================  
# INVENTORY MANAGEMENT  
# ============================================================================  

def add_item_to_inventory(character, item_id):
    if len(character['inventory']) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Inventory is full, cannot add more items.")
    character['inventory'].append(item_id)
    return True

def remove_item_from_inventory(character, item_id):
    if item_id not in character['inventory']:
        raise ItemNotFoundError("Item not found in inventory. Check ID.")
    character['inventory'].remove(item_id)
    return True

def has_item(character, item_id):
    return item_id in character['inventory']

def count_item(character, item_id):
    return character['inventory'].count(item_id)

def get_inventory_space_remaining(character):
    remaining = MAX_INVENTORY_SIZE - len(character['inventory'])
    return remaining if remaining >= 0 else 0

def clear_inventory(character):
    removed_items = character['inventory'][:]  # FIXED
    character['inventory'] = []
    return removed_items


# ============================================================================  
# ITEM USAGE  
# ============================================================================  

def use_item(character, item_id, item_data):
    if item_id not in character['inventory']:
        raise ItemNotFoundError("Item not found in inventory. Check ID.")
    if item_data['type'] != 'consumable':
        raise InvalidItemTypeError("This item is not a consumable!")
    stat_name, value = parse_item_effect(item_data['effect'])
    apply_stat_effect(character, stat_name, value)
    remove_item_from_inventory(character, item_id)
    item_name = item_data.get('name', item_id)
    return f"Used {item_name}! {stat_name} increased by {value}!"

def equip_weapon(character, item_id, item_data):
    if item_id not in character["inventory"]:
        raise ItemNotFoundError("Item not found in inventory. Check ID.")  # FIXED MESSAGE
    if item_data["type"] != "weapon":
        raise InvalidItemTypeError("Item is not a weapon!")

    # SAFETY CHECK (PREVENT INVENTORY OVERFLOW DURING SWAP)
    if character["equipped_weapon"] is not None and len(character["inventory"]) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Inventory full — cannot swap weapons.")

    stat_name, value = parse_item_effect(item_data["effect"])
    character[stat_name] += value

    character["equipped_weapon"] = item_id
    remove_item_from_inventory(character, item_id)

    item_name = item_data.get('name', item_id)
    return f"Equipped {item_name}! {stat_name} increased by {value}!"

def equip_armor(character, item_id, item_data):
    if item_id not in character["inventory"]:
        raise ItemNotFoundError("Item not found in inventory. Check ID.")
    if item_data["type"] != "armor":
        raise InvalidItemTypeError("Item is not armor!")

    # SAFETY CHECK — PREVENT OVERFLOW BEFORE UNEQUIPPING
    if character["equipped_armor"] is not None and len(character["inventory"]) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Inventory full — cannot swap armor.")

    if character["equipped_armor"] is not None:
        old_armor_id = unequip_armor(character)
        add_item_to_inventory(character, old_armor_id)

    stat_name, value = parse_item_effect(item_data["effect"])
    character[stat_name] += value

    character["equipped_armor"] = item_id
    remove_item_from_inventory(character, item_id)

    item_name = item_data.get('name', item_id)
    return f"Equipped {item_name}! {stat_name} increased by {value}!"

def unequip_weapon(character):
    weapon_id = character["equipped_weapon"]
    if weapon_id is None:
        return None

    if len(character["inventory"]) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Inventory is full! Cannot unequip weapon!")

    weapon_data = character["game_data"]["items"][weapon_id]
    stat, val = parse_item_effect(weapon_data["effect"])
    character[stat] -= val

    character["equipped_weapon"] = None
    return weapon_id

def unequip_armor(character):
    armor_id = character["equipped_armor"]
    if armor_id is None:
        return None

    if len(character["inventory"]) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Inventory is full! Cannot unequip armor!")

    armor_data = character["game_data"]["items"][armor_id]
    stat, val = parse_item_effect(armor_data["effect"])
    character[stat] -= val

    character["equipped_armor"] = None
    return armor_id


# ============================================================================  
# SHOP SYSTEM  
# ============================================================================  

def purchase_item(character, item_id, item_data):
    if character['gold'] < item_data['cost']:
        raise InsufficientResourcesError("You're too poor!")
    if len(character['inventory']) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Inventory is full! Sell something?")
    character['gold'] -= item_data['cost']
    character['inventory'].append(item_id)
    return True

def sell_item(character, item_id, item_data):
    if item_id not in character['inventory']:
        raise ItemNotFoundError("Item not found in inventory. Check ID.")
    sell_price = item_data['cost'] // 2
    remove_item_from_inventory(character, item_id)
    character['gold'] += sell_price
    return sell_price


# ============================================================================  
# HELPERS  
# ============================================================================  

def parse_item_effect(effect_string):
    parts = effect_string.split(":")
    return parts[0], int(parts[1])

def apply_stat_effect(character, stat_name, value):
    character[stat_name] += value
    if stat_name == "health" and character["health"] > character["max_health"]:
        character["health"] = character["max_health"]

def display_inventory(character, item_data_dict):
    lines = ["- CURRENT INVENTORY ! -"]
    counts = {}
    for item_id in character["inventory"]:
        counts[item_id] = counts.get(item_id, 0) + 1

    if not counts:
        lines.append("Inventory is empty. . Try some shopping!")
        return "\n".join(lines)

    for item_id, qty in counts.items():
        item_info = item_data_dict.get(item_id, {})
        name = item_info.get("name", item_id)
        item_type = item_info.get("type", "Unknown")
        lines.append(f"{name} | x{qty} ({item_type})")
    return "\n".join(lines)



# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== INVENTORY SYSTEM TEST ===")
    
    # Test adding items
    # test_char = {'inventory': [], 'gold': 100, 'health': 80, 'max_health': 80}
    # 
    # try:
    #     add_item_to_inventory(test_char, "health_potion")
    #     print(f"Inventory: {test_char['inventory']}")
    # except InventoryFullError:
    #     print("Inventory is full!")
    
    # Test using items
    # test_item = {
    #     'item_id': 'health_potion',
    #     'type': 'consumable',
    #     'effect': 'health:20'
    # }
    # 
    # try:
    #     result = use_item(test_char, "health_potion", test_item)
    #     print(result)
    # except ItemNotFoundError:
    #     print("Item not found")

