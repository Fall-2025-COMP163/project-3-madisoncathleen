"""
COMP 163 - Project 3: Quest Chronicles
Combat System Module - Starter Code

Name: madison wilkins

AI Usage: some chatgpt help for code help and bug fixes
"""
from custom_exceptions import (
    InvalidTargetError,
    CombatNotActiveError,
    CharacterDeadError,
    AbilityOnCooldownError
)

# ============================================================================
# ENEMY DEFINITIONS
# ============================================================================

def create_enemy(enemy_type):
    """
    Create an enemy based on type
    """
    enemy = {
        "goblin": {
            "name": "Goblin",  
            "health": 50,
            "max_health": 50,
            "strength": 8,
            "magic": 2,
            "xp_reward": 25,
            "gold_reward": 10
        },
        "orc": {
            "name": "Orc",
            "health": 80,
            "max_health": 80,
            "strength": 12,
            "magic": 5,
            "xp_reward": 50,
            "gold_reward": 25
        },
        "dragon": {
            "name": "Dragon",
            "health": 200,
            "max_health": 200,
            "strength": 25,
            "magic": 15,
            "xp_reward": 200,
            "gold_reward": 100
        }
    }

    if enemy_type not in enemy:
        raise InvalidTargetError(f"Enemy '{enemy_type}' is not recognized!")
    
    standard = enemy[enemy_type]

    norm = {
        "name": standard["name"],
        "health": standard["health"],
        "max_health": standard["max_health"],
        "strength": standard["strength"],
        "magic": standard["magic"],
        "xp_reward": standard["xp_reward"],
        "gold_reward": standard["gold_reward"]
    }
    return norm

def get_random_enemy_for_level(character_level):

    if character_level <= 2:
        return create_enemy("goblin")
    elif 3 <= character_level <= 5:
        return create_enemy("orc")
    else:
        return create_enemy("dragon")

# ============================================================================
# COMBAT SYSTEM
# ============================================================================

class SimpleBattle:
    
    def __init__(self, character, enemy):
        self.character = character
        self.enemy = enemy
        self.combat_active = True
        self.turn_counter = 0
    
    def start_battle(self):
        if self.character['health'] <= 0:
            raise CharacterDeadError("Character is dead and cannot fight!") 
        else:
            print("Battle initiated between " + self.character['name'] + " and " + self.enemy['name'] + "!")

        while self.combat_active:
            self.player_turn()
            result = self.check_battle_end()

            if not self.combat_active:
                break
            if result:
                break

            self.enemy_turn()
            result = self.check_battle_end()
            if result:
                break

            self.turn_counter += 1

        if result == 'player':
            rewards = get_victory_rewards(self.enemy)

            self.character['xp'] += rewards['xp']
            self.character['gold'] += rewards['gold']

            return {
                'winner': 'player',
                'xp_gained': rewards['xp'],
                'gold_gained': rewards['gold']
            }
        
        elif result == 'enemy':
            return {
                'winner': 'enemy',
                'xp_gained': 0,
                'gold_gained': 0
            }
        
        else:
            return {
                'winner': 'none',
                'xp_gained': 0,
                'gold_gained': 0
            }
    
    def player_turn(self):
        if not self.combat_active:
            raise CombatNotActiveError("Combat is not active.")
        
        else:
            print(f"\n{self.character['name']}'s turn!")
            print("Choose an action:")
            print("1. Basic Attack")
            print("2. Special Ability")
            print("3. Try to Run")

            choice = input("Enter #: ")

            if choice == '1':
                damage = self.calculate_damage(self.character, self.enemy)
                self.apply_damage(self.enemy, damage)
                display_battle_log(f"{self.character['name']} attacks {self.enemy['name']} for {damage} damage!")
            elif choice == '2':
                use_special_ability(self.character, self.enemy)
                print(f"{self.character['name']} used their special ability!")
            elif choice == '3':
                escaped = self.attempt_escape()
                if escaped:
                    display_battle_log(f"{self.character['name']} successfully escaped the battle!")
                else:
                    display_battle_log(f"{self.character['name']} failed to escape!")
            else: 
                print("Invalid choice. Please select a valid action.")
                self.player_turn()
    
    def enemy_turn(self):
        if not self.combat_active:
            raise CombatNotActiveError("Combat is not active.")
        
        damage = self.calculate_damage(self.enemy, self.character)
        self.apply_damage(self.character, damage)
        display_battle_log(f"{self.enemy['name']} attacks {self.character['name']} for {damage} damage!")

        if self.character['health'] <= 0:
            self.character['health'] = 0 
            self.combat_active = False  
            display_battle_log(f"{self.character['name']} has been defeated!")
    
    def calculate_damage(self, attacker, defender):
        damage = attacker['strength'] - (defender['strength'] // 4)

        if damage < 1:
            damage = 1  
        
        return damage
    
    def apply_damage(self, target, damage):
        if target['health'] - damage < 0:
            target['health'] = 0
    
    def check_battle_end(self):
        if self.enemy['health'] <= 0:
            self.combat_active = False
            return 'player'
        
        if self.character['health'] <= 0:
            self.combat_active = False
            return 'enemy'
        
        return None
    
    def attempt_escape(self):
        import random

        possibility = random.randint(0, 1)

        if possibility == 1:
            self.combat_active = False
            return True
        
        return False

# ============================================================================
# SPECIAL ABILITIES
# ============================================================================

def use_special_ability(character, enemy):
    char_class = character['class']

    if char_class == "Warrior":
        return warrior_power_strike(character, enemy)
    elif char_class == "Mage":
        return mage_fireball(character, enemy)
    elif char_class == "Rogue":
        return rogue_critical_strike(character, enemy)
    elif char_class == "Cleric":
        return cleric_heal(character)
    else:
       raise InvalidTargetError(f"Unknown character class '{char_class}' for special ability.")

def warrior_power_strike(character, enemy):
    damage = max(1, character["strength"] * 2)
    enemy["health"] -= damage
    if enemy["health"] < 0:
        enemy["health"] = 0
    return f"Warrior used Power Strike dealing {damage} damage to {enemy['name']}"

def mage_fireball(character, enemy):
    damage = max(1, character["magic"] * 2)
    enemy["health"] -= damage
    if enemy["health"] < 0:
        enemy["health"] = 0
    return f"Mage used Fireball dealing {damage} damage to {enemy['name']}"

def rogue_critical_strike(character, enemy):
    import random

    base = character["strength"] - (enemy["strength"] // 4)
    if base < 1:
        base = 1

    critical = random.randint(0, 1)

    if critical == 1:
        fin_damage = base * 3
        crit_msg = "It's a critical hit! "
    else:
        fin_damage = base
        crit_msg = "You missed the critical hit."

    enemy["health"] -= fin_damage
    if enemy["health"] < 0:
        enemy["health"] = 0

    return f"Rogue used Critical Strike dealing {fin_damage} damage to {enemy['name']}. {crit_msg}"

def cleric_heal(character):
    heal_amount = 30

    max_health = character["max_health"]
    current_health = character["health"]

    new_health = current_health + heal_amount

    if new_health > max_health:
        new_health = max_health

    real_heal = new_health - current_health

    character["health"] = new_health

    return f"Cleric healed for {real_heal} health points."

# ============================================================================
# COMBAT UTILITIES
# ============================================================================

def can_character_fight(character):
    return character['health'] > 0

def get_victory_rewards(enemy):
    return {
        'xp': enemy['xp_reward'],
        'gold': enemy['gold_reward']
    }

def display_combat_stats(character, enemy):
    print("\n=== Combat Status ===")
    print(f"\n{character['name']}: HP={character['health']}/{character['max_health']}")
    print(f"{enemy['name']}: HP={enemy['health']}/{enemy['max_health']}")

def display_battle_log(message):
    print(f">>> {message}")


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== COMBAT SYSTEM TEST ===")
    
    # Test enemy creation
    # try:
    #     goblin = create_enemy("goblin")
    #     print(f"Created {goblin['name']}")
    # except InvalidTargetError as e:
    #     print(f"Invalid enemy: {e}")
    
    # Test battle
    # test_char = {
    #     'name': 'Hero',
    #     'class': 'Warrior',
    #     'health': 120,
    #     'max_health': 120,
    #     'strength': 15,
    #     'magic': 5
    # }
    #
    # battle = SimpleBattle(test_char, goblin)
    # try:
    #     result = battle.start_battle()
    #     print(f"Battle result: {result}")
    # except CharacterDeadError:
    #     print("Character is dead!")

