import pytest

from rusty_iterators import Iter, IterInterface, NoValue, Value


@pytest.mark.parametrize(
    ("it", "expected"),
    (
        (Iter.from_items(1, 2, 3, 4), 4),
        (Iter.from_items(1, 2, 3, 4).map(lambda x: x + 1), 5),
        (Iter.from_items(1, 2, 3, 4).filter(lambda x: x % 2 == 0), 4),
        (Iter.from_items(1, 2, 3, 4).enumerate(), (3, 4)),
        (Iter.from_items(1, 2, 3, 4).filter_map(lambda x: Value(x**2) if x % 2 == 0 else NoValue()), 16),
        (Iter.from_items(1, 2, 3, 4).inspect(lambda _: None), 4),
    ),
)
def test_last(it: IterInterface[int], expected: int) -> None:
    item = it.last()
    assert item.exists and item.value == expected


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
def test_last_on_empty_iter(it: IterInterface[int]) -> None:
    item = it.last()
    assert not item.exists
