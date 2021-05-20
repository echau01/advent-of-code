from typing import List, Set


def get_combinations(x_positions: List[int]) -> Set[int]:
    """
    Returns the set of all possible numbers obtainable through the following process:
    1. Set all bits at the positions given in x_positions to "X", and set all other bits to 0
    2. Set some subset of the X bits to 1, then set all other X bits to 0.

    x_positions is a list of the positions of the X bits, where position 0 denotes the *rightmost* bit,
    and bits that are further left have higher position.

    For example, consider the input x_positions = [1, 4, 5]. This function returns a list of all numbers
    whose binary representation has the form XX00X0. Note how the X bits are at positions 1, 4, and 5.
    Each X bit can be set to 0 or 1. In total, there are 8 possible numbers that can be formed in this way:

    000000
    000010
    010000
    010010
    100000
    100010
    110000
    110010

    We return a set containing all 8 numbers.
    """

    def _get_combinations(x_positions: List[int], set_so_far: Set[int], curr_idx: int, curr_num: int):
        if curr_idx >= 0:
            set_so_far.add(curr_num + (1 << x_positions[curr_idx]))

            _get_combinations(x_positions, set_so_far, curr_idx - 1, curr_num)
            _get_combinations(x_positions, set_so_far, curr_idx - 1,
                              curr_num + (1 << x_positions[curr_idx]))

    result = {0}
    _get_combinations(x_positions, result, len(x_positions) - 1, 0)

    return result


with open("day14.txt", "r") as f:
    contents = f.read().splitlines()

# Number formed by replacing all X's in current bitmask with 0
mask_replace_x_with_zero = 0

# Number formed by replacing all X's in current bitmask with 1
mask_replace_x_with_one = 0

# Mapping of memory addresses (as int) to memory values (as int)
memory = dict()

# Idea: for each number, we first take all the 1 bits in the mask and
# overwrite the corresponding bits in the number with 1. This is done by
# bitwise-OR'ing the number with mask_replace_x_with_zero. Then, we take
# all the 0 bits in the mask and overwrite the corresponding bits in the
# number with 0. This is done by bitwise-AND'ing the number with mask_replace_x_with_one.

for line in contents:
    parsed_assignment = line.split(" = ")

    if parsed_assignment[0] == "mask":
        mask = parsed_assignment[1]
        mask_replace_x_with_zero = 0
        mask_replace_x_with_one = 0

        # Compute mask_replace_x_with_zero and mask_replace_x_with_one
        for character in mask:
            if character == "0":
                mask_replace_x_with_zero = mask_replace_x_with_zero << 1
                mask_replace_x_with_one = mask_replace_x_with_one << 1
            elif character == "1":
                mask_replace_x_with_zero = (mask_replace_x_with_zero << 1) + 1
                mask_replace_x_with_one = (mask_replace_x_with_one << 1) + 1
            else:  # character == "X"
                mask_replace_x_with_zero = mask_replace_x_with_zero << 1
                mask_replace_x_with_one = (mask_replace_x_with_one << 1) + 1
    else:  # parsed_assignment[0] equals "mem[k]" where k is some integer
        address = int(parsed_assignment[0].rsplit("mem[")[1][:-1])
        memory[address] = (int(parsed_assignment[1]) | mask_replace_x_with_zero) & mask_replace_x_with_one

print(sum(value for value in memory.values()))

# Part 2

# A list of the position of all X's in the bitmask, where position 0 is the rightmost bit,
# and position indices increase as we go left (i.e. as the bits become more significant).
mask_x_positions = []

memory.clear()

# Set of all possible combinations of numbers formed by first setting all non-X bits
# in the bitmask to 0, then setting some subset of the X bits to 1 bits while setting
# all other X bits to 0.
combinations = set()

# The number formed by replacing all non-X bits in the bitmask with 0 bits,
# then replacing all X bits with 1 bits.
mask_all_zeroes_except_at_x = 0

for line in contents:
    parsed_assignment = line.split(" = ")

    if parsed_assignment[0] == "mask":
        mask = parsed_assignment[1]
        mask_replace_x_with_zero = 0
        mask_x_positions.clear()
        mask_all_zeroes_except_at_x = 0

        for idx in range(len(mask)):
            if mask[idx] == "0":
                mask_replace_x_with_zero = mask_replace_x_with_zero << 1
                mask_all_zeroes_except_at_x = mask_all_zeroes_except_at_x << 1
            elif mask[idx] == "1":
                mask_replace_x_with_zero = (mask_replace_x_with_zero << 1) + 1
                mask_all_zeroes_except_at_x = mask_all_zeroes_except_at_x << 1
            else:  # character == "X"
                mask_replace_x_with_zero = mask_replace_x_with_zero << 1
                mask_all_zeroes_except_at_x = (mask_all_zeroes_except_at_x << 1) + 1
                mask_x_positions.append(len(mask) - 1 - idx)

        combinations = get_combinations(mask_x_positions)
        mask_all_ones_except_at_x = ~mask_all_zeroes_except_at_x
    else:  # parsed_assignment[0] equals "mem[k]" where k is some integer
        address = (int(parsed_assignment[0].rsplit("mem[")[1][:-1]) | mask_replace_x_with_zero) & ~mask_all_zeroes_except_at_x
        memory_value = int(parsed_assignment[1])

        for integer in combinations:
            memory[address | integer] = memory_value

print(sum(value for value in memory.values()))
