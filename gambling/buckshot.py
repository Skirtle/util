from __future__ import annotations
import random
from dataclasses import dataclass, field
from abc import ABC

@dataclass
class Shotgun:
    rounds: list[bool] = field(default_factory = list)
    is_sawed: bool = False
    
    def check_round(self) -> bool:
        return self.rounds[len(self.rounds) - 1]
    
    def polarize(self) -> None:
        self.rounds[0] = not self.rounds[0]
        
    def load(self, shells: list | None = None) -> None:
        if (not shells):
            round_count = random.randint(2, 8) # Need to check this
            self.rounds = [bool(random.randint(0, 1)) for _ in range(round_count)]
        elif (isinstance(shells, list)):
            self.rounds = [bool(shell) for shell in shells]
            
    def saw_off(self) -> None: self.is_sawed = True
        
    def fire(self) -> int:
        damage = self.rounds.pop()
        if (self.is_sawed and damage): 
            self.is_sawed = False
            return 2
        return damage

@dataclass
class Player:
    lives: int 
    items: list[Item] = field(default_factory = list)
    turns_to_skip: int = 0
    player_number: int = 0
    
    def __str__(self) -> str: return f"Player {self.player_number}: {self.lives} lives, items = {self.items}"
    def __repr__(self) -> str: return str(self)     

class Item(ABC):
    def use(self, shotgun: Shotgun | None = None, target: Player | None = None) -> object: ...

class MagnefyingGlass(Item):
    def use(self, shotgun: Shotgun | None = None, target: Player | None = None) -> object:
        if (shotgun): return shotgun.check_round()
    def __str__(self) -> str: return "Magnefying Glass"
    def __repr__(self) -> str: return str(self)

class Knife(Item):
    def use(self, shotgun: Shotgun | None = None, target: Player | None = None) -> object:
        if (shotgun): shotgun.saw_off()
    def __str__(self) -> str: return "Knife"
    def __repr__(self) -> str: return str(self)
        
class Beer(Item):
    def use(self, shotgun: Shotgun | None = None, target: Player | None = None) -> object:
        if (shotgun): return shotgun.rounds.pop()
    def __str__(self) -> str: return "Beer"
    def __repr__(self) -> str: return str(self)
        
class Cuffs(Item):
    def use(self, shotgun: Shotgun | None = None, target: Player | None = None) -> object:
        if (target): target.turns_to_skip = 2
    def __str__(self) -> str: return "Cuffs"
    def __repr__(self) -> str: return str(self)
    
class Polarizer(Item):
    def use(self, shotgun: Shotgun | None = None, target: Player | None = None) -> object:
        if (shotgun): shotgun.polarize()
    def __str__(self) -> str: return "Polarizer"
    def __repr__(self) -> str: return str(self)
        
class Cigarette(Item):
    def use(self, shotgun: Shotgun | None = None, target: Player | None = None) -> object:
        if (target): target.lives += 1
    def __str__(self) -> str: return "Cigarette"
    def __repr__(self) -> str: return str(self)

def continue_game(players: list[Player]) -> bool:
    left_alive = 0
    for player in players:
        if (player.lives >= 1): left_alive += 1
    return left_alive > 1

def game(player_count: int = 2, lives: int = 3, starting_item_count: int = 2) -> None:
    ITEMS = [MagnefyingGlass, Knife, Beer, Cuffs, Polarizer, Cigarette]
    
    # Create players and gives items
    players = [Player(lives, player_number = num + 1) for num in range(player_count)]
    for player in players:
        for _ in range(starting_item_count):
            player.items.append(random.choice(ITEMS)())
            
    shotgun = Shotgun()
    shotgun.load()
    
    # TODO - Announce what shells are loaded
    live_shells = 0
    blank_shells = 0
    for shell in shotgun.rounds:
        if (shell): live_shells += 1
        else: blank_shells += 1
    print(f"Loaded {live_shells} live and {blank_shells} blank")
    
    turn_cycle = 1
    while (continue_game(players)):
        if (turn_cycle >= 5): break
        
        for player in players:
            # Skip dead and players to that need to skip their turns
            if (player.lives == 0): continue
            elif (player.turns_to_skip > 0):
                player.turns_to_skip -= 1
                continue
            
            go_again = False
            went_once = False
            while (go_again or not went_once):
                go_again = False
                # Item selection
                while (True):
                    print(f"Player {player.player_number}, choose an item (0 for no choice):")
                    for index,item in enumerate(player.items):
                        print(f"\t{index + 1}. {item}")
                    item_choice = input(">>> ")
                    if (item_choice == ""): item_choice = 0
                    else: item_choice = int(item_choice)
                    
                    if (not item_choice): break
                    item_choice = player.items[item_choice - 1]
                    player.items.remove(item_choice)
                    
                    if (isinstance(item_choice, MagnefyingGlass)): 
                        loaded = item_choice.use(shotgun)
                        if (loaded): print("The shell is live")
                        else: print("The shell is a blank")
                    
                    elif (isinstance(item_choice, Knife)): 
                        item_choice.use(shotgun)
                    
                    elif (isinstance(item_choice, Beer)): 
                        loaded = item_choice.use(shotgun)
                        if (loaded): print("The ejected shell was live")
                        else: print("The ejected shell was a blank")
                        
                    elif (isinstance(item_choice, Cuffs)): 
                        print("Choose a player to handcuff to the table: ")
                        for index,target_player in enumerate(players):
                            if (index + 1 == player.player_number): continue
                            print(f"\t{index + 1}. Player {index + 1}")
                        target_index = int(input(">>> ")) - 1
                        item_choice.use(target = players[target_index])
                        
                    elif (isinstance(item_choice, Polarizer)): 
                        item_choice.use(shotgun)
                        
                    elif (isinstance(item_choice, Cigarette)): 
                        item_choice.use(target = player)
                        
                    else: raise NotImplementedError(f"Cannot use {item_choice} yet")
                    
                    
                # Choose someone to shoot
                print("Choose a player to shoot at: ")
                for index,target_player in enumerate(players):
                    print(f"\t{index + 1}. Player {index + 1}")
                target_index = int(input(">>> ")) - 1
                print(f"Player {player.player_number} aims at player {target_index + 1}")
                live = shotgun.fire()
                
                if (not live): 
                    print("The shell was a blank")
                    if (players[target_index] == player): go_again = True # Shot at self and was a blank, go again
                else: 
                    print(f"The shell was live")
                    players[target_index].lives -= live
                went_once = True
        
        turn_cycle += 1

if __name__ == "__main__":
    game()
    