from typing import Generator

import pytest

from rusty_iterators import Iterator

type IntGen = Generator[int, None, None]


@pytest.fixture
def empty_gen() -> IntGen:
    empty: list[int] = []
    return (x for x in empty)


@pytest.fixture
def gen() -> IntGen:
    return (x for x in [1, 2, 3, 4])


class TestIteratorConstructors:
    def test_from_items_builds_a_generator(self) -> None:
        it = Iterator.from_items(1, 2, 3)

        assert [x for x in it.gen] == [1, 2, 3]

    def test_from_iterable_builds_a_generator(self) -> None:
        arr = [1, 2, 3]
        it = Iterator.from_iterable(arr)

        assert [x for x in it.gen] == arr


class TestIteratorNext:
    def test_next_advances_an_iterator(self, gen: IntGen) -> None:
        it = Iterator(gen)

        assert it.next() == 1
        assert it.next() == 2

    def test_next_returns_none_when_iterator_is_depleted(self, empty_gen: IntGen) -> None:
        it = Iterator(empty_gen)

        assert it.next() is None


class TestIteratorCollect:
    def test_collect_iterator_to_list(self, gen: IntGen) -> None:
        result = Iterator(gen).collect()

        assert result == [1, 2, 3, 4]

    def test_iterator_cannot_be_collected_multiple_times(self, gen: IntGen) -> None:
        it = Iterator(gen)

        assert it.collect() == [1, 2, 3, 4]
        assert it.collect() == []


class TestIteratorMap:
    def test_map_applies_passed_callable_to_every_element(self, gen: IntGen) -> None:
        result = Iterator(gen).map(lambda x: x + 5).collect()

        assert result == [6, 7, 8, 9]

    def test_map_has_no_effect_on_empty_iterator(self, empty_gen: IntGen) -> None:
        result = Iterator(empty_gen).map(lambda x: x + 5).collect()

        assert result == []


class TestIteratorFilter:
    def test_filter_returns_only_correct_elements(self, gen: IntGen) -> None:
        result = Iterator(gen).filter(lambda x: x % 2 == 0).collect()

        assert result == [2, 4]

    def test_filter_returns_nothing_if_no_item_fits(self, gen: IntGen) -> None:
        result = Iterator(gen).filter(lambda x: x > 10).collect()

        assert result == []
