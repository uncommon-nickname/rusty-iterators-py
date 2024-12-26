import pytest

from rusty_iterators import IterInterface, RustyIter, Value


@pytest.mark.parametrize(
    ("it", "expected"),
    (
        (RustyIter.from_items(1, 2, 3, 4).advance_by(2), [3, 4]),
        (RustyIter.from_items(1, 2, 3, 4).map(lambda x: x + 2).advance_by(2), [5, 6]),
        (RustyIter.from_items(1, 2, 3, 4).filter(lambda x: x != 1).advance_by(1), [3, 4]),
        (RustyIter.from_items(1, 2, 3, 4).enumerate().advance_by(2), [(2, 3), (3, 4)]),
        (RustyIter.from_items(1, 2, 3, 4).filter_map(lambda x: Value(x)).advance_by(2), [3, 4]),
        (RustyIter.from_items(1, 2, 3, 4).inspect(lambda _: None).advance_by(2), [3, 4]),
        (RustyIter.from_items(1, 2, 3, 4).step_by(2).advance_by(1), [3]),
        (RustyIter.from_items(1, 2).chain(RustyIter.from_items(3, 4)).advance_by(1), [2, 3, 4]),
        (RustyIter.from_items(1, 2, 3, 4).take(2).advance_by(1), [2]),
        (RustyIter.from_items(1, 2, 3, 4).cycle().advance_by(3), [4, 1]),
        (RustyIter.from_items(1, 2, 3, 4).windows(2).advance_by(1), [[2, 3], [3, 4]]),
        (RustyIter.from_items(1, 2).zip(RustyIter.from_items("a", "b")).advance_by(1), [(2, "b")]),
    ),
)
def test_advance_by(it: IterInterface[int], expected: list[int]) -> None:
    for item in expected:
        assert it.next() == item


@pytest.mark.parametrize(
    "it",
    (
        RustyIter.from_items().advance_by(2),
        RustyIter.from_items().map(lambda x: x + 1).advance_by(2),
        RustyIter.from_items().filter(lambda x: x != 0).advance_by(2),
        RustyIter.from_items().enumerate().advance_by(2),
        RustyIter.from_items().filter_map(lambda x: Value(x)).advance_by(2),
        RustyIter.from_items().inspect(lambda _: None).advance_by(2),
        RustyIter.from_items().step_by(2).advance_by(2),
        RustyIter.from_items().chain(RustyIter.from_items()).advance_by(2),
        RustyIter.from_items().take(2).advance_by(2),
        RustyIter.from_items().cycle().advance_by(3),
        RustyIter.from_items().windows(2).advance_by(2),
        RustyIter.from_items().zip(RustyIter.from_items()).advance_by(2),
    ),
)
def test_advance_by_depleted(it: IterInterface[int]) -> None:
    with pytest.raises(StopIteration):
        it.next()


@pytest.mark.parametrize(
    "it",
    (
        RustyIter.from_items(),
        RustyIter.from_items().map(lambda x: x + 1),
        RustyIter.from_items().filter(lambda x: x != 0),
        RustyIter.from_items().enumerate(),
        RustyIter.from_items().filter_map(lambda x: Value(x)),
        RustyIter.from_items().inspect(lambda _: None),
        RustyIter.from_items().step_by(2),
        RustyIter.from_items().chain(RustyIter.from_items()),
        RustyIter.from_items().take(2),
        RustyIter.from_items().cycle(),
        RustyIter.from_items().windows(2),
        RustyIter.from_items().zip(RustyIter.from_items()),
    ),
)
def test_advance_by_negative_idx(it: IterInterface[int]) -> None:
    with pytest.raises(ValueError):
        it.advance_by(-1)
