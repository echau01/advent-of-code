def count(char: str, s: str) -> int:
    """
    Returns the number of occurrences of char in s. This function
    assumes char is a character (i.e. a string of length 1).
    """

    result = 0

    for i in range(len(s)):
        if s[i] == char:
            result += 1

    return result


ans_part1 = 0
ans_part2 = 0

with open("day2.txt", "r") as f:
    for line in f:
        components = line.split(":")

        policy = components[0]
        password = components[1][0:]

        letter = policy[-1]
        bounds = policy[:-2].split("-")
        lower_bound = int(bounds[0])
        upper_bound = int(bounds[1])

        occurrences = count(letter, password)

        if lower_bound <= occurrences <= upper_bound:
            ans_part1 += 1

        if (password[lower_bound] == letter) ^ (password[upper_bound] == letter):
            ans_part2 += 1

print(ans_part1)
print(ans_part2)
