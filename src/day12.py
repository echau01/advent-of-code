NORTH = "N"
EAST = "E"
SOUTH = "S"
WEST = "W"

DIRECTIONS = (NORTH, EAST, SOUTH, WEST)
DIRECTION_UNIT_VECTORS = {NORTH: (0, -1), EAST: (1, 0), SOUTH: (0, 1), WEST: (-1, 0)}

# Represents the index in DIRECTIONS that contains the current direction of the boat
current_direction_idx = 1

ship_x = 0
ship_y = 0

instructions = []

with open("day12.txt", "r") as f:
    for line in f:
        line = line.strip("\n")
        instructions.append((line[0], int(line[1:])))

# Part 1
for instruction in instructions:
    action = instruction[0]
    value = instruction[1]

    if action == "L":
        current_direction_idx = (current_direction_idx - value // 90) % 4
    elif action == "R":
        current_direction_idx = (current_direction_idx + value // 90) % 4
    else:
        if action in DIRECTIONS:
            unit_vector = DIRECTION_UNIT_VECTORS[action]
        else:
            # In this case, action == "F"
            unit_vector = DIRECTION_UNIT_VECTORS[DIRECTIONS[current_direction_idx]]

        ship_x += value * unit_vector[0]
        ship_y += value * unit_vector[1]

print(abs(ship_x) + abs(ship_y))

# Part 2
ship_x = 0
ship_y = 0

waypoint_x = 10
waypoint_y = -1

for instruction in instructions:
    action = instruction[0]
    value = instruction[1]

    # A clockwise rotation by 90 is the transformation (x, y) -> (y, -x)
    # A counterclockwise rotation by 90 is the transformation (x, y) -> (-y, x)
    if action == "L":
        for i in range(value // 90):
            temp = waypoint_x
            waypoint_x = waypoint_y
            waypoint_y = -temp
    elif action == "R":
        for i in range(value // 90):
            temp = waypoint_x
            waypoint_x = -waypoint_y
            waypoint_y = temp
    elif action in DIRECTIONS:
        unit_vector = DIRECTION_UNIT_VECTORS[action]
        waypoint_x += value * unit_vector[0]
        waypoint_y += value * unit_vector[1]
    else:
        # In this case, action == "F"
        ship_x += value * waypoint_x
        ship_y += value * waypoint_y

print(abs(ship_x) + abs(ship_y))
