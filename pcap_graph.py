from random import randint, seed, choices
from dataclasses import dataclass, field
from math import cos, sin, pi
import tkinter as tk
import graphs

@dataclass
class IP():
    oct1: int = 0
    oct2: int = 0
    oct3: int = 0
    oct4: int = 0

    def __post_init__(self):
        if (self.oct1 < 0 or self.oct1 > 255): raise ValueError(f"Value for octet 1 must be in range [0,255], but got {self.oct1} instead")
        elif (self.oct2 < 0 or self.oct2 > 255): raise ValueError(f"Value for octet 2 must be in range [0,255], but got {self.oct2} instead")
        elif (self.oct3 < 0 or self.oct3 > 255): raise ValueError(f"Value for octet 3 must be in range [0,255], but got {self.oct3} instead")
        elif (self.oct4 < 0 or self.oct4 > 255): raise ValueError(f"Value for octet 4 must be in range [0,255], but got {self.oct4} instead")

    def __str__(self) -> str: return f"{self.oct1}.{self.oct2}.{self.oct3}.{self.oct4}"

    def __repr__(self) -> str: return self.__str__()

    def __hash__(self) -> int: return self.__str__().__hash__()

    def __eq__(self, other) -> bool:
        if (not isinstance(other, IP)): return NotImplemented
        return (self.oct1 == other.oct1) and (self.oct2 == other.oct2) and (self.oct3 == other.oct3) and (self.oct4 == other.oct4) 

def generate_random_ip(oct1: int = -1, oct2: int = -1, oct3: int = -1, oct4: int = -1):
    oct1 = oct1 if oct1 in range(0,256) else randint(0, 255)
    oct2 = oct2 if oct2 in range(0,256) else randint(0, 255)
    oct3 = oct3 if oct3 in range(0,256) else randint(0, 255)
    oct4 = oct4 if oct4 in range(0,256) else randint(0, 255)
    return IP(oct1, oct2, oct3, oct4)

def generate_points_along_circle(x, y, radius, num_points):
    dAngle = 360 / num_points  # use float division for better accuracy
    points = []

    for i in range(num_points):
        angle = (i * dAngle) * pi / 180
        px = round(radius * cos(angle) + x)
        py = round(radius * sin(angle) + y)
        points.append((px, py))

    return points

def circle_points(center: tuple[int, int], radius: int):
    top_left = (center[0] - radius, center[1] - radius)
    bot_right = (center[0] + radius, center[1] + radius)
    return (top_left, bot_right)

if __name__ == "__main__":
    CONNS_MIN = 2
    CONNS_MAX = 4
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 800
    seed(1)
    ips = {}
    ip_count = 10
    graph_name = "Network Map"

    # Generate random IPs
    while (len(ips) != ip_count):
        new_ip = generate_random_ip(192, 168, 0)
        while (new_ip in ips):
            new_ip = generate_random_ip(192, 168, 0)
        ips[new_ip] = None
    
    # Generate connections between points
    circle_coords = generate_points_along_circle(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, 250, len(ips))
    for index,ip in enumerate(ips):
        conn_count = randint(CONNS_MIN, CONNS_MAX)
        ips[ip] = [choices(list(ips.keys()), k = conn_count), circle_coords[index]]

    # Print stuff
    for ip in ips: print(f"{ip}: {ips[ip][0]} ({ips[ip][1]})")

    # Create window
    window = tk.Tk()
    window.title(graph_name)
    window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
    canvas = tk.Canvas(window, width = WINDOW_WIDTH, height = WINDOW_HEIGHT, bg = "gray")
    canvas.pack(anchor = tk.CENTER, expand = True)

    # Draw nodes and connections
    for node in ips:
        start_coords = ips[node][1]
        # Node
        canvas.create_oval(*circle_points(ips[node][1], 30), fill = "black")

        # Connections
        for conn in ips[node][0]:
            end_coord = ips[conn][1]
            canvas.create_line(*start_coords, *end_coord)

    for node in ips:
        # Node label
        canvas.create_text(ips[node][1][0], ips[node][1][1] - 40, text = str(node), fill = "white", font=("Purisa", 12))

    window.mainloop()