import re
from collections import defaultdict
from functools import reduce
from operator import mul

from utils import (
    get_lines,
)


EXAMPLE_GAMES = [
    "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green",
    "Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue",
    "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red",
    "Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red",
    "Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green",
]
GAME_PATTERN = r"^Game (\d+):"
REFERENCE_BAG = {
    "red": 12,
    "green": 13,
    "blue": 14,
}
REVEAL_PATTERN = r"(\d+) (\w+)"


def power_of_a_cubes_set(cubes):
    return reduce(mul, cubes.values(), 1)


def compare(reference_bag, current_reveal):
    for what, n in current_reveal.items():
        if reference_bag[what] < n:
            return False
    return True


def prepare_subsets(game):
    colon = game.find(":") + 2
    game = game[colon:]
    subsets = list(map(str.strip, game.split(";")))
    return [subset.split(", ") for subset in subsets]


def is_game_possible(game, reference_bag):
    subsets = prepare_subsets(game)
    is_possible = True
    for subset in subsets:
        current_reveal = {}
        for reveal in subset:
            n, what = re.search(REVEAL_PATTERN, reveal).groups()
            n = int(n)
            current_reveal[what] = n
        if not compare(reference_bag, current_reveal):
            is_possible = False
            break
    return is_possible


def get_fewest_number_of_cubes_possible(game):
    subsets = prepare_subsets(game)
    grouped = defaultdict(list)
    for subset in subsets:
        for reveal in subset:
            n, what = re.search(REVEAL_PATTERN, reveal).groups()
            n = int(n)
            grouped[what].append(n)
    return {k: max(v) for k, v in grouped.items()}


def get_game_number(game):
    return int(re.search(GAME_PATTERN, game).group(1))


def example_one():
    total = 0
    for line in EXAMPLE_GAMES:
        if is_game_possible(line, REFERENCE_BAG):
            total += get_game_number(line)
    assert total == 8
    print(total)


def example_two():
    total = 0
    for line in EXAMPLE_GAMES:
        cubes = get_fewest_number_of_cubes_possible(line)
        total += power_of_a_cubes_set(cubes)
    assert total == 2286
    print(total)


def part_one():
    total = 0
    for line in get_lines("input/02.txt"):
        if is_game_possible(line, REFERENCE_BAG):
            total += get_game_number(line)
    return total

def part_two():
    total = 0
    for line in get_lines("input/02.txt"):
        cubes = get_fewest_number_of_cubes_possible(line)
        total += power_of_a_cubes_set(cubes)
    return total


def main():
    example_one()
    print(part_one())

    example_two()
    print(part_two())


if __name__ == "__main__":
    main()
