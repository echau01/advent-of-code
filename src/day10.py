from typing import List, Set


def count_valid_arrangements(ratings: List[int]) -> int:
    """
    Returns the number of valid arrangements of the joltages in ratings. This function
    assumes that ratings is sorted in ascending order.
    """

    def helper(_ratings: List[int], exclude: Set[int], starting: int) -> int:
        """
        Returns the number of valid arrangements of the joltages in _ratings, assuming that:
        - _ratings is sorted in ascending order
        - any joltage whose index is in exclude must not be in any arrangement
        - every joltage whose index is less than starting and is not in exclude must be
          in any arrangement
        """

        result = 0

        if starting < len(_ratings) - 2:
            previous_included_idx = starting - 1
            next_included_idx = starting + 1

            while previous_included_idx in exclude:
                previous_included_idx -= 1

            while next_included_idx in exclude:
                next_included_idx += 1

            if 1 <= _ratings[next_included_idx] - _ratings[previous_included_idx] <= 3:
                exclude.add(starting)
                result += helper(_ratings, exclude, next_included_idx)
                exclude.remove(starting)

            result += helper(_ratings, exclude, next_included_idx)
            return result
        else:
            return 1

    return helper(ratings, set(), 1)


with open("day10.txt", "r") as f:
    adapter_chain = [0]

    for line in f.read().splitlines():
        adapter_chain.append(int(line))

adapter_chain = sorted(adapter_chain)

# Add my device's joltage rating to the the adapter chain.
adapter_chain.append(adapter_chain[-1] + 3)

one_jolt_diffs = 0
three_jolt_diffs = 0

for i in range(1, len(adapter_chain)):
    if adapter_chain[i] == adapter_chain[i - 1] + 1:
        one_jolt_diffs += 1
    elif adapter_chain[i] == adapter_chain[i - 1] + 3:
        three_jolt_diffs += 1

print(one_jolt_diffs * three_jolt_diffs)
print(adapter_chain)
print(count_valid_arrangements(adapter_chain))
