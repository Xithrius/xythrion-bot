import re

WHITESPACE_PATTERN = re.compile(r"\s+")
TUPLE_3D_INT_PATTERN = re.compile(r"^\((-?\d+),(-?\d+),(-?\d+)\)$")


def remove_whitespace(s: str) -> str:
    s = s.lower()

    return re.sub(WHITESPACE_PATTERN, "", s)


def str_to_tuple3(s: str) -> tuple[int, ...]:
    s = s.lower()

    if (m := re.match(TUPLE_3D_INT_PATTERN, s)) is None:
        raise ValueError("No groups found in match")

    groups = m.groups()

    int3 = tuple(int(x) for x in groups)

    return int3
