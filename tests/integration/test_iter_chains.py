from rusty_iterators import RustyIter


def test_take_on_an_infinite_iterator() -> None:
    it = RustyIter.from_items(1, 2, 3).cycle().take(10)

    assert it.collect() == [1, 2, 3, 1, 2, 3, 1, 2, 3, 1]


def test_enumerate_on_infinite_iterator() -> None:
    it = RustyIter.from_items(1, 2, 3).cycle().enumerate().advance_by(10_000)

    assert it.next() == (10_000, 2)
    assert it.next() == (10_001, 3)


def test_step_by_correctly_skips_chain_iterator() -> None:
    it = (
        RustyIter.from_items(1, 2, 3, 4, 5)
        .chain(RustyIter.from_items(6, 7, 8, 9, 10))
        .step_by(2)
    )

    assert it.collect() == [1, 3, 5, 7, 9]


def test_multiple_cycles() -> None:
    it = RustyIter.from_items(1, 2, 3).cycle().cycle().cycle()

    assert [it.next() for _ in range(5)] == [1, 2, 3, 1, 2]


def test_multiple_chains() -> None:
    it = (
        RustyIter.from_items(1, 2)
        .chain(RustyIter.from_items(3, 4))
        .chain(RustyIter.from_items(5, 6).chain(RustyIter.from_items(7, 8)))
    )

    assert it.collect() == [1, 2, 3, 4, 5, 6, 7, 8]


def test_multiples_filters_chained() -> None:
    it = (
        RustyIter.from_items(1, 2, 3, 4)
        .filter(lambda x: x != 1)
        .filter(lambda x: x != 2)
        .filter(lambda x: x != 3)
    )

    assert it.collect() == [4]


def test_windows_cycle() -> None:
    it = RustyIter.from_items(1, 2, 3, 4).moving_window(2).cycle()

    assert [it.next() for _ in range(5)] == [[1, 2], [2, 3], [3, 4], [1, 2], [2, 3]]


def test_cycle_windows() -> None:
    it = RustyIter.from_items(1, 2, 3, 4).cycle().moving_window(2)

    assert [it.next() for _ in range(5)] == [[1, 2], [2, 3], [3, 4], [4, 1], [1, 2]]


def test_multiple_zips() -> None:
    it = (
        RustyIter.from_items(1, 2)
        .zip(RustyIter.from_items("a", "b"))
        .zip(RustyIter.from_items(2.0, 3.0))
    )

    assert it.collect() == [((1, "a"), 2.0), ((2, "b"), 3.0)]
