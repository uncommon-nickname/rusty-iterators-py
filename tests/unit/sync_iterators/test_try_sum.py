import pytest

from rusty_iterators import RustyIter


def test_try_sum_iterator() -> None:
    it = RustyIter.from_items(1, 2, 3, 4).map(lambda x: x + 1)

    assert it.try_sum() == 2 + 3 + 4 + 5


def test_try_sum_fails_if_items_cannot_be_added() -> None:
    it = RustyIter.from_items(object(), object())

    with pytest.raises(TypeError):
        it.try_sum()


def test_try_sum_fails_if_no_items_in_iterator() -> None:
    it = RustyIter[int].from_items()

    with pytest.raises(StopIteration):
        it.try_sum()
