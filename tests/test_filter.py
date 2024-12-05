from typing import Generator

from rusty_iterators import Iterator


class TestFilter:
    def test_filter_returns_only_correct_elements(self, gen: Generator[int, None, None]) -> None:
        result = Iterator(gen).filter(lambda x: x % 2 == 0).collect()

        assert result == [2, 4]

    def test_filter_returns_nothing_if_no_item_fits(self, gen: Generator[int, None, None]) -> None:
        result = Iterator(gen).filter(lambda x: x > 10).collect()

        assert result == []


class TestFilterCount:
    def test_filter_returns_count_of_filtered_elements(self, gen: Generator[int, None, None]) -> None:
        result = Iterator(gen).filter(lambda x: x % 2 == 0).count()

        assert result == 2

    def test_filter_when_no_elements(self, empty_gen: Generator[int, None, None]) -> None:
        result = Iterator(empty_gen).filter(lambda x: x % 2 == 0).count()

        assert result == 0

    def test_multiple_filters_count(self, gen: Generator[int, None, None]) -> None:
        result = Iterator(gen).filter(lambda x: x % 2 == 0).filter(lambda x: x == 2).count()

        assert result == 1
