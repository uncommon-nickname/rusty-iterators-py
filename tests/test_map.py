from typing import Iterator

from rusty_iterators import Iter


class TestMap:
    def test_map_applies_passed_callable_to_every_element(self, gen: Iterator[int]) -> None:
        result = Iter(gen).map(lambda x: x + 5).collect()

        assert result == [6, 7, 8, 9]

    def test_map_has_no_effect_on_empty_iterator(self, empty_gen: Iterator[int]) -> None:
        result = Iter(empty_gen).map(lambda x: x + 5).collect()

        assert result == []


class TestMapCount:
    def test_map_counts_parent_items(self, gen: Iterator[int]) -> None:
        result = Iter(gen).map(lambda x: x + 1).count()

        assert result == 4

    def test_map_when_no_elements(self, empty_gen: Iterator[int]) -> None:
        result = Iter(empty_gen).map(lambda x: x + 1).count()

        assert result == 0


class TestMapCopy:
    def test_copied_iterator_depletes_separately(self, gen: Iterator[int]) -> None:
        it_orig = Iter(gen).map(lambda x: x * 2)
        it_copy = it_orig.copy()

        assert it_orig.collect() == [2, 4, 6, 8]
        assert it_copy.collect() == [2, 4, 6, 8]
