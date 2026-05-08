def rotate(array: list, count: int = 1, direction: str = "right") -> list:
    count %= len(array)
    if (direction.lower() in ["right", "r"]): return array[len(array) - count:len(array)] + array[:len(array) - count]
    elif (direction.lower() in ["left", "l"]): return array[count:] + array[:count]
    raise ValueError(f"Expected direction 'left' or 'right' but got '{direction}' instead")

