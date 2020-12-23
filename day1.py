from typing import List, Tuple, Optional


def two_sum(sum: int, array: List[int]) -> Optional[Tuple[int, int]]:
    mapping = dict()

    for num in array:
        mapping[sum - num] = num

    for num in array:
        if num in mapping:
            return num, mapping[num]

    return None


def three_sum(sum: int, array: List[int]) -> Optional[Tuple[int, int, int]]:
    mapping = dict()

    for num in array:
        mapping[sum - num] = num

    for key in mapping:
        pair = two_sum(key, array)

        if pair:
            return mapping[key], pair[0], pair[1]

    return None


with open("day1.txt", "r") as f:
    arr = [int(line) for line in f.readlines()]

pair = two_sum(2020, arr)
print(f"{pair} has product {pair[0] * pair[1]}")

three_tuple = three_sum(2020, arr)
print(f"{three_tuple} has product {three_tuple[0] * three_tuple[1] * three_tuple[2]}")
