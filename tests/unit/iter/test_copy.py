import pytest

from rusty_iterators import Iter, IterInterface, NoValue, Value


@pytest.mark.parametrize(
    "it",
    (
        Iter.from_items(1, 2, 3, 4),
        Iter.from_items(1, 2, 3, 4).map(lambda x: x * 2),
        Iter.from_items(1, 2, 3, 4).filter(lambda x: x % 2 == 0),
        Iter.from_items(1, 2, 3, 4).filter_map(lambda x: Value(x**2) if x % 2 == 0 else NoValue()),
        Iter.from_items(1, 2, 3, 4).inspect(lambda _: None),
    ),
)
def test_easily_copyable_iterators(it: IterInterface[int]) -> None:
    assert it.copy().collect() == it.collect()


def test_copied_cycle_contains_the_original_iterator_state() -> None:
    it = Iter.from_items(1, 2)
    cycle = it.cycle()
    it.next()

    copied = cycle.copy()

    assert [copied.next() for _ in range(5)] == [cycle.next() for _ in range(5)] == [1, 2, 2, 2, 2]


def test_copied_enumerate_preserves_the_index_state() -> None:
    it = Iter.from_items(1, 2, 3, 4).enumerate()
    it.next(), it.next()

    assert it.copy().collect() == it.collect() == [(2, 3), (3, 4)]


def test_copied_step_by_preserves_the_first_item_state() -> None:
    it = Iter.from_items(1, 2, 3, 4, 5, 6).step_by(2)
    it.next()

    assert it.copy().collect() == it.collect() == [3, 5]


def test_copied_chain_preserves_second_iterator_state() -> None:
    it = Iter.from_items(1, 2).chain(Iter.from_items(3, 4))
    it.next(), it.next()

    assert it.copy().collect() == it.collect() == [3, 4]


def test_copied_take_preserves_taken_items() -> None:
    it = Iter.from_items(1, 2, 3, 4).take(3)
    it.next()

    assert it.copy().collect() == it.collect() == [2, 3]
