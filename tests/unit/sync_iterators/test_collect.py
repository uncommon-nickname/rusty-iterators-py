import pytest

from rusty_iterators import IterInterface, NoValue, RustyIter, Value


@pytest.mark.parametrize(
    ("it", "expected"),
    (
        (RustyIter.from_items(1, 2, 3, 4), [1, 2, 3, 4]),
        (RustyIter.from_items(1, 2, 3, 4).map(lambda x: x + 1), [2, 3, 4, 5]),
        (RustyIter.from_items(1, 2, 3, 4).filter(lambda x: x % 2 == 0), [2, 4]),
        (RustyIter.from_items(1, 2, 3, 4).enumerate(), [(0, 1), (1, 2), (2, 3), (3, 4)]),
        (RustyIter.from_items(1, 2, 3, 4).filter_map(lambda x: Value(x**2) if x % 2 == 0 else NoValue()), [4, 16]),
        (RustyIter.from_items(1, 2, 3, 4).inspect(lambda _: None), [1, 2, 3, 4]),
        (RustyIter.from_items(1, 2, 3, 4).step_by(2), [1, 3]),
        (RustyIter.from_items(1, 2).chain(RustyIter.from_items(3, 4)), [1, 2, 3, 4]),
    ),
)
def test_collect_iterator(it: IterInterface[int], expected: list[int]) -> None:
    assert it.collect() == expected


@pytest.mark.parametrize(
    "it",
    (
        RustyIter.from_items(),
        RustyIter.from_items().map(lambda x: x + 1),
        RustyIter.from_items().filter(lambda x: x % 2 == 0),
        RustyIter.from_items().enumerate(),
        RustyIter.from_items().filter_map(lambda x: Value(x**2) if x % 2 == 0 else NoValue()),
        RustyIter.from_items().inspect(lambda _: None),
        RustyIter.from_items().step_by(2),
        RustyIter.from_items().chain(RustyIter.from_items()),
        RustyIter.from_items().take(2),
    ),
)
def test_collect_empty_iterator(it: IterInterface[int]) -> None:
    assert it.collect() == []


@pytest.mark.parametrize(
    ("it", "expected"),
    (
        (RustyIter.from_items(1, 2, 3, 4), {1, 2, 3, 4}),
        (RustyIter.from_items(1, 2, 3, 4).map(lambda x: x + 1), {2, 3, 4, 5}),
        (RustyIter.from_items(1, 2, 3, 4).filter(lambda x: x % 2 == 0), {2, 4}),
        (RustyIter.from_items(1, 2, 3, 4).enumerate(), {(0, 1), (1, 2), (2, 3), (3, 4)}),
        (RustyIter.from_items(1, 2, 3, 4).filter_map(lambda x: Value(x**2) if x % 2 == 0 else NoValue()), {4, 16}),
        (RustyIter.from_items(1, 2, 3, 4).inspect(lambda _: None), {1, 2, 3, 4}),
        (RustyIter.from_items(1, 2, 3, 4).step_by(2), {1, 3}),
        (RustyIter.from_items(1, 2).chain(RustyIter.from_items(3, 4)), {1, 2, 3, 4}),
    ),
)
def test_collect_into_set(it: IterInterface[int], expected: set[int]) -> None:
    assert it.collect_into(set) == expected
