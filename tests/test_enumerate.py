from typing import Iterator

from rusty_iterators.iter import Iter


class TestEnumerate:
    def test_enumerate_keeps_track_of_idx(self, gen: Iterator[int]) -> None:
        result = Iter(gen).enumerate().collect()

        assert result == [(0, 1), (1, 2), (2, 3), (3, 4)]

    def test_enumerate_can_be_iterated_over(self, gen: Iterator[int]) -> None:
        it = Iter(gen).enumerate()

        assert [x for x in it] == [(0, 1), (1, 2), (2, 3), (3, 4)]

    def test_enumerate_next(self, gen: Iterator[int]) -> None:
        it = Iter(gen).enumerate()

        item = it.next()
        assert item.exists and item.value == (0, 1)
