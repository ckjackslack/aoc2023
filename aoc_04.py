import re

from utils import (
    get_lines,
)


BEG_CARD_PATTERN = r"Card\s+(\d+): "


EXAMPLE_SCRATCHCARDS = [
    "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53",
    "Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19",
    "Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1",
    "Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83",
    "Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36",
    "Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11",
]


def clean(line_of_numbers):
    return {
        int(n.strip())
        for n
        in line_of_numbers.split()
    }


def preprocess_line(line):
    winning, ours = re.sub(BEG_CARD_PATTERN, "", line).split("|")
    return clean(winning), clean(ours)


def total_worth_of_scratchcards_on_card(line):
    winning, ours = preprocess_line(line)
    points = 0
    for num in winning:
        if num in ours:
            if points == 0:
                points = 1
            else:
                points *= 2
    return points


def how_many_copies(winning, ours):
    return len([1 for num in winning if num in ours])


def prepare_lookup_table(lines):
    metadata = {}
    for line_no, line in enumerate(lines):
        winning, ours = preprocess_line(line)
        metadata[line_no] = how_many_copies(winning, ours)
    return metadata


def count_all_scratchpad_copies(lines):
    lookup_table = prepare_lookup_table(lines)

    no_of_cards = len(lookup_table)
    no_of_copies = [1] * no_of_cards

    for i in range(no_of_cards):
        for j in range(i + 1, min(i + 1 + lookup_table[i], no_of_cards)):
            no_of_copies[j] += no_of_copies[i]

    return sum(no_of_copies)


def example_one():
    total = 0
    for line in EXAMPLE_SCRATCHCARDS:
        total += total_worth_of_scratchcards_on_card(line)
    print(total)


def example_two():
    print(count_all_scratchpad_copies(EXAMPLE_SCRATCHCARDS))


def part_one():
    total = 0
    for line in get_lines("input/04.txt"):
        total += total_worth_of_scratchcards_on_card(line)
    return total


def part_two():
    return count_all_scratchpad_copies(get_lines("input/04.txt"))


def main():
    example_one()
    print(part_one())

    example_two()
    print(part_two())


if __name__ == "__main__":
    main()
