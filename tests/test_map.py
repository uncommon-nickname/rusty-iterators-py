from typing import Generator

from rusty_iterators import Iterator


class TestMap:
    def test_map_applies_passed_callable_to_every_element(self, gen: Generator[int, None, None]) -> None:
        result = Iterator(gen).map(lambda x: x + 5).collect()

        assert result == [6, 7, 8, 9]

    def test_map_has_no_effect_on_empty_iterator(self, empty_gen: Generator[int, None, None]) -> None:
        result = Iterator(empty_gen).map(lambda x: x + 5).collect()

        assert result == []


class TestMapCount:
    def test_map_counts_parent_items(self, gen: Generator[int, None, None]) -> None:
        result = Iterator(gen).map(lambda x: x + 1).count()

        assert result == 4

    def test_map_when_no_elements(self, empty_gen: Generator[int, None, None]) -> None:
        result = Iterator(empty_gen).map(lambda x: x + 1).count()

        assert result == 0
