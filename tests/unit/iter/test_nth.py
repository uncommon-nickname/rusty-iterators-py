import pytest

from rusty_iterators import Iter, IterInterface, NoValue, Value


@pytest.mark.parametrize(
    ("it", "expected"),
    (
        (Iter.from_items(1, 2, 3, 4), 1),
        (Iter.from_items(1, 2, 3, 4).map(lambda x: x + 1), 2),
        (Iter.from_items(1, 2, 3, 4).filter(lambda x: x % 2 == 0), 2),
        (Iter.from_items(1, 2, 3, 4).cycle().advance_by(4), 1),
        (Iter.from_items(1, 2, 3, 4).enumerate(), (0, 1)),
        (Iter.from_items(1, 2, 3, 4).filter_map(lambda x: Value(x**2) if x % 2 == 0 else NoValue()), 4),
        (Iter.from_items(1, 2, 3, 4).inspect(lambda _: None), 1),
        (Iter.from_items(1, 2, 3, 4).step_by(2), 1),
        (Iter[int].from_items().chain(Iter.from_items(1, 2)), 1),
    ),
)
def test_nth(it: IterInterface[int], expected: int) -> None:
    item = it.nth(0)
    assert item.exists and item.value == expected


@pytest.mark.parametrize(
    "it",
    (
        Iter.from_items(),
        Iter.from_items().map(lambda x: x + 1),
        Iter.from_items().filter(lambda x: x % 2 == 0),
        Iter.from_items().cycle(),
        Iter.from_items().enumerate(),
        Iter.from_items().filter_map(lambda x: Value(x**2) if x % 2 == 0 else NoValue()),
        Iter.from_items().inspect(lambda _: None),
        Iter.from_items().step_by(2),
        Iter.from_items().chain(Iter.from_items()),
    ),
)
def test_nth_empty_iterator(it: IterInterface[int]) -> None:
    item = it.nth(0)
    assert not item.exists
