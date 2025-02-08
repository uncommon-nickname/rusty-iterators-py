import pytest

from rusty_iterators import LIter


def test_step_by_next() -> None:
    it = LIter.from_items(1, 2, 3, 4).step_by(2)

    assert it.next() == 1
    assert it.next() == 3


def test_step_by_collect() -> None:
    assert LIter.from_items(1, 2, 3, 4).step_by(2).collect() == [1, 3]


def test_step_by_can_be_copied() -> None:
    it = LIter.from_items(1, 2, 3).step_by(2)
    it.next()

    assert it.can_be_copied()

    cp = it.copy()

    assert it.collect() == cp.collect() == [3]


@pytest.mark.parametrize("step", (0, -1))
def test_empty_step_by(step: int) -> None:
    with pytest.raises(ValueError):
        LIter.from_items(1, 2, 3).step_by(step)
