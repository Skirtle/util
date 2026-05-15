import gambling.dice as dice


if __name__ == "__main__":
    n = 100000
    sides = [2, 4, 6, 8, 10, 12, 20, 100]
    rolls = 50
    avgs = []
    for side_count in sides:
        print(f"Rolling {rolls}d{side_count}")
        adv_rolls = [sum(dice.roll_dice(f"{rolls}d{side_count}kh1")) for _ in range(n)]
        
        d = dice.Die(side_count)
        normal_rolls = [d.roll() for _ in range(n)]
        avgs.append((sum(adv_rolls) / len(adv_rolls), sum(normal_rolls) / len(normal_rolls)))


    for index in range(len(sides)):
        print(f"Sides: {sides[index]}")
        print(f"\tAverage roll: {avgs[index][1]}")
        print(f"\tAverage advantage roll: {avgs[index][0]}")