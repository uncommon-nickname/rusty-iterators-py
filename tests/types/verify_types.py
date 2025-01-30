from __future__ import annotations

from typing import TYPE_CHECKING, Any, assert_type

from rusty_iterators.lib import LIter

if TYPE_CHECKING:
    from rusty_iterators.core.interface import Filter, IterWrapper, Map, SeqWrapper


def verify_empty_items_iterator_type() -> None:
    it = LIter.from_items()

    assert_type(it, SeqWrapper[Any])
    assert_type(it.next(), Any)
    assert_type(it.collect(), list[Any])


def verify_items_iterator_type() -> None:
    it = LIter.from_items(1, 2, 3)

    assert_type(it, SeqWrapper[int])
    assert_type(it.next(), int)
    assert_type(it.collect(), list[int])


def verify_empty_sequence_iterator_type() -> None:
    it = LIter.from_seq([])

    assert_type(it, SeqWrapper[Any])
    assert_type(it.next(), Any)
    assert_type(it.collect(), list[Any])


def verify_sequence_iterator_type() -> None:
    it = LIter.from_seq([1, 2, 3])

    assert_type(it, SeqWrapper[int])
    assert_type(it.next(), int)
    assert_type(it.collect(), list[int])


def verify_iterator_type() -> None:
    it = LIter.from_it(iter(range(10)))

    assert_type(it, IterWrapper[int])
    assert_type(it.next(), int)
    assert_type(it.collect(), list[int])


def verify_map_iterator_type() -> None:
    it = LIter.from_items(1, 2, 3).map(lambda x: str(x))

    assert_type(it, Map[int, str])
    assert_type(it.next(), str)
    assert_type(it.collect(), list[str])


def verify_filter_iterator_type() -> None:
    it = LIter.from_items(1, 2, 3).filter(lambda x: x % 2 == 0)

    assert_type(it, Filter[int])
    assert_type(it.next(), int)
    assert_type(it.collect(), list[int])
