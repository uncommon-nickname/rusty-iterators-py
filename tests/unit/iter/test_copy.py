import pytest

from rusty_iterators import Iter, IterInterface, Value


@pytest.mark.parametrize(
    "it",
    (
        Iter.from_items(1, 2),
        Iter.from_items(1, 2).map(lambda x: x + 1),
        Iter.from_items(1, 2).filter(lambda x: x != 0),
        Iter.from_items(1, 2).cycle(),
        Iter.from_items(1, 2).enumerate(),
        Iter.from_items(1, 2).filter_map(lambda x: Value(x)),
        Iter.from_items(1, 2).inspect(lambda _: None),
        Iter.from_items(1, 2).step_by(2),
        Iter.from_items(1).chain(Iter.from_items(2)),
    ),
)
def test_copy(it: IterInterface[int]) -> None:
    copy = it.copy()
    assert copy.next() == it.next()
