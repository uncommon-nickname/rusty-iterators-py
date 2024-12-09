import pytest

from rusty_iterators import IterInterface, NoValue, RustyIter, Value
from rusty_iterators.sync_iterators import CycleCached, CycleCopy


@pytest.mark.parametrize(
    "it",
    (
        RustyIter.from_items(1, 2, 3).filter(lambda x: x > 1),
        RustyIter.from_items(1, 2, 3).map(lambda x: x**2),
        RustyIter.from_items(1, 2, 3).filter_map(lambda x: Value(x**2) if x > 1 else NoValue()),
        RustyIter.from_items(1, 2, 3).inspect(),
    ),
)
def test_trivially_copiable_iterators(it: IterInterface[int]) -> None:
    copy = it.copy()

    assert it.next() == copy.next()
    assert it.next() == copy.next()


def test_copy_cycle_copy() -> None:
    it = RustyIter.from_items(1, 2, 3).cycle()
    it.next()
    copy = it.copy()

    it.advance_by(2)

    assert isinstance(copy, CycleCopy)

    assert [it.next() for _ in range(5)] == [1, 2, 3, 1, 2]
    assert [copy.next() for _ in range(5)] == [2, 3, 1, 2, 3]


def test_copy_cycle_cached() -> None:
    it = CycleCached(RustyIter.from_items(1, 2, 3))
    it.next()
    copy = it.copy()

    it.advance_by(2)

    assert [it.next() for _ in range(5)] == [1, 2, 3, 1, 2]
    assert [copy.next() for _ in range(5)] == [2, 3, 1, 2, 3]


def test_copy_chain() -> None:
    it = RustyIter.from_items(1, 2, 3).chain(RustyIter.from_items(4, 5, 6))
    it.next()
    copy = it.copy()

    it.advance_by(2)

    assert it.collect() == [4, 5, 6]
    assert copy.collect() == [2, 3, 4, 5, 6]


def test_copy_enumerate() -> None:
    it = RustyIter.from_items(1, 2, 3, 4).enumerate()
    it.next()
    copy = it.copy()

    it.advance_by(2)

    assert it.collect() == [(3, 4)]
    assert copy.collect() == [(1, 2), (2, 3), (3, 4)]


def test_copy_step_by() -> None:
    it = RustyIter.from_items(1, 2, 3, 4, 5, 6, 7, 8, 9).step_by(2)
    it.next()
    copy = it.copy()

    it.advance_by(2)

    assert it.collect() == [7, 9]
    assert copy.collect() == [3, 5, 7, 9]


def test_copy_take() -> None:
    it = RustyIter.from_items(1, 2, 3, 4, 5).take(4)
    it.next()
    copy = it.copy()

    it.advance_by(2)

    assert it.collect() == [4]
    assert copy.collect() == [2, 3, 4]
