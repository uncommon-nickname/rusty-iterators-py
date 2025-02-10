import pytest

from rusty_iterators import LIter
from rusty_iterators.core.interface import CacheMovingWindow, CopyMovingWindow


def test_build_cached_iterator() -> None:
    it = LIter.from_items(1, 2, 3).moving_window(2)

    assert type(it) is CacheMovingWindow


def test_build_copy_iterator() -> None:
    it = LIter.from_items(1, 2, 3).moving_window(2, use_cache=False)

    assert type(it) is CopyMovingWindow


@pytest.mark.parametrize("use_cache", (True, False))
def test_next_returns_windows(use_cache: bool) -> None:
    it = LIter.from_items(1, 2, 3, 4).moving_window(2, use_cache)

    assert it.next() == [1, 2]
    assert it.next() == [2, 3]
    assert it.next() == [3, 4]


@pytest.mark.parametrize("use_cache", (True, False))
def test_collect(use_cache: bool) -> None:
    assert LIter.from_items(1, 2, 3, 4).moving_window(2, use_cache).collect() == [[1, 2], [2, 3], [3, 4]]


@pytest.mark.parametrize("use_cache", (True, False))
def test_can_be_copied(use_cache: bool) -> None:
    it = LIter.from_items(1, 2, 3, 4).moving_window(2, use_cache)
    it.next()

    assert it.can_be_copied()

    cp = it.copy()

    assert it.collect() == cp.collect() == [[2, 3], [3, 4]]


@pytest.mark.parametrize("use_cache", (True, False))
def test_size_has_to_be_at_least_one(use_cache: bool) -> None:
    with pytest.raises(ValueError):
        LIter.from_items(1, 2, 3).moving_window(0, use_cache)
