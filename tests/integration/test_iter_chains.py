from rusty_iterators import Iter


def test_take_on_an_infinite_iterator() -> None:
    it = Iter.from_items(1, 2, 3).cycle().take(10)

    assert it.collect() == [1, 2, 3, 1, 2, 3, 1, 2, 3, 1]


def test_enumerate_on_infinite_iterator() -> None:
    it = Iter.from_items(1, 2, 3).cycle().enumerate().advance_by(10_000)

    assert it.next() == (10_000, 2)
    assert it.next() == (10_001, 3)


def test_step_by_correctly_skips_chain_iterator() -> None:
    it = Iter.from_items(1, 2, 3, 4, 5).chain(Iter.from_items(6, 7, 8, 9, 10)).step_by(2)

    assert it.collect() == [1, 3, 5, 7, 9]


def test_multiple_chains() -> None:
    it = Iter.from_items(1, 2).chain(Iter.from_items(3, 4)).chain(Iter.from_items(5, 6).chain(Iter.from_items(7, 8)))

    assert it.collect() == [1, 2, 3, 4, 5, 6, 7, 8]


def test_multiple_cycles_chained() -> None:
    it = Iter.from_items(1, 2, 3).cycle().cycle().cycle()

    assert [it.next() for _ in range(4)] == [1, 2, 3, 1]


def test_double_cycle() -> None:
    it = Iter.from_items(1, 2, 3).cycle().map(lambda x: x * 3).filter(lambda x: x % 2 == 0).cycle()

    assert [it.next() for _ in range(4)] == [6, 6, 6, 6]


def test_multiples_filters_chained() -> None:
    it = Iter.from_items(1, 2, 3, 4).filter(lambda x: x != 1).filter(lambda x: x != 2).filter(lambda x: x != 3)

    assert it.collect() == [4]
