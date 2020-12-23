# The row number is the first 7 bits interpreted as unsigned binary
# The column number is the last 3 bits interpreted as unsigned binary.
# The seat ID is the entire 10-character string interpreted as unsigned binary.
# F = 0; B = 1; L = 0; R = 1


SEAT_ENCODING = {"F": 0, "B": 1, "L": 0, "R": 1}


def seat_id(seat_str: str) -> int:
    result = 0

    for i in range(len(seat_str)):
        next_bit = SEAT_ENCODING[seat_str[i]]

        if next_bit is not None:
            result = (result << 1) + next_bit
        else:
            raise ValueError("Parameter passed to seat_id(str) is invalid.")

    return result


with open("day5.txt", "r") as f:
    highest_seat_id = 0
    ids_seen = set()

    for line in f:
        next_id = seat_id(line.strip("\n"))
        ids_seen.add(next_id)
        highest_seat_id = max(highest_seat_id, next_id)

    print(highest_seat_id)

    my_seat_id = 0

    for seat_id in ids_seen:
        if (seat_id + 1) not in ids_seen and (seat_id + 2) in ids_seen:
            my_seat_id = seat_id + 1
        elif (seat_id - 1) not in ids_seen and (seat_id - 2) in ids_seen:
            my_seat_id = seat_id - 1

    print(my_seat_id)
