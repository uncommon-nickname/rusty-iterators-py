from rusty_iterators import LIter


def test_all_iterator() -> None:
    assert LIter.from_items(0, 2, 3).all() is False
    assert LIter.from_items(1, 2, 3).all() is True


def test_custom_callback_in_all_iterator() -> None:
    s = [(1, 2), (3, 4), (5, 6)]
    result = LIter.from_seq(s).all(lambda x: x[0] > 2)

    assert result is False
