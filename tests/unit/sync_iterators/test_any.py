import pytest

from rusty_iterators import IterInterface, RustyIter


@pytest.mark.parametrize(
    ("it", "expected"),
    ((RustyIter.from_items(0, 2, 3), True), (RustyIter.from_items(0, 0, 0), False)),
)
def test_any_iterator(it: IterInterface[int], expected: bool) -> None:
    assert it.any() is expected


def test_custom_callback_in_any_iterator() -> None:
    s = [(1, 2), (3, 4), (5, 6)]
    result = RustyIter.from_seq(s).any(lambda x: x[0] > 2)

    assert result is True
