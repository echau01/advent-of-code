from typing import Dict


class TurnInfo:
    def __init__(self):
        self.second_to_last_turn = None
        self.last_turn = None

    def record_turn(self, turn: int):
        self.second_to_last_turn = self.last_turn
        self.last_turn = turn

    def get_turn_difference(self):
        if self.second_to_last_turn is None:
            return 0
        else:
            return self.last_turn - self.second_to_last_turn


with open("day15.txt", "r") as f:
    numbers_as_strings = f.readline().strip("\n").split(",")

numbers = [int(num) for num in numbers_as_strings]
turn_dict: Dict[int, TurnInfo] = dict()
last_spoken_num = None

for i in range(1, len(numbers_as_strings) + 1):
    num = int(numbers_as_strings[i - 1])
    turn_dict[num] = TurnInfo()
    turn_dict[num].record_turn(i)
    last_spoken_num = num

for i in range(len(numbers_as_strings) + 1, 2021):
    last_spoken_num = turn_dict[last_spoken_num].get_turn_difference()

    if last_spoken_num not in turn_dict:
        turn_dict[last_spoken_num] = TurnInfo()

    turn_dict[last_spoken_num].record_turn(i)

print(last_spoken_num)

# Part 2

for i in range(2021, 30000001):
    last_spoken_num = turn_dict[last_spoken_num].get_turn_difference()

    if last_spoken_num not in turn_dict:
        turn_dict[last_spoken_num] = TurnInfo()

    turn_dict[last_spoken_num].record_turn(i)

print(last_spoken_num)
