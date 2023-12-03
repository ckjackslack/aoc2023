import re
from dataclasses import dataclass
from functools import reduce
from operator import mul
from string import punctuation
from typing import Tuple

from utils import (
    get_chars,
    get_lines,
)


@dataclass(frozen=True)
class NumberData:
    row: int
    number: int
    columns: Tuple[int]

    def its_me(self, row, column):
        return row == self.row and column in self.columns


@dataclass
class Point:
    x: int
    y: int

    def __add__(self, other):
        assert isinstance(other, self.__class__)
        return self.__class__(self.x + other.x, self.y + other.y)

    def as_tuple(self):
        return (self.x, self.y)


EXAMPLE_ENGINE_SCHEMATIC = [
    "467..114..",
    "...*......",
    "..35..633.",
    "......#...",
    "617*......",
    ".....+.58.",
    "..592.....",
    "......755.",
    "...$.*....",
    ".664.598..",
]

SYMBOLS = punctuation.replace(".", "")
GEAR_SYMBOL = "*"


def parse_all_numbers_with_positions(input_data):
    numbers = []
    for row, line in enumerate(input_data):
        for match in re.finditer(r"(\d+)", line):
            numbers.append(NumberData(
                row=row,
                number=int(match.group()),
                columns=tuple(
                    i
                    for i
                    in range(match.start(), match.end())
                ),
            ))
    return numbers


def get_adjacent_numbers(input_data, row, column):
    masks = [
        (-1, -1), (-1, 0), (-1, 1),     #012
        (0, -1), (0, 1),                #3x4
        (1, -1), (1, 0), (1, 1),        #567
    ]
    p_symbol = Point(row, column)
    temp = None
    adjacent_numbers = []
    for mask in masks:
        temp = p_symbol + Point(*mask)
        what = input_data[temp.x][temp.y]
        if what.isdigit():
            adjacent_numbers.append(temp.as_tuple())
    return adjacent_numbers


def get_sum_of_part_numbers(engine_schematic):
    numbers = parse_all_numbers_with_positions(engine_schematic)
    numbers = {n: False for n in numbers}

    for tup in get_chars(engine_schematic):
        char, row, column = tup

        if char in SYMBOLS:
            adjacent_numbers = get_adjacent_numbers(
                engine_schematic,
                row,
                column,
            )

            for an in adjacent_numbers:
                for number in numbers:
                    if number.its_me(*an):
                        numbers[number] = True
                        break

    return sum(n.number for n, flag in numbers.items() if flag)


def get_sum_of_all_gear_ratios(engine_schematic):
    numbers = parse_all_numbers_with_positions(engine_schematic)

    total = 0

    for tup in get_chars(engine_schematic):
        char, row, column = tup

        if char == GEAR_SYMBOL:
            adjacent_numbers = get_adjacent_numbers(
                engine_schematic,
                row,
                column,
            )

            for_ratio = set()
            for an in adjacent_numbers:
                for number in numbers:
                    if number.its_me(*an):
                        for_ratio.add(number)
                        break
            if len(for_ratio) == 2:
                total += reduce(mul, [nd.number for nd in for_ratio], 1)

    return total


def example_one():
    total = get_sum_of_part_numbers(EXAMPLE_ENGINE_SCHEMATIC)
    print(total)
    assert total == 4361


def example_two():
    total = get_sum_of_all_gear_ratios(EXAMPLE_ENGINE_SCHEMATIC)
    assert total == 467835


def part_one():
    lines = list(get_lines("input/03.txt"))
    return get_sum_of_part_numbers(lines)


def part_two():
    lines = list(get_lines("input/03.txt"))
    return get_sum_of_all_gear_ratios(lines)


def main():
    example_one()
    print(part_one())

    example_two()
    print(part_two())


if __name__ == "__main__":
    main()
