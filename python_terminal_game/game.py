import json
import random
import numpy as np
 
SAVE_FILE = "save_data.json"
HEAL_FULL_HP = 100
 
HIT_DAMAGE = 15                
BLEED_DAMAGE_PER_TURN = 3
BLEED_DURATION = 5
DAGGER_COMBO_MULTIPLIER = 0.5
BLOCK_ENDURANCE_MULTIPLIER = 7  
 
MOVE_NAMES = {"1": "Attack", "2": "Block", "3": "Dodge", "0": "Stumble"}
 
ENEMY_TEMPLATES = [
    ("Rabbit", 50),
    ("Orc", 150),
    ("Archer Goblin", 80),
]
 
STAT_POOL = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
 
 
class Player:
    def __init__(self, name, player_health, strength, agility, endurance):
        self.name = name
        self.health = player_health
        self.strength = strength
        self.agility = agility
        self.endurance = endurance
        self.equipped_weapon = None
        self.equipped_shield = None
 
    def take_damage(self, amount):
        self.health -= amount
 
    def is_alive(self):
        return self.health > 0
 
    def heal_full(self):
        self.health = HEAL_FULL_HP
 
    def level_up(self, stat_name):
        setattr(self, stat_name, getattr(self, stat_name) + 1)
 
    def to_dict(self):
        return {
            "player_health": self.health,
            "strength": self.strength,
            "agility": self.agility,
            "endurance": self.endurance,
        }
 
    def display_stats(self):
        print(f"\nPlayer: {self.name}")
        print(f"Health:    {self.health}")
        print(f"Strength:  {self.strength}")
        print(f"Agility:   {self.agility}")
        print(f"Endurance: {self.endurance}")
 
 
class Encounter:
    def __init__(self, name, health):
        self.name = name
        self.health = health
        self.is_stunned = False
        self.bleed_duration = 0
        picked_stats = np.random.choice(STAT_POOL, size=3)
        self.strength, self.endurance, self.agility = picked_stats
 
    def display(self):
        print(f"--- {self.name} ---")
        print(f"HP:        {self.health}")
        print(f"Strength:  {self.strength}")
        print(f"Endurance: {self.endurance}")
        print(f"Agility:   {self.agility}\n")
 
 
class Weapon:
    def __init__(self, name, wep_type, base_damage, scaling_stat,
                 can_use_shield, effect_name="None", effect_chance=0):
        self.name = name
        self.wep_type = wep_type
        self.base_damage = base_damage
        self.scaling_stat = scaling_stat
        self.can_use_shield = can_use_shield
        self.effect_name = effect_name
        self.effect_chance = effect_chance
        self.dagger_multiplier = 1.0
 
    def display(self):
        print(f"[{self.name}] - {self.wep_type}")
        print(f"ATK: {self.base_damage} ({self.scaling_stat})")
        if self.effect_name != "None":
            print(f"Special: {self.effect_chance}% chance to cause {self.effect_name}")
 
 
class Shield:
    def __init__(self, name, block_bonus_percent, required_endurance):
        self.name = name
        self.block_bonus_percent = block_bonus_percent
        self.required_endurance = required_endurance
 
 
WEAPONS = {
    "1": Weapon("Wooden Club", "Blunt", 10, "Strength", True,
                effect_name="Shock", effect_chance=25),
    "2": Weapon("Iron Sword", "Sharp", 12, "Endurance", True,
                effect_name="Bleed", effect_chance=40),
    "3": Weapon("Assassin Dagger", "Light", 10, "Agility", False,
                effect_name="Combo", effect_chance=100),
}
WOOD_SHIELD = Shield("Wooden Shield", block_bonus_percent=30, required_endurance=3)
 
 

def load_player():
    try:
        with open(SAVE_FILE, "r") as file:
            data = json.load(file)
        print("\n:::::save file loaded successfully:::::")
    except FileNotFoundError:
        data = {"player_health": 100, "strength": 3, "agility": 3, "endurance": 3}
        save_progress(data)
        print("\n-----created-----")
    print("*****player loaded*****")
    return Player("Hiro", **data)
 
 
def save_progress(stats_dict):
    with open(SAVE_FILE, "w") as file:
        json.dump(stats_dict, file, indent=4)
    print(" Game Saved Successfully!")
 
 
def choose_weapon(player, prompt="Choose your weapon:"):
    print(f"\n{prompt}")
    print("1. Wooden Club (Allows Shield)")
    print("2. Iron Sword (Allows Shield)")
    print("3. Assassin Dagger (No Shield allowed!)")
    choice = input("Enter 1, 2, or 3: ").strip()
 
    weapon = WEAPONS.get(choice)
    if weapon is None:
        print("Invalid choice — you get the default weapon.")
        weapon = WEAPONS["1"]
 
    player.equipped_weapon = weapon
    print(f"\n🗡️ You picked up the {weapon.name}!")
 
    if weapon.can_use_shield:
        player.equipped_shield = WOOD_SHIELD
        print("You also took a wooden shield.")
    else:
        player.equipped_shield = None
        print("🛡️ You put your shield away to hold the weapon in both hands.")
 
 

def roll_effect(weapon):
    return random.randint(1, 100) <= weapon.effect_chance
 
 
def player_deals_damage(player, enemy):
    weapon = player.equipped_weapon
    damage = weapon.base_damage * weapon.dagger_multiplier
    enemy.health -= damage
    print(f"🩸 You dealt {damage} damage!")
 
 
def apply_weapon_effect(player, enemy):
    weapon = player.equipped_weapon
    if weapon.effect_name == "Shock" and roll_effect(weapon):
        print("⚡ CRITICAL SHOCK! The enemy is staggered!")
        enemy.is_stunned = True
    elif weapon.effect_name == "Bleed" and roll_effect(weapon):
        print("🩸 DEEP CUT! The enemy is bleeding.")
        enemy.bleed_duration = BLEED_DURATION
 
 
def tick_bleed(enemy):
    if enemy.bleed_duration > 0 and enemy.health > 0:
        enemy.health -= BLEED_DAMAGE_PER_TURN
        enemy.bleed_duration -= 1
        print(f"🩸 The {enemy.name} loses {BLEED_DAMAGE_PER_TURN} HP from bleeding! "
              f"({enemy.bleed_duration} turns left)")
        if enemy.bleed_duration == 0:
            print(f"🩹 The {enemy.name}'s wounds have clotted.")
 
 
def update_dagger_combo(player, player_took_damage):
    weapon = player.equipped_weapon
    if weapon.name != "Assassin Dagger":
        return
    if not player_took_damage:
        weapon.dagger_multiplier *= DAGGER_COMBO_MULTIPLIER
        print(f"🗡️ COMBO UP! Your next attack will deal {weapon.dagger_multiplier:.1f}x damage!")
    else:
        if weapon.dagger_multiplier > 1.0:
            print("❌ COMBO BROKEN! Dagger damage resets to normal.")
        weapon.dagger_multiplier = 1.0
 
 
def resolve_turn(player, enemy, p_move, e_move):
    """Resolve one exchange of moves. Returns True if the player took damage."""
    player_took_damage = False
 
    if e_move == "0":  # enemy stunned this turn
        if p_move == "1":
            print("💥 FREE HIT! You strike the stunned enemy with no resistance!")
            player_deals_damage(player, enemy)
        return player_took_damage
 
    if p_move == "1" and e_move == "1":
        if player.strength < enemy.strength:
            print("💥 CRUSHED: They hit harder and faster!")
            player.take_damage(HIT_DAMAGE)
            player_took_damage = True
        elif player.strength > enemy.strength:
            print("🔥 DOMINATION: You overpower their strike!")
            player_deals_damage(player, enemy)
            apply_weapon_effect(player, enemy)
            tick_bleed(enemy)
        else:
            print("⚔️ CLASH: You both strike each other!")
            enemy.health -= player.equipped_weapon.base_damage
            player.take_damage(HIT_DAMAGE)
            player_took_damage = True
 
    elif p_move == "1" and e_move == "2":
        if player.endurance > enemy.endurance:
            print("You were strong enough to break the enemy's block!")
            player_deals_damage(player, enemy)
        elif player.endurance < enemy.endurance:
            print("You weren't strong enough to break the block.")
        else:
            print("The enemy blocked it perfectly.")
 
    elif p_move == "1" and e_move == "3":
        if player.agility > enemy.agility:
            print("You outpaced the enemy and landed a hit!")
            player_deals_damage(player, enemy)
        elif player.agility < enemy.agility:
            print("You weren't fast enough to catch the dodge.")
        else:
            print("The enemy is as fast as you.")
 
    elif p_move == "3" and e_move == "1":
        if player.agility > enemy.strength:
            print("💨 DOMINATION: You effortlessly sidestep the attack. 0 Damage!")
        elif player.agility < enemy.strength:
            print("💥 CRUSHED: You weren't fast enough! You take a massive hit.")
            player.take_damage(HIT_DAMAGE)
            player_took_damage = True
        else:
            if random.randint(1, 2) == 1:
                print("🎯 CLASH WON: You barely dodge in time!")
            else:
                print("❌ CLASH LOST: You dodge into their weapon!")
                player.take_damage(HIT_DAMAGE)
                player_took_damage = True
 
    elif p_move == "2" and e_move == "1":
        base_block = player.endurance * BLOCK_ENDURANCE_MULTIPLIER
        shield_bonus = player.equipped_shield.block_bonus_percent if player.equipped_shield else 0
        total_block = base_block + shield_bonus
        if random.randint(1, 100) <= total_block:
            print("🛡️ PERFECT BLOCK! You deflect the blow completely.")
        else:
            print("💥 GUARD BROKEN! Their attack smashes through.")
            player.take_damage(HIT_DAMAGE)
            player_took_damage = True
 
    elif p_move in ("2", "3") and e_move in ("2", "3"):
        print("👀 You both stand there staring at each other defensively. Nothing happens.")
 
    update_dagger_combo(player, player_took_damage)
    return player_took_damage
 
 
def level_up_menu(player):
    print("1. Strength")
    print("2. Endurance")
    print("3. Agility")
    stat_map = {"1": "strength", "2": "endurance", "3": "agility"}
    choice = input("\nChoose a stat to level up: ").strip()
    stat = stat_map.get(choice)
    if stat:
        player.level_up(stat)
        print(f"One stat point added to {stat}.")
    else:
        print("No valid stat chosen.stat points added to strength.")
        player.level_up("strength")
 
 
def combat(player, enemy):
    print("*****you started a fight*****")
    while player.is_alive() and enemy.health > 0:
        print(f"❤️ Your HP: {player.health}  |  👿 {enemy.name} HP: {enemy.health}")
        print("1. Attack ⚔️")
        print("2. Block 🛡️")
        print("3. Dodge 💨")
        p_move = input("What is your move? (1/2/3): ").strip()
 
        if p_move not in ("1", "2", "3"):
            print("Invalid move! You stumbled and lost your turn.")
            p_move = "0"
 
        if enemy.is_stunned:
            print(f"⚡ The {enemy.name} is STUNNED and cannot move!")
            e_move = "0"
            enemy.is_stunned = False
        else:
            e_move = random.choice(["1", "2", "3"])
 
        print(f"\n>>> You used {MOVE_NAMES[p_move]}! The {enemy.name} used {MOVE_NAMES[e_move]}! <<<")
        resolve_turn(player, enemy, p_move, e_move)
 
    if not player.is_alive():
        print(f"\n☠️ YOU DIED... The {enemy.name} defeated you.")
        e_l= input("Do you want another chance to fight? (y/n): ").strip().lower()
        if e_l == "y":
            extra_life(player)
            combat(player, enemy)
        else:
            print("Game Over.")
    else:
        print(f"\n🏆 VICTORY! You defeated the {enemy.name}.")
        level_up_menu(player)
 
    
def extra_life(player):
    print("\n💖 You found a magical fountain that restores your health and boosts your stats!")
    data = {"player_health": 150, "strength": 5, "agility": 4, "endurance": 8}
    save_progress(data)
    print("\nYour stats have been boosted and saved.")
    
 

def explore(player):
    print("\n🌲 You step out into the wild...")
    name, health = random.choice(ENEMY_TEMPLATES)
    enemy = Encounter(name, health)
 
    print(f"You encountered a {enemy.name}!")
    enemy.display()
 
    action = input("What do you wish to do — fight or flight (1/2): ").strip().lower()
    if action in ("fight", "1"):
        combat(player, enemy)
    elif action in ("flight", "2"):
        print("*****you fled from the fight*****")
    else:
        print("Invalid choice — you hesitate and the moment passes.")
 
 
def rest(player):
    print("\n⛺ You set up camp and rest. HP fully restored!")
    player.heal_full()
    print(f"❤️ HP fully restored to {player.health}!")
    print("💾 Auto-saving progress...")
    save_progress(player.to_dict())
 
 
def tavern(player):
    while True:
        print("\n🍺 You sit at the Tavern and review your gear.")
        print("1. Player stats")
        print("2. Weapons")
        print("3. Switch weapon")
        print("4. Exit Tavern")
        choice = input("\nWhat do you want to do?: ").strip().lower()
 
        match choice:
            case "1":
                player.display_stats()
            case "2":
                for weapon in WEAPONS.values():
                    weapon.display()
            case "3":
                choose_weapon(player, "Available Weapons:")
            case "4":
                break
            case _:
                print("Invalid choice.")
 
 
def main():
    player = load_player()
    choose_weapon(player, "Choose your starting weapon:")
 
    while True:
        print("\n" + "=" * 20)
        print("      MAIN MENU")
        print("=" * 20)
        print("1. Explore")
        print("2. Rest")
        print("3. Tavern")
        print("4. Quit")
 
        choice = input("\nWhat is your move?: ").strip().lower()
 
        match choice:
            case "1" | "explore":
                explore(player)
            case "2" | "rest":
                rest(player)
            case "3" | "tavern":
                tavern(player)
            case "4" | "quit":
                print("\n💾 Saving game... Farewell, adventurer!")
                save_progress(player.to_dict())
                break
            case _:
                print("\n❌ Invalid choice. Please pick 1, 2, 3, or 4.")
 
 
if __name__ == "__main__":
    main()
 