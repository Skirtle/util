from dataclasses import dataclass, field
from typing import Iterator
import random

@dataclass(order = True)
class Die:
    sides: int = 6
    
    def __post_init__(self) -> None:
        if (self.sides <= 0): 
            raise ValueError(f"expected postive integer for sides, but got {self.sides} instead")
    
    def roll(self) -> int: return random.randint(1, self.sides)
    
    def __repr__(self) -> str: return f"1d{self.sides}"
    
    def __str__(self) -> str: return f"1d{self.sides}"
    
    def __hash__(self) -> int: return self.sides.__hash__()
    
    
@dataclass
class Bag:
    dice: list[Die] = field(default_factory = list)
    
    def roll(self, times = 1) -> int:
        total = 0
        for _ in range(times):
            for die in self.dice:
                total += die.roll()
        return total
    
    def __iter__(self) -> Iterator[Die]: return iter(self.dice)
    
    def __str__(self) -> str: 
        s = "["
        dice_dict = self.get_dice()
        for die in dice_dict:
            s += f"{dice_dict[die]}d{die.sides}, "
        return s[:len(s) - 2] + "]"
    
    def get_dice(self) -> dict[Die, int]:
        d = {}
        for die in self:
            if (die not in d): d[die] = 1
            else: d[die] += 1
        return d
    
    def append(self, *others) -> None:
        for other in others:
            if (isinstance(other, Die)): self.dice.append(other)
            elif (isinstance(other, int)): self.dice.append(Die(other))
            else: raise TypeError(f"expected type 'Die' or 'int' to append into bag, but got type '{type(other).__name__}' instead")

def split_dice_notation(s: str) -> dict[str, int]:
    if (len(s) == 0): return {"count": 0, "sides": 0}
    
    res = {"count": 0, "sides": 0}
    if (s[0].isalpha()): s = "1" + s # d4 -> 1d4
        
    d_index = s.index("d")
    count = s[:d_index]
    
    # Get where the sides end, for cases of 10+ sides
    
    index = d_index + 1
    sides = 0
    while (index < len(s) and s[index].isnumeric()):
        sides = sides * 10 + int(s[index])
        index += 1
    
    if (index < len(s)):
        # We have more stuff to go through
        keepdrop_highlow = ""
        if (s[index] == "k"): keepdrop_highlow = "keep"
        elif (s[index] == "d"): keepdrop_highlow = "drop"
        else: raise ValueError(f"Didn't expect '{s[index]}'")
        
        if (s[index + 1] == "h"): keepdrop_highlow += "high"
        elif (s[index + 1] == "l"): keepdrop_highlow += "low"
        else: raise ValueError(f"Didn't expect '{s[index + 1]}'")
        
        keepdrop_number = 0
        index = index + 2
        while (index < len(s) and s[index].isnumeric()):
            keepdrop_number = keepdrop_number * 10 + int(s[index])
            index += 1
        res[keepdrop_highlow] = keepdrop_number
    
    res["count"] = int(count)
    res["sides"] = int(sides)
    return res

def roll_dice(dice: str | list[Die | int] | Bag) -> list[int]:
    results = []
    
    if (isinstance(dice, str)):
        # 4d6kh3 is roll a d6 4 times, keep the highest 3
        split_notation = split_dice_notation(dice)
        sides = split_notation["sides"]
        count = split_notation["count"]
        results = [Die(sides).roll() for _ in range(count)]
        results = sorted(results, reverse = True)
        
        if ("keephigh" in split_notation): 
            print(f"Keeping highest {split_notation['keephigh']} of {results}")
            results = results[:split_notation["keephigh"]]

        elif ("keeplow" in split_notation): 
            print(f"Keeping lowest {split_notation['keeplow']} of {results}")
            results = results[len(results) - split_notation["keeplow"]:]

        elif ("drophigh" in split_notation): 
            print(f"Dropping highest {split_notation['drophigh']} of {results}")
            results = results[split_notation["drophigh"]:]

        elif ("droplow" in split_notation): 
            print(f"Dropping lowest {split_notation['droplow']} of {results}")
            results = results[:len(results) - split_notation["droplow"]]


    elif (isinstance(dice, Bag) or isinstance(dice, list)):
        for die in dice: 
            if (isinstance(die, int)):
                results.append(Die(die).roll())
            elif (isinstance(die, Die)):
                results.append(die.roll())

    return results
    
if __name__ == "__main__":
    bag = Bag()
    bag.append(6, 6, 8, 4, 20, 20, 6, 6)
    # print(roll_dice(bag))
    print(roll_dice("d4"))
    print(roll_dice("2d100"))
    print(roll_dice("6d8kh2"))
    print(roll_dice("6d8kl2"))
    print(roll_dice("6d8dh2"))
    print(roll_dice("6d8dl2"))