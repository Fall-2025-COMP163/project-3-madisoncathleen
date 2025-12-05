"""
COMP 163 - Project 3: Quest Chronicles
Main Game Module - Starter Code

Name: Madison Wilkins

AI Usage: Chatgpt assistance for bug fixes and code recommendations, and also made some of the strings sound less robotic.

This is the main game file that ties all modules together.
Demonstrates module integration and complete game flow.
"""

# Import all our custom modules
import character_manager
import inventory_system
import quest_handler
import combat_system
import game_data
from custom_exceptions import *

# ============================================================================
# GAME STATE
# ============================================================================

current_character = None
all_quests = {}
all_items = {}
game_running = False

# ============================================================================
# MAIN MENU
# ============================================================================

def main_menu():
    print("\n=== Main Menu ===")
    print("1. Begin a New Journey")
    print("2. Load Previous Adventure")
    print("3. Exit Game")

    answer = input("Select an option (1-3): ").strip()
    if answer in ['1', '2', '3']:
        return int(answer)
    
    print("Invalid choice. Enter 1, 2, or 3.")
    return main_menu()
    
def new_game():
    global current_character

    print("\n=== New Journey ===")

    name = input("Name your character: ").strip()
    print("Choose your specialty:")
    print("1. Warrior")
    print("2. Mage")
    print("3. Rogue")
    print("4. Cleric")
    class_choice = input("Select (1-4): ").strip()

    class_map = {
        '1': 'Warrior',
        '2': 'Mage',
        '3': 'Rogue',
        '4': 'Cleric'
    }
 
    if class_choice not in class_map: 
        print("Invalid choice. Try again.")
        return new_game()   
    char_class = class_map[class_choice] 

    try: 
        current_character = character_manager.create_character(name, char_class) 
        print(f"{name} the {char_class} is ready for adventure.")
    except InvalidCharacterClassError:
        print("Invalid class selection.")
        return 

def load_game():
    global current_character

    print("\n=== Load Adventure ===")

    saved_characters = character_manager.list_saved_characters() 
    if not saved_characters:
        print("No saved characters found. Start a new game instead.")
        return
    
    print("Your saved characters:")
    for i, char_name in enumerate(saved_characters, start=1):
        print(f"{i}. {char_name}") 
    
    answer = input("Select a character by number: ").strip()

    if not answer.isdigit():
        print("Enter a valid number.")
        return 
    
    choice = int(answer)

    if choice < 1 or choice > len(saved_characters):
        print("Invalid selection.")
        return
    
    char_name = saved_characters[choice - 1]

    try:
        current_character = character_manager.load_character(char_name)
        print(f"{char_name} has returned to the world.")
    except CharacterNotFoundError:
        print("Character file not found.")
        return
    except SaveFileCorruptedError:
        print("Save file is corrupted.")
        return  
    except InvalidSaveDataError:
        print("Save file contains invalid data.")
        return
    
    game_loop()
    

# ============================================================================
# GAME LOOP
# ============================================================================

def game_loop():
    global game_running, current_character
    
    game_running = True
    
    while game_running:
        choice = game_menu()
        
        if choice == 1:
            view_character_stats()
        elif choice == 2:
            view_inventory()
        elif choice == 3:
            quest_menu()
        elif choice == 4:
            explore()
        elif choice == 5:
            shop()
        elif choice == 6:
            save_game()
            print("Progress saved. Returning to the main menu.")
            game_running = False
        else:
            print("Invalid choice.")

def game_menu():
    print("\n=== Game Menu ===")
    print("1. Character Overview")
    print("2. Inventory")
    print("3. Quest Log")
    print("4. Explore the World")
    print("5. Visit Shop")
    print("6. Save and Exit")

    answer = input("Choose (1-6): ").strip()
    while answer not in ['1', '2', '3', '4', '5', '6']:
        print("Invalid choice. Enter a number between 1 and 6.")
        answer = input("Choose (1-6): ").strip()

    return int(answer)

# ============================================================================
# GAME ACTIONS
# ============================================================================

def view_character_stats():
    global current_character
    
    character = current_character

    print("\n=== Character Overview ===")
    print(f"Name: {character['name']}")
    print(f"Class: {character['class']}")
    print(f"Level: {character['level']}")
    print(f"Health: {character['health']}/{character['max_health']}")
    print(f"Strength: {character['strength']}")
    print(f"Experience: {character['xp']}")
    print(f"Gold: {character['gold']}")
    print(f"Magic: {character['magic']}")
    print(f"Active Quests: {len(character['active_quests'])}")
    print(f"Completed Quests: {len(character['completed_quests'])}")

def view_inventory():
    global current_character, all_items
    
    inventory_system.display_inventory(current_character, all_items) 
    answer = input("Type an item name to interact or 'back' to exit: ").strip()
    if answer.lower() == 'back':
        return

def quest_menu():
    global current_character, all_quests

    print("\n=== Quest Log ===")
    print("1. Active Quests")
    print("2. Available Quests")
    print("3. Completed Quests")
    print("4. Accept a Quest")
    print("5. Abandon a Quest")
    print("6. Force Complete Quest (debug)")
    print("7. Back")    

    answer = int(input("Choose (1-7): ")).strip()

    if answer == 7:
        return

def explore():
    global current_character

    print("You move deeper into unfamiliar territory...")

    enemy = combat_system.get_random_enemy_for_level(current_character['level'])
    print(f"A hostile {enemy['name']} emerges.")

    fight = combat_system.SimpleBattle(current_character, enemy)

    try:
        result = fight.start_battle()
    except CharacterDeadError:
        handle_character_death()
        return
    
    print("\n=== Encounter Result ===")

    if result['victory'] == "player":
        print("You survived the encounter.")
        print(f"Experience gained: {result['xp_gained']}")
        print(f"Gold collected: {result['gold_gained']}")

    elif result['victory'] == "enemy":
        print("You were defeated.")
        handle_character_death()    
        return
    else:
        print("The encounter ended without a clear winner.")

    input("Press Enter to continue...")

def shop():
    global current_character, all_items
    while True:
        print("\n=== Trading Post ===")
        print(f"Your Gold: {current_character['gold']}")
        print("Items for Sale:")

        for item_name, item_info in all_items.items():
            print(f"- {item_name}: {item_info['cost']} gold")

        print("1. Buy Item")
        print("2. Sell Item")
        print("3. Leave Shop")
        
        answer = input("Choose (1-3): ").strip()
        
        if answer == '1':
            item_id = input("Enter item name to buy: ").strip()

            if item_id not in all_items:
                print("That item is not sold here.")
                continue

            item_data = all_items[item_id]

            try:
                inventory_system.purchase_item(current_character, item_id, item_data)
                print(f"You acquire {item_data['name']}.")
            except InsufficientResourcesError:
                print("Not enough gold.")
            except InventoryFullError:
                print("Your pack is full.")

            input("Press Enter to continue...")
            continue

        elif answer == '2':
            item_id = input("Enter item name to sell: ").strip()

            if item_id not in all_items:
                print("The shop doesn't deal in that item.")
                continue

            item_data = all_items[item_id]
            try:
                gold = inventory_system.sell_item(current_character, item_id, item_data)
                print(f"You sold {item_data['name']} for {gold} gold.")
                
            except ItemNotFoundError:
                print("You don't possess that item.")

        elif answer == '3':
            break
        else:
            print("Invalid selection.")

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def save_game():
    global current_character

    if current_character is None:
        print("No character available to save.")
        return
    
    try: 
        character_manager.save_character(current_character)
        print(f"{current_character['name']}'s journey has been saved.")
    except PermissionError:
        print("Permission denied during save.")
    except IOError: 
        print("An I/O error occurred while saving.")

def load_game_data():
    global all_quests, all_items

    try:
        all_quests = game_data.load_quests() 
        all_items = game_data.load_items()
    except MissingDataFileError:
        print("Game data missing. Generating new data...")
        game_data.create_default_data_files()

        all_quests = game_data.load_quests()
        all_items = game_data.load_items()

    except InvalidDataFormatError as e:
        print(f"Error reading game data: {e}")
        raise

def handle_character_death():
    global current_character, game_running

    print("\n=== You Have Fallen ===")
    print("1. Revive (50 gold)")
    print("2. Return to Main Menu")

    while True:
        choice = input("Choose (1-2): ").strip()

        if choice == '1':
            if current_character['gold'] < 50:
                print("Not enough gold to revive.")
                game_running = False
                return

            current_character['gold'] -= 50

            try:
                character_manager.revive_character(current_character, cost=50)
                print("You awaken again, battered but alive.")
                return
            except InsufficientResourcesError:
                print("You lack the funds to revive.")

        elif choice == '2':
            print("Returning to main menu...")
            game_running = False
            return
        else:
            print("Invalid choice.")

def display_welcome():
    print("=" * 50)
    print("               MADISON'S GAME")
    print("=" * 50)
    print("\nA world shaped by your decisions.")
    print("Forge your path, test your limits, and leave your mark.")
    print()

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    display_welcome()
    
    try:
        load_game_data()
        print("Game data loaded.")
    except MissingDataFileError:
        print("Creating new data files...")
        game_data.create_default_data_files()
        load_game_data()
    except InvalidDataFormatError as e:
        print(f"Data error: {e}")
        print("Check your data files.")
        return
    
    while True:
        choice = main_menu()
        
        if choice == 1:
            new_game()
        elif choice == 2:
            load_game()
        elif choice == 3:
            print("\nExiting Madison's Game.")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
