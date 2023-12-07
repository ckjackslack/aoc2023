import re
from collections import defaultdict, namedtuple
from functools import reduce
from io import StringIO
from operator import mul

from utils import (
    get_lines,
    get_lines_from_file,
)


Race = namedtuple("Race", "time distance")


EXAMPLE_DOCUMENT = StringIO("""
Time:      7  15   30
Distance:  9  40  200
""")

NAME_PATTERN = r"^(\w+):"

NUMBER_PATTERN = r"(\d+)"


def get_possible_holds(time):
    return list(range(0, time + 1))


def evaluate_distance(hold, time):
    how_many = time - hold
    return how_many * hold


def get_winning_ways(race):
    holds = get_possible_holds(race.time)
    c = 0
    for hold in holds:
        result = evaluate_distance(hold, race.time)
        if result > race.distance:
            c += 1
    return c


def parse_input(lines, ignore_spaces=False):
    races = []
    kwargs = defaultdict(list)
    for line in lines:
        name = re.search(NAME_PATTERN, line).group(1).lower()
        all_nums = re.findall(NUMBER_PATTERN, line)
        if ignore_spaces:
            kwargs[name].append(int("".join(all_nums)))
            continue
        for num in all_nums:
            kwargs[name].append(int(num))
    races = [
        Race(time=t, distance=d)
        for t, d
        in zip(
            kwargs["time"],
            kwargs["distance"], # this is current record
        )
    ]
    return races


def get_result(obj, ignore_spaces=False):
    if hasattr(obj, "read"):
        obj.seek(0)
        lines = get_lines_from_file(obj)
    elif type(obj) == list:
        lines = get_lines(obj)
    else:
        lines = obj
    data = parse_input(lines, ignore_spaces)
    return reduce(mul, [get_winning_ways(race) for race in data], 1)


def example_one():
    result = get_result(EXAMPLE_DOCUMENT)
    print(result)


def example_two():
    result = get_result(EXAMPLE_DOCUMENT, ignore_spaces=True)
    print(result)


def part_one():
    result = get_result(get_lines("input/06.txt"))
    print(result)


def part_two():
    result = get_result(get_lines("input/06.txt"), ignore_spaces=True)
    print(result)


def main():
    example_one()
    example_two()

    part_one()
    part_two()


if __name__ == "__main__":
    main()