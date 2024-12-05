from typing import Generator

from rusty_iterators import Iterator


class TestIteratorConstructors:
    def test_from_items_builds_a_generator(self) -> None:
        it = Iterator.from_items(1, 2, 3)

        assert [x for x in it.gen] == [1, 2, 3]

    def test_from_iterable_builds_a_generator(self) -> None:
        arr = [1, 2, 3]
        it = Iterator.from_iterable(arr)

        assert [x for x in it.gen] == arr


class TestIteratorNext:
    def test_next_advances_an_iterator(self, gen: Generator[int, None, None]) -> None:
        it = Iterator(gen)

        assert it.next() == 1
        assert it.next() == 2

    def test_next_returns_none_when_iterator_is_depleted(self, empty_gen: Generator[int, None, None]) -> None:
        it = Iterator(empty_gen)

        assert it.next() is None


class TestIteratorCollect:
    def test_collect_iterator_to_list(self, gen: Generator[int, None, None]) -> None:
        result = Iterator(gen).collect()

        assert result == [1, 2, 3, 4]

    def test_iterator_cannot_be_collected_multiple_times(self, gen: Generator[int, None, None]) -> None:
        it = Iterator(gen)

        assert it.collect() == [1, 2, 3, 4]
        assert it.collect() == []


class TestIteratorCount:
    def test_count_returns_amount_of_elements(self, gen: Generator[int, None, None]) -> None:
        result = Iterator(gen).count()

        assert result == 4

    def test_count_on_empty_iterator(self, empty_gen: Generator[int, None, None]) -> None:
        result = Iterator(empty_gen).count()

        assert result == 0
