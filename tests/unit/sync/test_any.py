from rusty_iterators import LIter


def test_any_iterator() -> None:
    assert LIter.from_items(0, 2, 3).any() is True
    assert LIter.from_items(0, 0, 0).any() is False


def test_custom_callback_in_any_iterator() -> None:
    s = [(1, 2), (3, 4), (5, 6)]
    result = LIter.from_seq(s).any(lambda x: x[0] > 2)

    assert result is True
