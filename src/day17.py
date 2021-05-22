from typing import List, Set, Tuple, Union


def get_neighbours(point: Union[Tuple[int, int, int], Tuple[int, int, int, int]]) \
        -> Union[List[Tuple[int, int, int]], List[Tuple[int, int, int, int]]]:
    """
    Returns the neighbours of the given point.

    Definition: two distinct ordered tuples (x_1, x_2, ..., x_n) and (y_1, y_2, ..., y_n) are
    neighbours if for all 1 <= i <= n, x_i and y_i differ by at most 1.
    """

    result = []

    for x in range(point[0] - 1, point[0] + 2):
        for y in range(point[1] - 1, point[1] + 2):
            for z in range(point[2] - 1, point[2] + 2):
                if len(point) == 3:
                    if x != point[0] or y != point[1] or z != point[2]:
                        result.append((x, y, z))
                elif len(point) == 4:
                    for w in range(point[3] - 1, point[3] + 2):
                        if x != point[0] or y != point[1] or z != point[2] or w != point[3]:
                            result.append((x, y, z, w))
    return result


def count_active_neighbours(point: Union[Tuple[int, int, int], Tuple[int, int, int, int]],
                            active_locations: Union[Set[Tuple[int, int, int]], Set[Tuple[int, int, int, int]]]):
    neighbours = get_neighbours(point)
    result = 0

    for neighbour in neighbours:
        if neighbour in active_locations:
            result += 1

    return result


with open("day17.txt", "r") as f:
    contents = f.read().splitlines()

# Set of locations of all active cubes, represented as 3-tuples
active_cubes = set()
cycles = 6
cubes_becoming_inactive = set()
cubes_becoming_active = set()

for i in range(2):
    for y in range(len(contents)):
        for x in range(len(contents[y])):
            if contents[y][x] == "#":
                if i == 0:
                    active_cubes.add((x, y, 0))
                else:
                    active_cubes.add((x, y, 0, 0))

    for _ in range(cycles):
        for cube in active_cubes:
            neighbours = get_neighbours(cube)
            num_active_neighbours = count_active_neighbours(cube, active_cubes)

            if num_active_neighbours != 2 and num_active_neighbours != 3:
                cubes_becoming_inactive.add(cube)

            for neighbour in neighbours:
                if neighbour not in active_cubes \
                        and count_active_neighbours(neighbour, active_cubes) == 3:
                    cubes_becoming_active.add(neighbour)

        for cube in cubes_becoming_inactive:
            active_cubes.discard(cube)

        for cube in cubes_becoming_active:
            active_cubes.add(cube)

        cubes_becoming_active.clear()
        cubes_becoming_inactive.clear()

    print(len(active_cubes))
    active_cubes.clear()
