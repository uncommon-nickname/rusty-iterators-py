from rusty_iterators import RustyIter


def test_fold_iterator() -> None:
    result = RustyIter.from_items(1, 2, 3, 4, 5).fold("0", lambda acc, x: f"({acc} + {x})")

    assert result == "(((((0 + 1) + 2) + 3) + 4) + 5)"


def test_sum_iterator_using_fold() -> None:
    result = RustyIter.from_items(1, 2, 3, 4).fold(0, lambda acc, x: acc + x)

    assert result == 10
