import re
from dataclasses import dataclass
from enum import Enum
from io import StringIO

from utils import (
    get_lines,
    get_lines_from_file,
)


class Instruction(Enum):
    RIGHT = "R"
    LEFT = "L"


class SpecialNode(Enum):
    START = "AAA"
    STOP = "ZZZ"


@dataclass
class Node:
    label: str
    left: str
    right: str

    def get(self, instr):
        return self.right if instr == Instruction.RIGHT.value else self.left


EXAMPLE_NETWORK = StringIO("""
RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
""")

LINE_PATTERN = r"^(\w+)\s\=\s\((\w+)\,\s(\w+)\)$"


def find_some_node(nodes, what, whole=False):
    for idx, node in enumerate(nodes):
        if node.label == what:
            return idx if not whole else node


def find_start_node(nodes):
    return find_some_node(nodes, SpecialNode.START.value)


def move_through_nodes(instructions, nodes):
    # print(instructions)
    # print(nodes)
    start_pos = find_start_node(nodes)
    start_node = nodes[start_pos]
    current_node = start_node
    steps = 0
    is_found = False
    while True:
        for instr in instructions:
            to_find = current_node.get(instr)
            steps += 1
            print(f"Current instruction: {instr}")
            print(f"Current node: {current_node}")
            print(f"Next node: {to_find}")
            if to_find == SpecialNode.STOP.value:
                is_found = True
                break
            current_node = find_some_node(nodes, to_find, whole=True)
        if is_found:
            break
    return steps


def parse_input(_input):
    lines = get_lines_from_file(_input)
    instructions = next(lines)

    nodes = []
    for line in lines:
        match = re.search(LINE_PATTERN, line)
        one, two, three = match.groups()
        nodes.append(Node(label=one, left=two, right=three))

    return instructions, nodes


def example_one():
    instructions, nodes = parse_input(EXAMPLE_NETWORK)
    return move_through_nodes(instructions, nodes)


def example_two():
    pass


def part_one():
    lines = get_lines("input/08.txt")
    instructions, nodes = parse_input(lines)
    return move_through_nodes(instructions, nodes)


def part_two():
    pass


def main():
    print(example_one())

    print(part_one())


if __name__ == "__main__":
    main()
