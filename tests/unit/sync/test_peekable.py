import pytest

from rusty_iterators import LIter


def test_peeked_iterator_returns_same_element() -> None:
    it = LIter.from_items(1, 2, 3).peekable()

    assert it.peek() == 1
    assert it.next() == 1


def test_peeked_iterator_resets_state() -> None:
    it = LIter.from_items(1, 2, 3).peekable()
    it.peek()

    assert it.next() == 1
    assert it.next() == 2
    assert it.next() == 3


def test_peeked_iterator_can_be_peeked_again() -> None:
    it = LIter.from_items(1, 2, 3).peekable()

    assert it.peek() == 1
    assert it.peek() == 1
    assert it.peek() == 1


def test_peek_on_empty_iterator() -> None:
    with pytest.raises(StopIteration):
        LIter.from_items().peekable().peek()


def test_copy_non_peeked_iterator() -> None:
    it = LIter.from_items(1, 2, 3).peekable()
    cp = it.copy()

    it.peek()
    cp.next()

    assert it.next() == 1
    assert cp.next() == 2


def test_copy_peeked_iterator() -> None:
    it = LIter.from_items(1, 2, 3).peekable()
    it.peek()

    cp = it.copy()

    assert it.next() == 1
    assert cp.next() == 1
