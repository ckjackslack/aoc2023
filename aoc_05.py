import re
from collections import defaultdict
from functools import reduce
from operator import add

from utils import (
    get_lines,
)


EXAMPLE_ALMANAC = """
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""

TRAVERSAL_PATH = [
    "seed",
    "soil",
    "fertilizer",
    "water",
    "light",
    "temperature",
    "humidity",
    "location",
]

BEG_SEEDS = "seeds:"

NUMBER_PATTERN = r"(\d+)"

SOURCE_DESTINATION_PATTERN = r"^([\w\-]+)"

SPLIT_AT = "-to-"


def get_traversal_path():
    return list(zip(TRAVERSAL_PATH, TRAVERSAL_PATH[1:]))


def parse_lines(lines):
    dd = defaultdict(list)
    lines = iter(lines)
    next(lines)
    key = None
    for line in lines:
        if line[0].isalpha():
            text = re.search(SOURCE_DESTINATION_PATTERN, line).group(0)
            source, destination = text.split(SPLIT_AT)
            key = (source, destination)
            dd[key] = []
        else:
            numbers = parse_numbers(line)
            dd[key].append(numbers)
    return dd


def parse_seed_line_part_one(line):
    if not line.startswith(BEG_SEEDS):
        raise ValueError("This is not a seed line.")
    to_skip = line.find(BEG_SEEDS) + len(BEG_SEEDS)
    numbers = line[to_skip:].strip()
    return parse_numbers(numbers)


def parse_seed_line_part_two(line):
    numbers = parse_seed_line_part_one(line)
    numbers = sorted(reduce(add, [
        list(range(
            numbers[i], numbers[i] + numbers[i+1]
        ))
        for i
        in range(0, len(numbers), 2)
    ], []))
    return numbers


def parse_numbers(line):
    return list(map(int, re.findall(NUMBER_PATTERN, line)))


def make_mapper(*rows):
    def mapper(what):
        nonlocal rows
        for row in rows:
            destination, source, length = row
            if what >= source:
                if what <= (source + length):
                    diff = what - source
                    return destination + diff
        return what
    return mapper


def find_location(lines, parse_seed_line_fn):
    lines = [line for line in lines.strip().split("\n") if line]
    data = parse_lines(lines)
    seeds = parse_seed_line_fn(lines[0])
    merged = {}
    for key, value in data.items():
        merged[key] = make_mapper(*value)
    locations = []
    path = get_traversal_path()
    for seed in seeds:
        out = seed
        for step in path:
            out = merged[step](out)
        locations.append(out)
    return min(locations)


def example_one():
    print(find_location(EXAMPLE_ALMANAC, parse_seed_line_part_one))


def example_two():
    print(find_location(EXAMPLE_ALMANAC, parse_seed_line_part_two))


def part_one():
    lines = "\n".join(get_lines("input/05.txt"))
    return find_location(lines, parse_seed_line_part_one)


def part_two():
    lines = "\n".join(get_lines("input/05.txt"))
    return find_location(lines, parse_seed_line_part_two)


def main():
    example_one()
    print(part_one())

    example_two()
    # print(part_two())


if __name__ == "__main__":
    main()
