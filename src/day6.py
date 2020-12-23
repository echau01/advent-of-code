with open("day6.txt", "r") as f:
    yes_responses = dict()

    sum_any_yes = 0
    sum_all_yes = 0

    group_size = 0

    for line in f:
        line = line.strip("\n")

        if len(line):
            group_size += 1

            for char in line:
                if char in yes_responses:
                    yes_responses[char] += 1
                else:
                    yes_responses[char] = 1
        else:
            sum_any_yes += len(yes_responses)

            for value in yes_responses.values():
                if value == group_size:
                    sum_all_yes += 1

            yes_responses.clear()
            group_size = 0

    # We have to update the sums one more time when we finish reading the file, since
    # the last line processed may not be a blank line.
    sum_any_yes += len(yes_responses)

    for value in yes_responses.values():
        if value == group_size:
            sum_all_yes += 1

    print(sum_any_yes)
    print(sum_all_yes)
