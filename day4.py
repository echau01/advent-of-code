import re
from typing import Set


REQUIRED_FIELDS = ("byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid")
VALID_EYE_COLOURS = {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}

passports_with_required_fields = 0
valid_passports = 0


def has_required_fields(fields: Set[str]) -> bool:
    for field in REQUIRED_FIELDS:
        if field not in fields:
            return False

    return True


def valid_field(field: str, value: str) -> bool:
    def valid_byr(byr: str) -> bool:
        try:
            return 1920 <= int(byr) <= 2002
        except ValueError:
            return False

    def valid_iyr(iyr: str) -> bool:
        try:
            return 2010 <= int(iyr) <= 2020
        except ValueError:
            return False

    def valid_eyr(eyr: str) -> bool:
        try:
            return 2020 <= int(eyr) <= 2030
        except ValueError:
            return False

    def valid_hgt(hgt: str) -> bool:
        try:
            unit = hgt[-2:]
            height = int(hgt[:-2])

            if unit == "cm":
                return 150 <= height <= 193
            elif unit == "in":
                return 59 <= height <= 76
            else:
                return False
        except ValueError:
            return False

    def valid_hcl(hcl: str) -> bool:
        return re.fullmatch("#[0-9a-f]{6}", hcl) is not None

    def valid_ecl(ecl: str) -> bool:
        return ecl in VALID_EYE_COLOURS

    def valid_pid(pid: str) -> bool:
        return re.fullmatch("\\d{9}", pid) is not None

    def valid_cid(cid: str) -> bool:
        return True

    jump_table = {
        "byr": valid_byr,
        "iyr": valid_iyr,
        "eyr": valid_eyr,
        "hgt": valid_hgt,
        "hcl": valid_hcl,
        "ecl": valid_ecl,
        "pid": valid_pid,
        "cid": valid_cid
    }

    fn = jump_table[field]

    if fn:
        return fn(value)
    else:
        return False


with open("day4.txt", "r") as f:
    fields = set()
    valid_so_far = True

    for line in f:
        line = line.strip("\n")
        components = line.split()

        if len(line):
            field_dict = dict(zip(map(lambda c: c[0:3], components), map(lambda c: c[4:], components)))

            for key, value in field_dict.items():
                fields.add(key)
                valid_so_far = valid_so_far & valid_field(key, value)
        else:
            if has_required_fields(fields):
                passports_with_required_fields += 1

                if valid_so_far:
                    valid_passports += 1

            fields.clear()
            valid_so_far = True

    # We have to update the counters one more time when we finish reading the file, since
    # the last line processed may not be a blank line.
    if has_required_fields(fields):
        passports_with_required_fields += 1

        if valid_so_far:
            valid_passports += 1

print(passports_with_required_fields)
print(valid_passports)
