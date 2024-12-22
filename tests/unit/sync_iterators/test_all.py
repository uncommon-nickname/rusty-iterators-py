import pytest

from rusty_iterators import IterInterface, RustyIter


@pytest.mark.parametrize(
    ("it", "expected"),
    ((RustyIter.from_items(0, 2, 3), False), (RustyIter.from_items(1, 2, 3), True)),
)
def test_all_iterator(it: IterInterface[int], expected: bool) -> None:
    assert it.all() is expected


def test_custom_callback_in_all_iterator() -> None:
    s = [(1, 2), (3, 4), (5, 6)]
    result = RustyIter.from_seq(s).all(lambda x: x[0] > 2)

    assert result is False
