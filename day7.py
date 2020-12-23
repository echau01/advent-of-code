from typing import Dict


# Each bag type T is associated with a dict that maps bag types to the quantities
# of those bag types that T must contain.
rules: Dict[str, Dict[str, int]] = dict()


def contains(bag_type: str, target_type: str) -> bool:
    """
    Returns True if a bag with type bag_type must eventually contain a bag with
    type target_type. Returns False otherwise.
    """

    if bag_type == target_type:
        return True

    inner_bag_types = rules[bag_type]

    for _bag_type in inner_bag_types:
        if contains(_bag_type, target_type):
            return True

    return False


def num_bags(bag_type: str) -> int:
    """
    Returns the number of bags contained inside the bag with given type.
    Does not include the outermost bag itself.
    """

    result = 1

    for key, value in rules[bag_type].items():
        # We add 1 to num_bags(key) so that we count the actual bag with type `key`.
        result += value * (num_bags(key) + 1)

    return result - 1


with open("day7.txt", "r") as f:
    for line in f:
        line = line.strip(".\n")
        line_components = line.split(" contain ")
        bag_type = " ".join(line_components[0].split(" ")[:-1])
        bag_rules = line_components[1].split(", ")

        if bag_type not in rules:
            rules[bag_type] = dict()

        if bag_rules[0] != "no other bags":
            for rule in bag_rules:
                rule_components = rule.split(" ", 1)
                quantity = int(rule_components[0])
                inner_bag_type = " ".join(rule_components[1].split(" ")[:-1])

                rules[bag_type][inner_bag_type] = quantity

gold_bag_counter = 0

for bag_type in rules:
    if contains(bag_type, "shiny gold"):
        gold_bag_counter += 1

# Why do we subtract 1? We want to calculate the number of bag types *other* than "shiny gold"
# that eventually contain a shiny gold bag.
print(gold_bag_counter - 1)

print(num_bags("shiny gold"))
