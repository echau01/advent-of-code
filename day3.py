

def num_trees(right: int, down: int) -> int:
    """
    Return the number of trees we would encounter if we travelled along the slope
    with the given "right" and "down" components.
    """

    # My current horizontal position (x-coordinate) in the forest.
    # The x-coordinate is taken modulo the horizontal length of the pattern.
    x = 0

    trees = 0
    line_acc = 0

    with open("day3.txt", "r") as f:
        for line in f:
            if not line_acc:
                line = line.strip("\n")

                if line[x] == "#":
                    trees += 1

                x = (x + right) % len(line)

            line_acc = (line_acc + 1) % down

    return trees


# Part 1
print(num_trees(3, 1))

# Part 2
print(num_trees(1, 1) * num_trees(3, 1) * num_trees(5, 1) * num_trees(7, 1) * num_trees(1, 2))
