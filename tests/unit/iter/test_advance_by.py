import pytest

from rusty_iterators import Iter, IterInterface, Value


@pytest.mark.parametrize(
    ("it", "expected"),
    (
        (Iter.from_items(1, 2, 3, 4).advance_by(2), [3, 4]),
        (Iter.from_items(1, 2, 3, 4).map(lambda x: x + 2).advance_by(2), [5, 6]),
        (Iter.from_items(1, 2, 3, 4).filter(lambda x: x != 1).advance_by(1), [3, 4]),
        (Iter.from_items(1, 2, 3, 4).cycle().advance_by(4), [1, 2]),
        (Iter.from_items(1, 2, 3, 4).enumerate().advance_by(2), [(2, 3), (3, 4)]),
        (Iter.from_items(1, 2, 3, 4).filter_map(lambda x: Value(x)).advance_by(2), [3, 4]),
        (Iter.from_items(1, 2, 3, 4).inspect(lambda _: None).advance_by(2), [3, 4]),
        (Iter.from_items(1, 2, 3, 4).step_by(2).advance_by(1), [3]),
        (Iter.from_items(1, 2).chain(Iter.from_items(3, 4)).advance_by(1), [2, 3, 4]),
        (Iter.from_items(1, 2, 3, 4).take(2).advance_by(1), [2]),
    ),
)
def test_advance_by(it: IterInterface[int], expected: list[int]) -> None:
    for item in expected:
        assert it.next() == item


@pytest.mark.parametrize(
    "it",
    (
        Iter.from_items().advance_by(2),
        Iter.from_items().map(lambda x: x + 1).advance_by(2),
        Iter.from_items().filter(lambda x: x != 0).advance_by(2),
        Iter.from_items().cycle().advance_by(2),
        Iter.from_items().enumerate().advance_by(2),
        Iter.from_items().filter_map(lambda x: Value(x)).advance_by(2),
        Iter.from_items().inspect(lambda _: None).advance_by(2),
        Iter.from_items().step_by(2).advance_by(2),
        Iter.from_items().chain(Iter.from_items()).advance_by(2),
        Iter.from_items().take(2).advance_by(2),
    ),
)
def test_advance_by_depleted(it: IterInterface[int]) -> None:
    with pytest.raises(StopIteration):
        it.next()


@pytest.mark.parametrize(
    "it",
    (
        Iter.from_items(),
        Iter.from_items().map(lambda x: x + 1),
        Iter.from_items().filter(lambda x: x != 0),
        Iter.from_items().cycle(),
        Iter.from_items().enumerate(),
        Iter.from_items().filter_map(lambda x: Value(x)),
        Iter.from_items().inspect(lambda _: None),
        Iter.from_items().step_by(2),
        Iter.from_items().chain(Iter.from_items()),
        Iter.from_items().take(2).advance_by(1),
    ),
)
def test_advance_by_negative_idx(it: IterInterface[int]) -> None:
    with pytest.raises(ValueError):
        it.advance_by(-1)
