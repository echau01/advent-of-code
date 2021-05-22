from typing import List, Tuple


def run(instructions: List[str]) -> Tuple[bool, int]:
    """
    Run the assembly program with the given instructions. Returns a tuple
    containing a bool and an int.
        - The bool is True if the program finishes execution without
          infinitely looping; False otherwise.
        - The int is the value of acc when the program finishes running
          or right before the same instruction is executed a second time.
    """

    acc = 0
    instructions_seen = set()
    idx = 0

    while idx not in instructions_seen and idx < len(instructions):
        instruction = instructions[idx]
        instructions_seen.add(idx)
        argument = int(instruction[4:])

        if instruction.startswith("jmp"):
            idx += argument
            continue
        elif instruction.startswith("acc"):
            acc += argument

        idx += 1

    if idx < len(instructions):
        return False, acc
    else:
        return True, acc


with open("day8.txt", "r") as f:
    instructions = f.read().splitlines()

# Part 1
print(f"Part 1: acc={run(instructions)[1]}")

# Part 2
for i in range(len(instructions)):
    instruction = instructions[i]
    operation = instruction[0:3]

    # Swap out a jmp for nop or nop for jmp. Skip this current instruction
    # if it is an "acc" instruction.
    if operation == "acc":
        continue
    elif operation == "jmp":
        instructions[i] = "nop" + instruction[3:]
    elif operation == "nop":
        instructions[i] = "jmp" + instruction[3:]

    test_run = run(instructions)

    # Reset instructions list to how it was before
    instructions[i] = operation + instruction[3:]

    if test_run[0]:
        print(f"Part 2: acc={test_run[1]}")
        break
