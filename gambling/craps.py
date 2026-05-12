import gambling.dice as dice
import matplotlib.pyplot as plt

def game(bet: int = 1, limit: int | None = 3, print_rolls: bool = False) -> int:
    
    first_roll = dice.roll_dice("2d6")
    first_sum = sum(first_roll)
    if (print_rolls): print(f"Rolled {first_roll[0]} + {first_roll[1]} = {first_sum}")
    if (first_sum in [2, 3, 12]): return 0
    elif (first_sum in [7, 11]): return 2 * bet

    rolls = 0
    while (limit == None or rolls < limit):
        new_roll = dice.roll_dice("2d6")
        new_sum = sum(new_roll)
        if (print_rolls): print(f"\tRolled {new_roll[0]} + {new_roll[1]} = {new_sum}")
        if (new_sum == 7): return 0
        elif (new_sum == first_sum): return 4 * bet
        
        if (limit): rolls += 1
    return 1 * bet

if __name__ == "__main__":
    winnings = {0: 0, 1: 0, 2: 0, 4: 0}
    total = 0
    n = 10000000
    for _ in range(n):
        w = game(limit = None)
        winnings[w] += 1
        total += w
    avg = total / n

    x = sorted(list(winnings.keys()))
    y = [winnings[i] for i in x]
    plt.bar(x, y)
    plt.title(f"Craps scores ({avg = }, n = {n:,})")
    plt.show()