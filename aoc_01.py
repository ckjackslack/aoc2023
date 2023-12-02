from utils import (
    concat_lists,
    find_all_positions,
    get_lines,
    group_by,
    put_on_positions,
    sliding_window_overlap,
)


NUMBER_WORDS = {
    v: k
    for k, v
    in enumerate(
        [
            "one", "two", "three",
            "four", "five", "six",
            "seven", "eight", "nine",
        ],
        start=1,
    )
}

NUMBER_WORDS_SORTED = sorted(
    NUMBER_WORDS.items(),
    key=lambda tup: -len(tup[0]),
)

NUMBER_WORDS_GROUPED = group_by(NUMBER_WORDS, len)


# def replace_number_words(line):
#     for length, items in sorted(
#         NUMBER_WORDS_GROUPED.items(),
#         key=lambda t: -t[0],
#     ):
#         for item in items:
#             if length > len(line):
#                 continue
#             for part in sliding_window_overlap(line, length):
#                 if part == item:
#                     line = line.replace(part, str(NUMBER_WORDS[part]), 1)
#     return line


# def replace_number_words(line):
#     while True:
#         replacements = 0
#         for word, value in NUMBER_WORDS.items():
#             if word in line:
#                 # print(f"replacing `{word}` in `{line}`")
#                 line = line.replace(word, str(value), 1)
#                 replacements += 1
#         if replacements == 0:
#             break
#     return line


# def replace_number_words(line):
#     found = {}
#     for word, value in NUMBER_WORDS.items():
#         positions = find_all_positions(line, word)
#         if positions:
#             found[value] = positions
#     for i, c in enumerate(line):
#         if c.isdigit():
#             c = int(c)
#             if c in found:
#                 found[c].append(i)
#             else:
#                 found[c] = [i]
#     return put_on_positions(line, found, strip=True)


def calculate_calibration_value(line, filter_non_digits=True):
    if filter_non_digits:
        line = "".join(c for c in line if c.isdigit())
    return int(line[0] + line[-1]) if line else 0


def find_all_numbers(line):
    ds = {}
    for word, value in NUMBER_WORDS.items():
        positions = find_all_positions(line, word)
        if positions:
            ds[str(value)] = positions
    for i, c in enumerate(line):
        if c.isdigit():
            if c in ds:
                ds[c].append(i)
            else:
                ds[c] = [i]
    return ds


def calculate_calibration_value_with_number_words(line):
    numbers = find_all_numbers(line)
    positions = concat_lists(numbers.values())
    first, last = min(positions), max(positions)
    for what, where in numbers.items():
        if first in where:
            first = what
        if last in where:
            last = what
    return int(str(first) + str(last))


def part_one():
    total = 0
    for line in get_lines("input/01.txt"):
        total += calculate_calibration_value(line)
    return total


def part_two():
    total = 0
    for line in get_lines("input/01.txt"):
        total += calculate_calibration_value_with_number_words(line)
    return total


def example_one():
    total = 0
    for line, num in [
        ("1abc2", 12),
        ("pqr3stu8vwx", 38),
        ("a1b2c3d4e5f", 15),
        ("treb7uchet", 77),
    ]:
        value = calculate_calibration_value(line)
        assert value == num
        total += value
    assert total == 142


def example_two():
    total = 0
    for line, num in [
        ("two1nine", 29),
        ("eightwothree", 83),
        ("abcone2threexyz", 13),
        ("xtwone3four", 24),
        ("4nineeightseven2", 42),
        ("zoneight234", 14),
        ("7pqrstsixteen", 76),
    ]:
        value = calculate_calibration_value_with_number_words(line)
        assert value == num
        total += value
    assert total == 281


def main():
    example_one()
    example_two()

    print(part_one())
    print(part_two())


if __name__ == "__main__":
    main()
