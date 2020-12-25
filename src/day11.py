from copy import deepcopy
from typing import Callable, List, Tuple


# The possible states of a cell in the ferry seat layout.
FLOOR = "."
EMPTY = "L"
OCCUPIED = "#"

NORTHWEST = (-1, -1)
NORTH = (0, -1)
NORTHEAST = (1, -1)
WEST = (-1, 0)
EAST = (1, 0)
SOUTHWEST = (-1, 1)
SOUTH = (0, 1)
SOUTHEAST = (1, 1)

DIRECTIONS = (NORTHWEST, NORTH, NORTHEAST, WEST, EAST, SOUTHWEST, SOUTH, SOUTHEAST)

seat_layout = []


def get_cell(layout: List[List[str]], x: int, y: int) -> str:
    """
    Returns the value of the cell at position (x, y) in layout.
    """

    return layout[y][x]


def set_cell(layout: List[List[str]], x: int, y: int, state: str):
    """
    Set the value of the cell at position (x, y) in layout to state.
    """

    layout[y][x] = state


def valid_cell(layout: List[List[str]], x: int, y: int) -> bool:
    """
    Returns True if (x, y) is a valid position in layout. Assumes layout is a 2D grid.
    """

    return 0 <= x <= len(layout[0]) - 1 and 0 <= y <= len(layout) - 1


def occupied_adjacent_seats(layout: List[List[str]], x: int, y: int) -> int:
    """
    Returns the number of occupied seats that are adjacent to the seat at position (x, y) in layout.
    """

    adjacent_positions = [(i, j) for i in range(x - 1, x + 2) for j in range(y - 1, y + 2)
                          if valid_cell(layout, i, j) and not (i == x and j == y)]

    # The sum of a boolean array equals the number of True elements.
    return sum(map(lambda pos: get_cell(layout, pos[0], pos[1]) == OCCUPIED, adjacent_positions))


def occupied_directional_seats(layout: List[List[str]], x: int, y: int) -> int:
    """
    Returns the number of occupied seats visible (in one of the 8 directions) from the
    cell at position (x, y).
    """

    def occupied_seat_visible(_x: int, _y: int, direction: Tuple[int, int]) -> bool:
        """
        Returns True if an occupied seat is visible in the given direction from position (_x, _y).
        Returns False otherwise.

        The direction parameter is one of NORTHWEST, NORTH, NORTHEAST, WEST, EAST,
        SOUTHWEST, SOUTH, or SOUTHEAST.

        Note: empty seats block the visibility of occupied seats -- a bit counterintuitive, but
        those are the rules of the game.
        """

        _x += direction[0]
        _y += direction[1]

        while valid_cell(layout, _x, _y):
            if get_cell(layout, _x, _y) == OCCUPIED:
                return True
            elif get_cell(layout, _x, _y) == EMPTY:
                return False

            _x += direction[0]
            _y += direction[1]

        return False

    return sum(map(lambda d: occupied_seat_visible(x, y, d), DIRECTIONS))


def simulate(layout: List[List[str]],
             occupied_seats_fn: Callable[[List[List[str]], int, int], int],
             occupied_seat_threshold: int) -> int:
    """
    Simulates ferry seat activity.

    The layout parameter is the initial seat layout. This parameter is not modified.

    occupied_seats_fn is a function that calculates the number of occupied seats "around"
    a position (x, y), for some definition of "around".

    occupied_seat_threshold is the minimum number of occupied seats "around" a seat
    that will cause that seat to become empty (if it is occupied).

    Returns the number of occupied seats when the seats reach an equilibrium.
    """

    layout_copy = deepcopy(layout)

    while True:
        new_occupied_seats = []
        new_empty_seats = []

        for y in range(len(layout_copy)):
            for x in range(len(layout_copy[0])):
                if (get_cell(layout_copy, x, y) == EMPTY
                        and not occupied_seats_fn(layout_copy, x, y)):
                    new_occupied_seats.append((x, y))
                elif (get_cell(layout_copy, x, y) == OCCUPIED
                        and occupied_seats_fn(layout_copy, x, y) >= occupied_seat_threshold):
                    new_empty_seats.append((x, y))

        if not new_occupied_seats and not new_empty_seats:
            break

        for seat in new_occupied_seats:
            set_cell(layout_copy, seat[0], seat[1], OCCUPIED)

        for seat in new_empty_seats:
            set_cell(layout_copy, seat[0], seat[1], EMPTY)

    return sum(map(lambda row: sum(map(lambda cell: cell == OCCUPIED, row)), layout_copy))


with open("day11.txt", "r") as f:
    for line in f:
        line = line.strip("\n")

        # list(line) returns a list of all the characters of line
        seat_layout.append(list(line))

print(simulate(seat_layout, occupied_adjacent_seats, 4))
print(simulate(seat_layout, occupied_directional_seats, 5))
