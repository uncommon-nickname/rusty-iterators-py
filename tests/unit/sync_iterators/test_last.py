import pytest

from rusty_iterators import IterInterface, NoValue, RustyIter, Value


@pytest.mark.parametrize(
    ("it", "expected"),
    (
        (RustyIter.from_items(1, 2, 3, 4), 4),
        (RustyIter.from_items(1, 2, 3, 4).map(lambda x: x + 1), 5),
        (RustyIter.from_items(1, 2, 3, 4).filter(lambda x: x % 2 == 0), 4),
        (RustyIter.from_items(1, 2, 3, 4).enumerate(), (3, 4)),
        (RustyIter.from_items(1, 2, 3, 4).filter_map(lambda x: Value(x**2) if x % 2 == 0 else NoValue()), 16),
        (RustyIter.from_items(1, 2, 3, 4).inspect(lambda _: None), 4),
        (RustyIter.from_items(1, 2, 3, 4).step_by(2), 3),
        (RustyIter.from_items(1, 2).chain(RustyIter.from_items(3, 4)), 4),
        (RustyIter.from_items(1, 2, 3, 4).take(2), 2),
        (RustyIter.from_items(1, 2, 3, 4).moving_window(2), [3, 4]),
        (RustyIter.from_items(1, 2).zip(RustyIter.from_items(3, 4)), (2, 4)),
    ),
)
def test_last(it: IterInterface[int], expected: int) -> None:
    assert it.last() == expected


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
        RustyIter.from_items().take(5),
        RustyIter.from_items().moving_window(2),
    ),
)
def test_last_on_empty_iter(it: IterInterface[int]) -> None:
    with pytest.raises(StopIteration):
        it.last()
