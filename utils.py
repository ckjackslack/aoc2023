import math
import sys
from collections import defaultdict
from enum import IntEnum
from functools import reduce
from itertools import zip_longest
from operator import add
from typing import List


class ScanOutcome(IntEnum):
    ROWS_EQUAL_LENGTH = 0
    ROWS_JAGGED = 1
    ROWS_EMPTY = 2
    ROWS_1D_EMPTY = 3


def get_lines(filename):
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if line:
                yield line


def apply(e, *funcs):
    for func in funcs:
        e = func(e)
    return e


def double(x):
    return x * x


def incr(x):
    return x + 1


def decr(x):
    return x - 1


def identity(x):
    return x


def get_lines_with_hooks(
    filename,
    preprocess=identity,
    condition=None,
    postprocess=identity,
):
    def _f(line, process):
        return (
            process(line)
            if callable(process)
            else apply(line, *process)
        )
    with open(filename) as f:
        for line in f:
            line = _f(line, preprocess)
            if condition is not None:
                if condition(line):
                    yield _f(line, postprocess)
            else:
                yield _f(line, postprocess)


def find_all_positions(where, what):
    positions = []
    cur = 0
    while True:
        pos = where.find(what, cur)
        if pos != -1:
            positions.append(pos)
            cur = pos + 1
        else:
            break
    return positions


def put_on_positions(line, positions, strip=False):
    s = "x" * len(line)
    for what, where in positions.items():
        for who in where:
            s = s[:who] + str(what) + s[who:]
    return s if not strip else s.replace("x", "")


def sliding_window_non_overlap(s, n=1):
    assert s
    assert 0 < n <= len(s)
    cur = 0
    while True:
        part = s[cur:cur+n]
        cur += n
        if part:
            yield part
        else:
            break


def sliding_window_overlap(s, n=2):
    assert s
    assert 0 < n <= len(s)
    cur = 0
    while True:
        part = s[cur:cur+n]
        cur += 1
        if len(part) == n:
            yield part
        else:
            break


def group_by(items, key_fn):
    assert callable(key_fn)
    dd = defaultdict(list)
    for item in items:
        dd[key_fn(item)].append(item)
    return dd


def concat_lists(lists):
    return reduce(add, lists, [])


def get_chars(obj, only_char=False):
    def iterate_over(it, only_char):
        for row, line in enumerate(it):
            line = line.strip()
            for column, char in enumerate(line):
                if only_char:
                    yield char
                else:
                    yield (char, row, column)

    if hasattr(obj, "read") or isinstance(obj, list):
        yield from iterate_over(obj, only_char)
    else:
        with open(obj) as f:
            yield from iterate_over(f, only_char)


def scan_rows(numeric_nested_list: List[List[int|float]]) -> ScanOutcome:
    sizes = []
    largest, lowest = -1, sys.maxsize
    for row in numeric_nested_list:
        size = len(row)
        if size > largest:
            largest = size
        if size < lowest:
            lowest = size
        sizes.append(size)
    if sum(sizes) != 0:
        first = sizes[0]
        if all(first == e for e in sizes[1:]):
            return ScanOutcome.ROWS_EQUAL_LENGTH
        else:
            return ScanOutcome.ROWS_JAGGED
    elif len(sizes) == 0:
        return ScanOutcome.ROWS_1D_EMPTY
    else:
        return ScanOutcome.ROWS_EMPTY


def sum_column_naive(numeric_nested_list):
    total = 0
    for row in numeric_nested_list:
        try:
            total += row[col_num]
        except:
            continue
    return total


def sum_column_inline(numeric_nested_list):
    return sum(a_list[col_num] for a_list in numeric_nested_list)


def sum_column(numeric_nested_list, col_num):
    scan_outcome = scan_rows(numeric_nested_list)
    if scan_outcome in {ScanOutcome.ROWS_EMPTY, ScanOutcome.ROWS_1D_EMPTY}:
        return 0
    elif scan_outcome == ScanOutcome.ROWS_EQUAL_LENGTH:
        assert col_num < len(numeric_nested_list[0]), "Index out of range"
        return sum_column_inline(numeric_nested_list)
    else:
        return sum_column_naive(numeric_nested_list)


def get_elements_for_mask(seq, masks):
    assert max(masks) <= len(seq)
    return {
        m: seq[m]
        for m
        in masks
    }


def chunks_iterative(seq, part_size):
    size = len(seq)
    assert 0 < part_size <= size
    yield from [
        seq[i:i+part_size]
        for i
        in range(size - part_size + 1)
    ]


def chunks_step_by_step(seq, part_size):
    size = len(seq)
    assert 0 < part_size <= size
    i = 0
    while True:
        chunk = seq[i*part_size:i*part_size+part_size]
        if chunk:
            yield chunk
            i += 1
        else:
            break


def get_right_diagonal(numeric_nested_list):
    i = 0
    for row in numeric_nested_list:
        yield row[i]
        i += 1


def get_left_diagonal(numeric_nested_list):
    j = len(numeric_nested_list) - 1
    for row in numeric_nested_list:
        yield row[j]
        j -= 1


def transpose(numeric_nested_list):
    return list(zip_longest(*numeric_nested_list))


def traverse_nested(data):
    stack = data
    while len(stack) > 0:
        e = stack.pop()
        if isinstance(e, list):
            stack.extend(e)
        else:
            yield e


def take_while(seq, predicate):
    for e in seq:
        if predicate(e):
            yield e
        else:
            break


def drop_while(seq, predicate):
    for i, e in enumerate(seq):
        if predicate(e):
            continue
        else:
            yield from seq[i:]


def only_digits(string):
    return "".join(c for c in string if c.isdigit())


def without_digits(string):
    return "".join(c for c in string if not c.isdigit())


"""
for line in get_lines_with_hooks(
    "input/01.txt",
    preprocess=str.strip,
    condition=lambda line: "sss" in line,
    postprocess=without_digits,
):
    print(line)
"""