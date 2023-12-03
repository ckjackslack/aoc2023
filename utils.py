from collections import defaultdict
from functools import reduce
from operator import add


def get_lines(filename):
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if line:
                yield line


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
