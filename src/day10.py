from typing import List, Set


def count_valid_arrangements(ratings: List[int]) -> int:
    """
    Returns the number of valid arrangements of the joltages in ratings. This function
    assumes that ratings is sorted in ascending order.

    A valid arrangement is a subset of ratings where the first and last elements are included,
    and every element is at least 1 more and at most 3 more than the previous element.
    """

    def _count_valid_arrangements(_ratings: List[int], exclude: Set[int], start: int) -> int:
        """
        Returns the number of valid arrangements of the joltages in _ratings, assuming that:
        1. _ratings is sorted in ascending order.
        2. start is not in exclude.
        3. Any joltage whose index is in exclude must not be in any arrangement.
        4. Every joltage whose index is less than start and is not in exclude must be included
        in any arrangement.
        5. The sorted list formed by taking every joltage in [0, start] that is not in exclude
        is itself a valid arrangement.
        """

        result = 0

        # The last element of _ratings is always 3 more than the second-to-last element.
        # Thus, there are no valid arrangements where the second-to-last element is excluded.
        # If start points to the second-to-last element (or any element to the right of the
        # second-to-last element), then there is exactly 1 valid arrangement.

        if start < len(_ratings) - 2:
            # The highest index to the left of start that is not in exclude
            previous_included_idx = start - 1

            # The lowest index to the right of start that is not in exclude
            next_included_idx = start + 1

            while previous_included_idx in exclude:
                previous_included_idx -= 1

            while next_included_idx in exclude:
                next_included_idx += 1

            # If this conditional check does not pass, then that means
            # _ratings[next_included_idx] - _ratings[start] > 3, which means
            # there are 0 valid arrangements.
            if _ratings[next_included_idx] - _ratings[start] <= 3:
                # An example to illustrate our approach:
                # Suppose _rating looks like [0, 1, 2, 3, 4, 6, ...], and suppose start
                # points to the element 10. How many valid arrangements are there?
                #
                # The number 4 is the highest number in _rating whose difference from 1 is at most 3.
                #
                # Case 1: we must include 1 and 4.
                #
                # Let n be the number of valid arrangements where 2 and 3 are excluded, but 1 and 4 are
                # included. For each of those n arrangements, there are 3 valid analogous arrangements:
                # 1. The arrangement with 2 included.
                # 2. The arrangement with 3 included.
                # 3. The arrangement with both 2 and 3 included.
                # The total number of valid arrangements where 1 and 4 must be included is therefore 4n.
                # Note that this computation requires only one recursive call! This is the key area
                # where we save time.
                #
                # To generalize: if we must include x and y (where x < y), and there are n numbers between
                # x and y in _rating, then the number of valid arrangements is calculated as follows:
                # 1. Exclude all n numbers between x and y, and set start to point to y.
                # 2. Make a recursive call to _count_valid_arrangements.
                # 3. Multiply the result of the previous step by 2^n.
                #
                # Case 2: we must include 1 and exclude 4.
                #
                # In this case, we just add 4 to the exclude parameter, set start to point to 2,
                # and recursively call _count_valid_arrangements.
                #
                # Case 3: we must exclude 1.
                #
                # In this case, we just add 1 to the exclude parameter, set start to point to 2,
                # and recursively call _count_valid_arrangements.

                # Compute case 1
                middle_indices = []
                curr = next_included_idx

                while _ratings[curr] - _ratings[start] <= 3:
                    if curr not in exclude:
                        middle_indices.append(curr)

                    curr += 1

                highest_valid_idx = middle_indices[-1]
                middle_indices = middle_indices[:-1]

                for idx in middle_indices:
                    exclude.add(idx)

                result += _count_valid_arrangements(_ratings, exclude, highest_valid_idx) << len(middle_indices)

                for idx in middle_indices:
                    exclude.remove(idx)

                # Compute case 2. The conditional maintains assumption 2 of the function.
                if highest_valid_idx != next_included_idx:
                    exclude.add(highest_valid_idx)
                    result += _count_valid_arrangements(_ratings, exclude, next_included_idx)
                    exclude.remove(highest_valid_idx)

                # Compute case 3. The conditional maintains assumption 5 of the function.
                if 1 <= _ratings[next_included_idx] - _ratings[previous_included_idx] <= 3:
                    exclude.add(start)
                    result += _count_valid_arrangements(_ratings, exclude, next_included_idx)
                    exclude.remove(start)

            return result

        return 1

    if len(ratings) >= 2 and ratings[1] > ratings[0] + 3:
        return 0

    return _count_valid_arrangements(ratings, set(), 1)


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
print(count_valid_arrangements(adapter_chain))
