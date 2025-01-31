import random
import time

class Player:
    def __init__(self):
        self.level = 1
        self.hp = 100
        self.max_hp = 100
        self.attack = 10
        self.defense = 5
        self.gold = 0
        self.inventory = []
        self.exp = 0
        self.exp_to_next_level = 100
        self.mana = 50
        self.max_mana = 50
        self.moves = {
            "Basic Attack": self.basic_attack,
            "Power Strike": self.power_strike,
            "Defend": self.defend,
            "Double Strike": self.double_strike,
            "Counter": self.counter
        }
        self.defend_uses = 3  # Number of times Defend can be used per level
        self.double_strike_cooldown = 0  # Cooldown for Double Strike
        self.power_strike_turns = 0  # Turns remaining for Power Strike
        self.equipped_shield = None

    def basic_attack(self, enemy):
        damage = max(0, self.attack - enemy.defense)
        enemy.hp -= damage
        print(f"You used Basic Attack and dealt {damage} damage to {enemy.name}!")

    def power_strike(self, enemy):
        if self.power_strike_turns == 0:
            self.power_strike_turns = 1  # Set for the next turn
            print("You used Power Strike! It will activate on your next turn.")
        else:
            print(f"Power Strike is still on cooldown for {self.power_strike_turns} turn(s).")
            return

    def execute_power_strike(self, enemy):
        if self.power_strike_turns > 0:
            self.power_strike_turns -= 1
            if self.power_strike_turns == 0:
                damage = max(0, (self.attack * 2.25) - enemy.defense)
                enemy.hp -= damage
                print(f"You dealt {damage} damage to {enemy.name} with Power Strike!")

    def defend(self, enemy):
        if self.defend_uses > 0:
            self.defend_uses -= 1
            print(f"You used Defend! You can still use it {self.defend_uses} more time(s) this level.")
            return True  # Indicate that Defend was used
        else:
            print("You have no uses left for Defend this level.")
            return False

    def double_strike(self, enemy):
        if self.double_strike_cooldown > 0:
            print(f"Double Strike is on cooldown for {self.double_strike_cooldown} turn(s).")
            return

        damage = max(0, self.attack - enemy.defense)
        enemy.hp -= damage
        print(f"You used Double Strike and dealt {damage} damage to {enemy.name}!")
        enemy.hp -= damage
        print(f"You struck again and dealt {damage} damage to {enemy.name}!")
        self.double_strike_cooldown = 2  # Set cooldown for 2 turns

    def counter(self, enemy):
        if enemy.attack_type == "physical":
            damage = max(0, (enemy.attack * 0.25) - self.defense)  # Reduced damage from enemy
            enemy.hp -= damage * 3  # Counter deals 3x damage
            print(f"You used Counter and dealt {damage * 3} damage to {enemy.name}!")
        else:
            print(f"{enemy.name} used a non-physical move. Counter failed!")

    def gain_exp(self, amount):
        self.exp += amount
        if self.exp >= self.exp_to_next_level:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.max_hp += 20
        self.hp = self.max_hp
        self.attack += 5
        self.defense += 2
        self.max_mana += 5
        self.mana = self.max_mana
        self.exp -= self.exp_to_next_level
        self.exp_to_next_level = int(self.exp_to_next_level * 1.5)
        print(f"Level up! You are now level {self.level}!")
        self.show_stats()

    def use_item(self, item):
        if item.stat == "hp":
            self.hp = min(self.hp + item.value, self.max_hp)
            print(f"You used {item.name} and restored {item.value} HP!")
        elif item.stat == "mana":
            self.mana = min(self.mana + item.value, self.max_mana)
            print(f"You used {item.name} and restored {item.value} Mana!")
        elif item.stat == "attack":
            self.attack += item.value
            print(f"You used {item.name} and gained {item.value} Attack!")
        elif item.stat == "defense":
            self.defense += item.value
            print(f"You used {item.name} and gained {item.value} Defense!")
        elif item.stat == "move":
            self.unlock_move(item.move_name, item.move_function)
        self.inventory.remove(item)

    def unlock_move(self, move_name, move_function):
        if move_name not in self.moves:
            self.moves[move_name] = move_function
            print(f"You unlocked a new move: {move_name}!")

    def show_moves(self):
        print("\nAvailable Moves:")
        for i, (move_name, _) in enumerate(self.moves.items()):
            print(f"{i+1}. {move_name}")

    def show_stats(self):
        print(f"Level: {self.level}, HP: {self.hp}/{self.max_hp}, Attack: {self.attack}, Defense: {self.defense}, Gold: {self.gold}, EXP: {self.exp}/{self.exp_to_next_level}, Mana: {self.mana}/{self.max_mana}")

    def has_item(self, item_name):
        return any(item.name == item_name for item in self.inventory)

class Enemy:
    def __init__(self, name, hp, attack, defense, exp_reward, gold_reward, attack_type="physical"):
        self.name = name
        self.hp = hp * 2.5  # Enemies are 2.5x stronger
        self.attack = attack * 2.5
        self.defense = defense * 2.5
        self.exp_reward = exp_reward
        self.gold_reward = gold_reward
        self.attack_type = attack_type

    def is_alive(self):
        return self.hp > 0

class Boss(Enemy):
    def __init__(self, name, hp, attack, defense, exp_reward, gold_reward, attack_type="physical"):
        super().__init__(name, hp, attack, defense, exp_reward, gold_reward, attack_type)

class Item:
    def __init__(self, name, stat, value, move_name=None, move_function=None, price=50):
        self.name = name
        self.stat = stat
        self.value = value
        self.move_name = move_name
        self.move_function = move_function
        self.price = price

class Store:
    def __init__(self, player):
        self.player = player
        self.items = [
            Item("Sword", "attack", 10, "Slash", lambda enemy: player.slash(enemy), price=100),
            Item("Shield", "defense", 10, "Shield Bash", lambda enemy: player.shield_bash(enemy), price=100),
            Item("Staff", "move", 0, "Fireball", lambda enemy: player.fireball(enemy), price=150),
            Item("Potion", "hp", 50, price=30),
            Item("Mana Potion", "mana", 25, price=30)
        ]

    def show_items(self):
        for i, item in enumerate(self.items):
            if item.stat == "move":
                print(f"{i+1}. {item.name} (Unlocks: {item.move_name}) - {item.price} gold")
            else:
                print(f"{i+1}. {item.name} (+{item.value} {item.stat}) - {item.price} gold")

    def buy_item(self, item_index):
        item = self.items[item_index - 1]
        if self.player.gold >= item.price:
            self.player.gold -= item.price
            self.player.inventory.append(item)
            print(f"You bought {item.name}!")
        else:
            print("Not enough gold!")

def battle(player, enemy):
    while player.hp > 0 and enemy.is_alive():
        print(f"\n{enemy.name} HP: {enemy.hp}")
        print(f"Your HP: {player.hp}/{player.max_hp}, Mana: {player.mana}/{player.max_mana}")
        action = input("Press 'i' to open inventory, 'e' to select a move, or 'a' to attack: ").lower()
        if action == 'i':
            print("\nInventory:")
            for i, item in enumerate(player.inventory):
                print(f"{i+1}. {item.name} (+{item.value} {item.stat})")
            item_choice = input("Enter the number of the item to use (or 'b' to go back): ")
            if item_choice.isdigit() and int(item_choice) <= len(player.inventory):
                player.use_item(player.inventory[int(item_choice) - 1])
        elif action == 'e':
            player.show_moves()
            move_choice = input("Enter the number of the move to use (or 'b' to go back): ")
            if move_choice.isdigit() and int(move_choice) <= len(player.moves):
                move_name = list(player.moves.keys())[int(move_choice) - 1]
                if move_name == "Power Strike":
                    player.power_strike(enemy)
                else:
                    player.moves[move_name](enemy)  # Pass the enemy argument here
                if enemy.is_alive():
                    player.execute_power_strike(enemy)  # Execute Power Strike if applicable
                    damage = max(0, enemy.attack - player.defense)
                    player.hp -= damage
                    print(f"{enemy.name} dealt {damage} damage to you!")
            else:
                print("Invalid choice, please try again.")
        elif action == 'a':
            player.basic_attack(enemy)
            if enemy.is_alive():
                damage = max(0, enemy.attack - player.defense)
                player.hp -= damage
                print(f"{enemy.name} dealt {damage} damage to you!")
        else:
            print("Invalid choice!")

        # Handle cooldowns
        if player.double_strike_cooldown > 0:
            player.double_strike_cooldown -= 1
        if player.power_strike_turns > 0:
            player.power_strike_turns -= 1

    if player.hp > 0:
        print(f"\nYou defeated {enemy.name}!")
        player.gold += int(enemy.gold_reward * 0.8)  # Reduced gold gain
        player.gain_exp(enemy.exp_reward)
        return True
    else:
        print("\nYou were defeated!")
        return False

def debug_console(player):
    print("\n--- Debug Console ---")
    print("1. Set Level")
    print("2. Set HP")
    print("3. Set Mana")
    print("4. Set Gold")
    print("5. Set Multiple Stats")
    print("6. Exit Debug")
    choice = input("Enter your choice: ")
    if choice == "1":
        level = int(input("Enter new level: "))
        player.level = level
        player.exp = 0
        player.exp_to_next_level = 100 * (1.5 ** (level - 1))
        print(f"Level set to {level}!")
    elif choice == "2":
        hp = int(input("Enter new HP: "))
        player.hp = hp
        player.max_hp = hp
        print(f"HP set to {hp}!")
    elif choice == "3":
        mana = int(input("Enter new Mana: "))
        player.mana = mana
        player.max_mana = mana
        print(f"Mana set to {mana}!")
    elif choice == "4":
        gold = int(input("Enter new Gold: "))
        player.gold = gold
        print(f"Gold set to {gold}!")
    elif choice == "5":
        level = int(input("Enter new level: "))
        hp = int(input("Enter new HP: "))
        mana = int(input("Enter new Mana: "))
        gold = int(input("Enter new Gold: "))
        player.level = level
        player.hp = hp
        player.max_hp = hp
        player.mana = mana
        player.max_mana = mana
        player.gold = gold
        print(f"Level set to {level}, HP set to {hp}, Mana set to {mana}, Gold set to {gold}!")
    elif choice == "6":
        print("Exiting debug console.")
    else:
        print("Invalid choice!")

def main():
    player = Player()
    enemies = [
        Enemy("Goblin", 20, 5, 2, 20, 10),
        Enemy("Orc", 30, 8, 4, 30, 20),
        Enemy("Slime", 15, 3, 1, 15, 5),
        Enemy("Skeleton", 25, 7, 3, 25, 15),
        Enemy("Wolf", 18, 6, 2, 18, 10),
        Enemy("Bandit", 22, 9, 4, 22, 20),
        Enemy("Spider", 12, 4, 1, 12, 5),
        Enemy("Bat", 10, 3, 0, 10, 5),
        Enemy("Snake", 16, 5, 2, 16, 10),
        Enemy("Rat", 8, 2, 0, 8, 3),
        Enemy("Ghost", 20, 6, 3, 20, 15),
        Enemy("Troll", 35, 10, 6, 35, 30),
        Enemy("Witch", 18, 7, 2, 18, 20, attack_type="magic"),
        Enemy("Knight", 30, 12, 8, 30, 40),
        Enemy("Dragonling", 25, 9, 5, 25, 25),
        Enemy("Golem", 40, 15, 10, 40, 50),
        Enemy("Vampire", 22, 10, 4, 22, 30),
        Enemy("Wraith", 20, 8, 3, 20, 20, attack_type="magic"),
        Enemy("Imp", 12, 4, 1, 12, 10)
    ]
    bosses = [
        Boss("Dragon", 100, 15, 10, 100, 100),
        Boss("Giant", 150, 20, 15, 150, 150),
        Boss("Demon King", 200, 25, 20, 200, 200)
    ]
    store = Store(player)

    debug_mode = False
    start_input = input("Press Enter to start or type 'debug' to enter debug mode: ").lower()
    if start_input == "debug":
        debug_mode = True
        debug_console(player)

    level = 1
    while level <= 30:
        print(f"\n--- Level {level} ---")
        if level % 10 == 0:
            boss = bosses[(level // 10) - 1]
            print(f"A wild {boss.name} appears!")
            if not battle(player, boss):
                break
        else:
            enemy = random.choice(enemies)
            print(f"A wild {enemy.name} appears!")
            if not battle(player, enemy):
                break
        if level % 5 == 0:
            print("\n--- Store ---")
            store.show_items()
            while True:
                try:
                    item_choice = int(input("Enter the number of the item you want to buy (or 0 to skip): "))
                    if item_choice == 0:
                        break
                    elif 1 <= item_choice <= len(store.items):
                        store.buy_item(item_choice)
                        break
                    else:
                        print("Invalid choice, please try again.")
                except ValueError:
                    print("Invalid input, please enter a number.")
        player.show_stats()

        if debug_mode:
            debug_input = input("Press 'd' to enter debug mode or any other key to continue: ").lower()
            if debug_input == "d":
                debug_console(player)

        level += 1

    if player.hp > 0:
        print("\nCongratulations! You completed all 30 levels!")
    else:
        print("\nGame Over! Try again!")

if __name__ == "__main__":
    main()
