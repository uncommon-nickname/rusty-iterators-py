import pytest

from rusty_iterators import IterInterface, RustyIter


@pytest.mark.parametrize(
    ("it", "expected"),
    ((RustyIter.from_items(0, 2, 3), False), (RustyIter.from_items(1, 2, 3), True)),
)
def test_all_iterator(it: IterInterface[int], expected: bool) -> None:
    assert it.all() is expected
