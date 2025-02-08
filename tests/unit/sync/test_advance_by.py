import pytest

from rusty_iterators import LIter


def test_advance_by() -> None:
    it = LIter.from_items(1, 2, 3, 4).map(lambda x: x + 2).advance_by(2)
    assert it.collect() == [5, 6]


def test_advance_by_depleted() -> None:
    with pytest.raises(StopIteration):
        LIter.from_items().advance_by(2).next()


def test_advance_by_negative_idx() -> None:
    with pytest.raises(ValueError):
        LIter.from_items().advance_by(-1)
