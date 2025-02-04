from rusty_iterators import LIter
from rusty_iterators.core.interface import CacheCycle, CopyCycle


def test_default_iterator_returns_cache_based_cycle() -> None:
    _iter = (x for x in [1, 2, 3])
    it = LIter.from_it(_iter).cycle()

    assert isinstance(it, CacheCycle)
    assert [it.next() for _ in range(7)] == [1, 2, 3, 1, 2, 3, 1]


def test_when_specified_cycle_returns_cached() -> None:
    it = LIter.from_items("a", "b", "c").cycle(use_cache=True)

    assert isinstance(it, CacheCycle)
    assert [it.next() for _ in range(7)] == ["a", "b", "c", "a", "b", "c", "a"]


def test_when_specified_cycle_returns_copy() -> None:
    it = LIter.from_items("a", "b", "c").cycle(use_cache=False)

    assert isinstance(it, CopyCycle)
    assert [it.next() for _ in range(7)] == ["a", "b", "c", "a", "b", "c", "a"]


def test_copy_cycle_can_be_copied() -> None:
    it = LIter.from_items(1, 2).cycle(use_cache=False)
    it.next()

    assert it.can_be_copied()

    cp = it.copy()

    assert cp.next() == it.next() == 2
    assert cp.next() == it.next() == 1
    assert cp.next() == it.next() == 2


def test_cache_cycle_can_be_copied() -> None:
    it = LIter.from_items(1, 2).cycle(use_cache=True)
    it.next()

    assert it.can_be_copied()

    cp = it.copy()

    assert cp.next() == it.next() == 2
    assert cp.next() == it.next() == 1
    assert cp.next() == it.next() == 2
