import pytest

from rusty_iterators import IterInterface, NoValue, RustyIter, Value


@pytest.mark.parametrize(
    ("it", "expected"),
    (
        (RustyIter.from_items(1, 2), 1),
        (RustyIter.from_items(1, 2).map(lambda x: x + 1), 2),
        (RustyIter.from_items(1, 2).filter(lambda x: x != 1), 2),
        (RustyIter.from_items(1, 2).enumerate(), (0, 1)),
        (RustyIter.from_items(1, 2).filter_map(lambda x: Value(x**2) if x % 2 == 0 else NoValue()), 4),
        (RustyIter.from_items(1, 2).inspect(lambda _: None), 1),
        (RustyIter.from_items(1, 2).step_by(2), 1),
        (RustyIter[int].from_items().chain(RustyIter.from_items(3, 4)), 3),
        (RustyIter.from_items(1, 2, 3).take(2), 1),
        (RustyIter.from_items(1, 2, 3).cycle(), 1),
    ),
)
def test_next(it: IterInterface[int], expected: int) -> None:
    assert it.next() == expected


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
        RustyIter.from_items().cycle(),
    ),
)
def test_next_on_empty_iterator(it: IterInterface[int]) -> None:
    with pytest.raises(StopIteration):
        it.next()
