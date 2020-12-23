from typing import List, Optional, Tuple


def is_two_sum(target: int, nums: List[int]) -> bool:
    """
    Returns one pair of numbers in nums that sum to target. If no such
    pair exists, returns None.
    """

    differences = {target - n: n for n in nums}

    return any(map(lambda n: n in differences, nums))


def two_difference(target: int, nums: List[int]) -> Optional[Tuple[int, int]]:
    """
    Returns a pair of indices (i, j) such that nums[j] - nums[i - 1] == target.
    If no such pair exists, and if target is contained in nums, returns the
    tuple (0, j) where nums[j] == target. Otherwise, returns None.
    """

    differences = {target + nums[i - 1]: i for i in range(1, len(nums) + 1)}

    if target not in differences:
        differences[target] = 0

    for j in range(len(nums)):
        if nums[j] in differences:
            return differences[nums[j]], j

    return None


with open("day9.txt", "r") as f:
    counter = 0

    # All the numbers in day9.txt, in order of appearance
    all_numbers = []

    # The 25 most recently seen numbers
    recent_numbers = []

    # cumulative_sum[k] is the sum of the numbers from lines 1 to k+1 inclusive in day9.txt.
    # Equivalently, cumulative_sum[k] is the sum of the numbers in all_numbers[0..k].
    cumulative_sum = []

    part_one_answer = None

    for line in f:
        new_number = int(line)
        all_numbers.append(new_number)

        if not cumulative_sum:
            cumulative_sum.append(new_number)
        else:
            cumulative_sum.append(cumulative_sum[-1] + new_number)

        if len(recent_numbers) != 25:
            recent_numbers.append(new_number)
        else:
            if part_one_answer is None and not is_two_sum(new_number, recent_numbers):
                part_one_answer = new_number

            # Replace the oldest number (the earliest-seen number)
            # in the list of 25 numbers with the new number.
            recent_numbers[counter % 25] = new_number

        counter += 1

    print(f"Part 1 answer: {part_one_answer}")

    # To find the indices i and j such that all_numbers[i..j] sums up to part_one_answer, we just
    # need to find i and j such that cumulative_sum[j] - cumulative_sum[i - 1] == part_one_answer.
    contiguous_set_index_bounds = two_difference(part_one_answer, cumulative_sum)
    lower_bound = contiguous_set_index_bounds[0]
    upper_bound = contiguous_set_index_bounds[1]
    contiguous_set = all_numbers[lower_bound + 1:upper_bound + 1]

    print(f"Part 2 answer: {min(contiguous_set) + max(contiguous_set)}")
