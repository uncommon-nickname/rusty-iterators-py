from typing import Iterator

from rusty_iterators.iter import Iter


class TestCycle:
    def test_cycle_repeats_itself(self, gen: Iterator[int]) -> None:
        it = Iter(gen).cycle()

        result = []
        for _ in range(10):
            if (item := it.next()).exists:
                result.append(item.value)

        assert result == [1, 2, 3, 4, 1, 2, 3, 4, 1, 2]

    def test_cycle_on_empty_iterator(self, empty_gen: Iterator[int]) -> None:
        it = Iter(empty_gen).cycle()

        assert it.next().exists is False
        assert it.next().exists is False


class TestCycleCopy:
    def test_copied_iterator_depletes_separately(self, gen: Iterator[int]) -> None:
        it_orig = Iter(gen).cycle()
        it_copy = it_orig.copy()

        item = it_orig.next()
        assert item.exists and item.value == 1

        item = it_copy.next()
        assert item.exists and item.value == 1
