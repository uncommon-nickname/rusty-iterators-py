from unittest.mock import MagicMock, call

import pytest

from rusty_iterators import IterInterface, NoValue, RustyIter, Value


@pytest.mark.parametrize(
    ("it", "expected"),
    (
        (RustyIter.from_items(1, 2, 3, 4), [1, 2, 3, 4]),
        (RustyIter.from_items(1, 2, 3, 4).map(lambda x: x + 1), [2, 3, 4, 5]),
        (RustyIter.from_items(1, 2, 3, 4).filter(lambda x: x % 2 == 0), [2, 4]),
        (RustyIter.from_items(1, 2, 3, 4).enumerate(), [(0, 1), (1, 2), (2, 3), (3, 4)]),
        (RustyIter.from_items(1, 2, 3, 4).filter_map(lambda x: Value(x**2) if x % 2 == 0 else NoValue()), [4, 16]),
        (RustyIter.from_items(1, 2, 3, 4).inspect(lambda _: None), [1, 2, 3, 4]),
        (RustyIter.from_items(1, 2, 3, 4).step_by(2), [1, 3]),
        (RustyIter.from_items(1, 2).chain(RustyIter.from_items(3, 4)), [1, 2, 3, 4]),
    ),
)
def test_for_each(it: IterInterface[int], expected: list[int]) -> None:
    mock = MagicMock()
    it.for_each(lambda x: mock(x))

    mock.assert_has_calls([call(x) for x in expected])
