from typing import Iterator

from rusty_iterators import RustyIter


def gen() -> Iterator[int]:
    while True:
        yield 1


def test_take_on_an_infinite_iterator() -> None:
    it = RustyIter.from_it(gen()).take(10)

    assert it.collect() == [1] * 10


def test_enumerate_on_infinite_iterator() -> None:
    it = RustyIter.from_it(gen()).enumerate().advance_by(10_000)

    assert it.next() == (10_000, 1)
    assert it.next() == (10_001, 1)


def test_step_by_correctly_skips_chain_iterator() -> None:
    it = RustyIter.from_items(1, 2, 3, 4, 5).chain(RustyIter.from_items(6, 7, 8, 9, 10)).step_by(2)

    assert it.collect() == [1, 3, 5, 7, 9]


def test_multiple_chains() -> None:
    it = (
        RustyIter.from_items(1, 2)
        .chain(RustyIter.from_items(3, 4))
        .chain(RustyIter.from_items(5, 6).chain(RustyIter.from_items(7, 8)))
    )

    assert it.collect() == [1, 2, 3, 4, 5, 6, 7, 8]


def test_multiples_filters_chained() -> None:
    it = RustyIter.from_items(1, 2, 3, 4).filter(lambda x: x != 1).filter(lambda x: x != 2).filter(lambda x: x != 3)

    assert it.collect() == [4]