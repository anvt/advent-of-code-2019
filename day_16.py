from itertools import cycle, accumulate


def read(file):
    with open(file, "r") as f:
        return f.readline()


def get_pattern(n):
    def inner():
        for i in cycle([0, 1, 0, -1]):
            for _ in range(n):
                yield i

    iterator = inner()
    next(iterator)
    yield from iterator


def apply_pattern(signal, n):
    result = [x * y for x, y in zip(signal, get_pattern(n))]
    return abs(sum(result)) % 10


def phase(signal):
    return [apply_pattern(signal, i) for i in range(1, len(signal) + 1)]


def part_one():
    signal = list(map(int, read("inputs/day_16.txt")))

    for _ in range(100):
        signal = phase(signal)

    return int("".join(map(str, signal[:8])))


def part_two():
    signal = read("inputs/day_16.txt") * 10000

    offset = int(signal[:7])
    signal = [int(i) for i in signal][offset:][::-1]

    for _ in range(100):
        signal = list(accumulate(signal, lambda a, b: (a + b) % 10))

    return int("".join(map(str, signal[::-1][:8])))
