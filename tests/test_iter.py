from typing import Iterator

from rusty_iterators import Iter


class TestIteratorConstructors:
    def test_from_items_builds_a_generator(self) -> None:
        it = Iter.from_items(1, 2, 3)

        assert [x for x in it.gen] == [1, 2, 3]

    def test_from_iterable_builds_a_generator(self) -> None:
        arr = [1, 2, 3]
        it = Iter.from_iterable(arr)

        assert [x for x in it.gen] == arr


class TestIteratorNext:
    def test_next_advances_an_iterator(self, gen: Iterator[int]) -> None:
        it = Iter(gen)

        assert it.next() == 1
        assert it.next() == 2

    def test_next_returns_none_when_iterator_is_depleted(self, empty_gen: Iterator[int]) -> None:
        it = Iter(empty_gen)

        assert it.next() is None


class TestIteratorCollect:
    def test_collect_iterator_to_list(self, gen: Iterator[int]) -> None:
        result = Iter(gen).collect()

        assert result == [1, 2, 3, 4]

    def test_iterator_cannot_be_collected_multiple_times(self, gen: Iterator[int]) -> None:
        it = Iter(gen)

        assert it.collect() == [1, 2, 3, 4]
        assert it.collect() == []


class TestIteratorCount:
    def test_count_returns_amount_of_elements(self, gen: Iterator[int]) -> None:
        result = Iter(gen).count()

        assert result == 4

    def test_count_on_empty_iterator(self, empty_gen: Iterator[int]) -> None:
        result = Iter(empty_gen).count()

        assert result == 0
