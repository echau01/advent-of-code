with open("day16.txt", "r") as f:
    contents = f.read().splitlines()

i = 0
field_intervals_map = dict()

while len(contents[i]) != 0:
    field_and_str_intervals = contents[i].split(": ")
    field = field_and_str_intervals[0]
    str_intervals = field_and_str_intervals[1].split(" or ")

    field_intervals = []

    for str_interval in str_intervals:
        endpoints = str_interval.split("-")
        interval = [int(endpoints[0]), int(endpoints[1])]

        if field not in field_intervals_map:
            field_intervals_map[field] = [interval]
        else:
            field_intervals_map[field].append(interval)

    i += 1

my_ticket_values = [int(num) for num in contents[i + 2].split(",")]
nearby_tickets_start_idx = i + 5

# Sum of all invalid ticket values in nearby tickets
error_rate = 0

invalid_ticket_indices = set()

for idx in range(nearby_tickets_start_idx, len(contents)):
    values = [int(num) for num in contents[idx].split(",")]
    invalid_ticket = False

    for value in values:
        value_fits_in_interval = False

        for intervals in field_intervals_map.values():
            for interval in intervals:
                if interval[0] <= value <= interval[1]:
                    value_fits_in_interval = True
                    break

        if not value_fits_in_interval:
            error_rate += value
            invalid_ticket_indices.add(idx)

print(error_rate)

# Part 2

# Maps each field to a set of their possible positions on a ticket (where position 0 denotes
# the first number on a ticket, position 1 denotes the second number, and so on).
field_possible_positions_map = dict()
fields = field_intervals_map.keys()
num_fields = len(fields)

for field in fields:
    field_possible_positions_map[field] = {i for i in range(num_fields)}

for idx in range(nearby_tickets_start_idx, len(contents)):
    if idx not in invalid_ticket_indices:
        values = [int(num) for num in contents[idx].split(",")]

        for value_idx in range(len(values)):
            value = values[value_idx]

            for field, intervals in field_intervals_map.items():
                if value_idx in field_possible_positions_map[field]:
                    value_fits_in_interval = False

                    for interval in intervals:
                        if interval[0] <= value <= interval[1]:
                            value_fits_in_interval = True
                            break

                    if not value_fits_in_interval:
                        field_possible_positions_map[field].discard(value_idx)

product = 1

for _ in range(num_fields):
    position = None

    for field, positions in field_possible_positions_map.items():
        if len(positions) == 1:
            position = positions.pop()

            if field[:len("departure")] == "departure":  # if the field starts with "departure"
                product *= my_ticket_values[position]

            break

    for positions in field_possible_positions_map.values():
        positions.discard(position)

print(product)
