from rusty_iterators import RustyIter


def test_unzip_zipped_iterator() -> None:
    it = RustyIter.from_items(1, 2, 3).zip(RustyIter.from_items("a", "b", "c"))

    assert it.unzip() == ([1, 2, 3], ["a", "b", "c"])


def test_unzip_list_elements() -> None:
    it = RustyIter.from_items([1, 2], [3, 4], [5, 6])

    assert it.unzip() == ([1, 3, 5], [2, 4, 6])


def test_unzip_enumerate() -> None:
    it = RustyIter.from_items(1, 2, 3).enumerate()

    assert it.unzip() == ([0, 1, 2], [1, 2, 3])


def test_unzip_moving_windows() -> None:
    it = RustyIter.from_items(1, 2, 3, 4).moving_window(2)

    assert it.unzip() == ([1, 2, 3], [2, 3, 4])


def test_unzip_chained_zips() -> None:
    it = RustyIter.from_items(1, 2, 3).zip(RustyIter.from_items(4, 5, 6).zip(RustyIter.from_items("a", "b", "c")))

    assert it.unzip() == ([1, 2, 3], [(4, "a"), (5, "b"), (6, "c")])
