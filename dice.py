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
    
    
if __name__ == "__main__":
    bag = Bag()
    bag.append(6, 6, 8, 4, 20, 20, 6, 6)
    print(bag)