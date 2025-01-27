import pytest

from rusty_iterators.lib import LIter


def test_sequence_constructor() -> None:
    assert LIter.build("ab").map(lambda x: x * 2).collect() == ["abab"]


@pytest.mark.skip("to check")
def test_iterator_constructor() -> None:
    assert LIter.build(iter(range(4))).filter(lambda x: x % 2 == 0).collect() == [0, 2]
