import pytest

from rusty_iterators import Iter, IterInterface, NoValue, Value


@pytest.mark.parametrize(
    ("it", "expected"),
    (
        (Iter.from_items(1, 2, 3, 4), [1, 2, 3, 4]),
        (Iter.from_items(1, 2, 3, 4).map(lambda x: x + 1), [2, 3, 4, 5]),
        (Iter.from_items(1, 2, 3, 4).filter(lambda x: x % 2 == 0), [2, 4]),
        (Iter.from_items(1, 2, 3, 4).enumerate(), [(0, 1), (1, 2), (2, 3), (3, 4)]),
        (Iter.from_items(1, 2, 3, 4).filter_map(lambda x: Value(x**2) if x % 2 == 0 else NoValue()), [4, 16]),
        (Iter.from_items(1, 2, 3, 4).inspect(lambda _: None), [1, 2, 3, 4]),
    ),
)
def test_collect_iterator(it: IterInterface[int], expected: list[int]) -> None:
    assert it.collect() == expected


@pytest.mark.parametrize(
    "it",
    (
        Iter.from_items(),
        Iter.from_items().map(lambda x: x + 1),
        Iter.from_items().filter(lambda x: x % 2 == 0),
        Iter.from_items().enumerate(),
        Iter.from_items().filter_map(lambda x: Value(x**2) if x % 2 == 0 else NoValue()),
        Iter.from_items().inspect(lambda _: None),
    ),
)
def test_collect_empty_iterator(it: IterInterface[int]) -> None:
    assert it.collect() == []


@pytest.mark.parametrize(
    ("it", "expected"),
    (
        (Iter.from_items(1, 2, 3, 4), {1, 2, 3, 4}),
        (Iter.from_items(1, 2, 3, 4).map(lambda x: x + 1), {2, 3, 4, 5}),
        (Iter.from_items(1, 2, 3, 4).filter(lambda x: x % 2 == 0), {2, 4}),
        (Iter.from_items(1, 2, 3, 4).enumerate(), {(0, 1), (1, 2), (2, 3), (3, 4)}),
        (Iter.from_items(1, 2, 3, 4).filter_map(lambda x: Value(x**2) if x % 2 == 0 else NoValue()), {4, 16}),
        (Iter.from_items(1, 2, 3, 4).inspect(lambda _: None), {1, 2, 3, 4}),
    ),
)
def test_collect_into_set(it: IterInterface[int], expected: set[int]) -> None:
    assert it.collect_into(set) == expected
