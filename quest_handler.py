"""
COMP 163 - Project 3: Quest Chronicles
Quest Handler Module - Starter Code

Name: Madison Wilkins

AI Usage: help from chatgpt with bug fices and code recommendations again. 

This module handles quest management, dependencies, and completion.
"""

from custom_exceptions import (
    QuestNotFoundError,
    QuestRequirementsNotMetError,
    QuestAlreadyCompletedError,
    QuestNotActiveError,
    InsufficientLevelError
)

# ============================================================================
# QUEST MANAGEMENT
# ============================================================================

def accept_quest(character, quest_id, quest_data_dict):

    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest '{quest_id}' does not exist!")
    
    quest = quest_data_dict[quest_id]

    if character['level'] < quest['required_level']:
        raise InsufficientLevelError(f"Level {quest['required_level']} required!")
    
    requiredquest = quest['prerequisite']
    if requiredquest != "NONE" and requiredquest not in character['completed_quests']:
        raise QuestRequirementsNotMetError(f"'{requiredquest}' needs to be completed.")
    
    if quest_id in character['completed_quests']:
        raise QuestAlreadyCompletedError(f" '{quest_id}' has been completed!")
    
    if quest_id in character['active_quests']:
        raise QuestRequirementsNotMetError(f"'{quest_id}' is already active!")
    
    character['active_quests'].append(quest_id)

    return True


def complete_quest(character, quest_id, quest_data_dict):

    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest '{quest_id}' does not exist!")
    if quest_id not in character['active_quests']:
        raise QuestNotActiveError(f" You dont have '{quest_id}'!")
    quest = quest_data_dict[quest_id]

    character['active_quests'].remove(quest_id)
    character['completed_quests'].append(quest_id)

    xp_reward = quest["reward_xp"]
    gold_reward = quest["reward_gold"]

    character['experience'] += xp_reward
    character['gold'] += gold_reward

    return {
        "reward_xp": xp_reward,
        "reward_gold": gold_reward,
        "quest_title": quest["title"]
    }

def abandon_quest(character, quest_id):
    if quest_id not in character['active_quests']:
        raise QuestNotActiveError(f"You dont have '{quest_id}'!")
    character['active_quests'].remove(quest_id)
    return True

def get_active_quests(character, quest_data_dict):
    currentquests = []
    for quest_id in character['active_quests']:
        if quest_id in quest_data_dict: 
            currentquests.append(quest_data_dict[quest_id])

    return currentquests

def get_completed_quests(character, quest_data_dict):
    completedquests = []

    for quest_id in character["completed_quests"]:
        if quest_id in quest_data_dict:  
            completedquests.append(quest_data_dict[quest_id]) 

    return completedquests

def get_available_quests(character, quest_data_dict):
    available = []

    for quest_id, quest in quest_data_dict.items():
        if character['level'] < quest['required_level']:
            continue
        
        prereq = quest['prerequisite']
        if prereq != "NONE" and prereq not in character['completed_quests']:
            continue
        
        if quest_id in character['completed_quests']:
            continue
        
        if quest_id in character['active_quests']:
            continue

        available.append(quest)

    return available

# ============================================================================
# QUEST TRACKING
# ============================================================================

def is_quest_completed(character, quest_id):
    return quest_id in character['completed_quests']


def is_quest_active(character, quest_id):
    return quest_id in character['active_quests']


def can_accept_quest(character, quest_id, quest_data_dict):
    if quest_id not in quest_data_dict:
        return False
    quest = quest_data_dict[quest_id]
    if character['level'] < quest['required_level']:
        return False
    prereq = quest['prerequisite']
    if prereq != "NONE" and prereq not in character['completed_quests']:
        return False
    if quest_id in character['completed_quests']:
        return False
    if quest_id in character['active_quests']:
        return False
    
    return True

def get_quest_prerequisite_chain(quest_id, quest_data_dict):
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest '{quest_id}' doesn't exist!")
    
    sneeze = []
    current_quest_id = quest_id

    while True:
        if current_quest_id not in quest_data_dict:
            raise QuestNotFoundError(f"Quest '{current_quest_id}' doesn't exist!")
        sneeze.append(current_quest_id)
        prerequisite = quest_data_dict[current_quest_id]['prerequisite']
        if prerequisite == "NONE":
            break

        current_quest_id = prerequisite

    sneeze.reverse()
    return sneeze

# ============================================================================
# QUEST STATISTICS
# ============================================================================

def get_quest_completion_percentage(character, quest_data_dict):
    total_quests = len(quest_data_dict)
    if total_quests == 0:
        return 0.0
    completed = len(character['completed_quests'])
    return (completed / total_quests) * 100

def get_total_quest_rewards_earned(character, quest_data_dict):
    total_xp = 0
    total_gold = 0

    for quest_id in character["completed_quests"]:

        if quest_id in quest_data_dict:

            quest = quest_data_dict[quest_id]
            total_xp += quest["reward_xp"]
            total_gold += quest["reward_gold"]
    return {
        "total_xp": total_xp,
        "total_gold": total_gold
    }

def get_quests_by_level(quest_data_dict, min_level, max_level):
    results = []  

    for quest_id, quest in quest_data_dict.items():

        level = quest["required_level"]
        if min_level <= level <= max_level:
            results.append(quest)

    return results

# ============================================================================
# DISPLAY FUNCTIONS
# ============================================================================

def display_quest_info(quest_data):
    print(f"\n - - {quest_data['title']} - - ")
    print(f"Description: {quest_data['description']}")
    print(f"Required Level: {quest_data['required_level']}")
    print(f"Required Quest: {quest_data['prerequisite']}")
    print(f"Reward XP: {quest_data['reward_xp']}")
    print(f"Reward Gold: {quest_data['reward_gold']}")

def display_quest_list(quest_list):
    if not quest_list:
        print("No quests to display.")
        return
    print("\n- - Available Quest - -")
    for quest in quest_list:
        print(f"- {quest['title']} (Level {quest['required_level']})")
        print(f"  Rewards: {quest['reward_xp']} XP, {quest['reward_gold']} Gold")
        print()

def display_character_quest_progress(character, quest_data_dict):
    active_count = len(character['active_quests'])
    completed_count = len(character['completed_quests'])
    completion_percentage = get_quest_completion_percentage(character, quest_data_dict)
    total_rewards = get_total_quest_rewards_earned(character, quest_data_dict)

    print("\n- - QUEST PROGRESS - -")
    print(f"Active Quests: {active_count}")
    print(f"Completed Quests: {completed_count} !")
    print(f"Completion: {completion_percentage:.2f}%")
    print(f"Total XP Earned: {total_rewards['total_xp']}")
    print(f"Total Gold Earned: {total_rewards['total_gold']}")

# ============================================================================
# VALIDATION
# ============================================================================

def validate_quest_prerequisites(quest_data_dict):
    for quest_id, quest in quest_data_dict.items():

        prereq = quest['prerequisite']
        if prereq == "NONE":
            continue

        # If prerequisite name is not found in the list of quests
        if prereq not in quest_data_dict:
            raise QuestNotFoundError(
                f"'{prereq}' for '{quest_id}' doesn't exist!"
            )
    return True


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== QUEST HANDLER TEST ===")
    
    # Test data
    # test_char = {
    #     'level': 1,
    #     'active_quests': [],
    #     'completed_quests': [],
    #     'experience': 0,
    #     'gold': 100
    # }
    #
    # test_quests = {
    #     'first_quest': {
    #         'quest_id': 'first_quest',
    #         'title': 'First Steps',
    #         'description': 'Complete your first quest',
    #         'reward_xp': 50,
    #         'reward_gold': 25,
    #         'required_level': 1,
    #         'prerequisite': 'NONE'
    #     }
    # }
    #
    # try:
    #     accept_quest(test_char, 'first_quest', test_quests)
    #     print("Quest accepted!")
    # except QuestRequirementsNotMetError as e:
    #     print(f"Cannot accept: {e}")

