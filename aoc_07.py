from collections import Counter
from enum import IntEnum, auto
from functools import cmp_to_key
from operator import itemgetter

from utils import (
    get_lines,
    get_lines_from_file,
)


FIGURE_SYMBOL = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
FIGURE_STRENGTH = range(len(FIGURE_SYMBOL) + 1, 1, -1)
FIGURE_SYMBOL_2 = ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"]
FIGURE_STRENGTH_2 = range(len(FIGURE_SYMBOL_2) + 1, 1, -1)
HAND_SIZE = 5
LOOKUP = dict(zip(FIGURE_SYMBOL, FIGURE_STRENGTH))
LOOKUP_2 = dict(zip(FIGURE_SYMBOL_2, FIGURE_STRENGTH_2))


class HandType(IntEnum):
    FIVE_OF_A_KIND = auto()
    FOUR_OF_A_KIND = auto()
    FULL_HOUSE = auto()
    THREE_OF_A_KIND = auto()
    TWO_PAIR = auto()
    ONE_PAIR = auto()
    HIGH_CARD = auto()

    @staticmethod
    def is_five_of_a_kind(hand):
        first = hand[0]
        return all(c == first for c in hand)

    @staticmethod
    def is_four_of_a_kind(hand):
        c = Counter(hand)
        return c.most_common(1)[0][1] == 4

    @staticmethod
    def is_full_house(hand):
        return list(map(itemgetter(1), Counter(hand).most_common())) == [3, 2]

    @staticmethod
    def is_three_of_a_kind(hand):
        c = Counter(hand)
        return c.most_common(1)[0][1] == 3

    @staticmethod
    def is_two_pair(hand):
        return list(map(itemgetter(1), Counter(hand).most_common())) == [2, 2, 1]

    @staticmethod
    def is_one_pair(hand):
        return list(map(itemgetter(1), Counter(hand).most_common())) == [2, 1, 1, 1]

    def _validate(hand):
        assert all(figure in FIGURE_SYMBOL for figure in hand)
        assert len(hand) == HAND_SIZE

    @classmethod
    def determine_hand_type(cls, hand):
        cls._validate(hand)
        for opt in list(cls)[:-1]:
            name = opt.name.lower()
            check_fn = getattr(cls, f"is_{name}")
            if check_fn(hand):
                return opt
        return cls.HIGH_CARD

    @classmethod
    def joker_update(cls, hand):
        no_of_jokers = hand.count("J")
        hand_without = hand.replace("J", "")
        if not hand_without:
            return hand
        c, _ = Counter(hand_without).most_common(1)[0]
        return hand.replace("J", c)

    @classmethod
    def determine_hand_type_with_joker(cls, hand):
        if "J" not in hand:
            return cls.determine_hand_type(hand)
        hand = cls.joker_update(hand)
        return cls.determine_hand_type(hand)

    @classmethod
    def get_order(cls):
        return [(opt, opt.value) for opt in cls]


def make_positional_comparator(LOOKUP):
    def compare_positional(hand1, hand2):
        for h1c, h2c in zip(hand1, hand2):
            h1cv = LOOKUP.get(h1c)
            h2cv = LOOKUP.get(h2c)
            if h1cv == h2cv:
                continue
            elif h1cv > h2cv:
                return 1
            else:
                return -1
        return 0
    return compare_positional


def make_strength_comparator(compare_positional, determine_hand_type):
    def compare_strength(hand1, hand2):
        type1 = determine_hand_type(hand1)
        type2 = determine_hand_type(hand2)
        if type1 == type2:
            return compare_positional(hand1, hand2)
        else:
            return 1 if type1.value < type2.value else -1
    return compare_strength


def create_hand_to_bid_lookup(lines):
    lookup = {}
    for line in lines:
        hand, bid = line.split(" ")
        bid = int(bid)
        lookup[hand] = bid
    return lookup


EXAMPLE_INPUT = """
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
""".strip()


def get_total_winnings(lines):
    compare_positional = make_positional_comparator(LOOKUP)
    compare_strength = make_strength_comparator(
        compare_positional,
        HandType.determine_hand_type,
    )
    lookup = create_hand_to_bid_lookup(lines)
    order = sorted(lookup.keys(), key=cmp_to_key(compare_strength))
    ranks = {v: k for k, v in dict(enumerate(order, start=1)).items()}
    return sum(lookup[h] * ranks[h] for h in lookup.keys())


def get_total_winnings_2(lines):
    compare_positional = make_positional_comparator(LOOKUP_2)
    compare_strength = make_strength_comparator(
        compare_positional,
        HandType.determine_hand_type_with_joker,
    )
    lookup = create_hand_to_bid_lookup(lines)
    order = sorted(lookup.keys(), key=cmp_to_key(compare_strength))
    ranks = {v: k for k, v in dict(enumerate(order, start=1)).items()}
    return sum(lookup[h] * ranks[h] for h in lookup.keys())


def example_one():
    print(get_total_winnings(EXAMPLE_INPUT.split("\n")))


def example_two():
    print(get_total_winnings_2(EXAMPLE_INPUT.split("\n")))


def part_one():
    lines = get_lines("input/07.txt")
    print(get_total_winnings(lines))


def part_two():
    lines = get_lines("input/07.txt")
    print(get_total_winnings_2(lines))


def main():
    example_one()
    example_two()

    part_one()
    part_two()


if __name__ == "__main__":
    main()