from typing import Iterator

import pytest

from rusty_iterators.iter import Iter


class TestCycle:
    def test_cycle_repeats_itself(self, gen: Iterator[int]) -> None:
        it = Iter(gen).cycle()
        result = [it.next() for _ in range(10)]

        assert result == [1, 2, 3, 4, 1, 2, 3, 4, 1, 2]

    def test_cycle_on_empty_iterator(self, empty_gen: Iterator[int]) -> None:
        with pytest.raises(StopIteration):
            Iter(empty_gen).cycle().next()


class TestCycleCopy:
    def test_copied_iterator_depletes_separately(self, gen: Iterator[int]) -> None:
        it_orig = Iter(gen).cycle()
        it_copy = it_orig.copy()

        assert it_orig.next() == 1
        assert it_copy.next() == 1
