import pytest

from rusty_iterators import LIter


def test_collects_correct_amount_of_items() -> None:
    assert LIter.from_items(1, 2, 3, 4).take(3).collect() == [1, 2, 3]


@pytest.mark.parametrize("amount", (0, -1))
def test_take_zero_items(amount: int) -> None:
    with pytest.raises(Exception):
        LIter.from_items(1, 2, 3).take(amount)


def test_take_can_be_copied() -> None:
    it = LIter.from_items(1, 2, 3).take(2)
    it.next()

    cp = it.copy()

    assert it.collect() == cp.collect() == [2]
