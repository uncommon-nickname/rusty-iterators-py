from rusty_iterators.lib import LIter


def test_sequence_constructor() -> None:
    assert LIter.from_seq("ab").map(lambda x: x * 2).collect() == ["aa", "bb"]
    assert LIter.from_seq([1, 2, 3]).map(lambda x: x * 2).collect() == [2, 4, 6]


def test_iterator_constructor() -> None:
    it = LIter.from_it(iter(range(4))).filter(lambda x: x % 2 == 0)
    assert it.collect() == [0, 2]


def test_items_constructor() -> None:
    assert LIter.from_items(1, 2, 3).map(lambda x: x * 2).collect() == [2, 4, 6]
