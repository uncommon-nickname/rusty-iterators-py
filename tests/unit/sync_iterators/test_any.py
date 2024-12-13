import pytest

from rusty_iterators import IterInterface, RustyIter


@pytest.mark.parametrize(
    ("it", "expected"),
    ((RustyIter.from_items(0, 2, 3), True), (RustyIter.from_items(0, 0, 0), False)),
)
def test_any_iterator(it: IterInterface[int], expected: bool) -> None:
    assert it.any() is expected
