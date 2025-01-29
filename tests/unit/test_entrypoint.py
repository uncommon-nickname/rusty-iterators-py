from rusty_iterators.lib import LIter


def test_sequence_constructor() -> None:
    assert LIter.build("ab").map(lambda x: x * 2).collect() == ["aa", "bb"]
    assert LIter.build([1, 2, 3]).map(lambda x: x * 2).collect() == [2, 4, 6]


def test_iterator_constructor() -> None:
    assert LIter.build(iter(range(4))).filter(lambda x: x % 2 == 0).collect() == [0, 2]


def test_items_constructor() -> None:
    assert LIter.build(1, 2, 3).map(lambda x: x * 2).collect() == [2, 4, 6]
