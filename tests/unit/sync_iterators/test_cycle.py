from rusty_iterators import RustyIter
from rusty_iterators.iterators._sync import CycleCached, CycleCopy


def test_default_iterator_returns_cache_based_cycle() -> None:
    it = RustyIter.from_it(x for x in [1, 2, 3]).cycle()

    assert not it.can_be_copied()
    assert isinstance(it, CycleCached)


def test_when_specified_cycle_returns_cached() -> None:
    it = RustyIter.from_items(1, 2, 3).cycle(use_cache=True)

    assert isinstance(it, CycleCached)


def test_when_specified_cycle_returns_copy() -> None:
    it = RustyIter.from_items(1, 2, 3).cycle(use_cache=False)

    assert isinstance(it, CycleCopy)


def test_cache_cycle_caches_only_n_elements() -> None:
    it = RustyIter.from_it(x for x in [1, 2, 3]).cycle()
    it.take(20).collect()

    assert isinstance(it, CycleCached)
    assert it.cache == [1, 2, 3]
