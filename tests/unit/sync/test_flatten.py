import gc
import sys
from unittest.mock import Mock

import pytest

from rusty_iterators import LIter


def test_invalid_iterator_structure() -> None:
    # This is not allowed and will crash, so `type: ignore` is needed.
    it = LIter.from_items(1, 2, 3, [3]).flatten()  # type: ignore[misc, var-annotated]

    with pytest.raises(TypeError):
        it.collect()


def test_single_flatten() -> None:
    it = LIter.from_items([1, 2, 3], [4, 5, 6]).flatten()

    assert it.collect() == [1, 2, 3, 4, 5, 6]


def test_double_flatten() -> None:
    it = LIter.from_items([[1], [2], [3]], [[4], [5], [6]]).flatten().flatten()

    assert it.collect() == [1, 2, 3, 4, 5, 6]


def test_copy_flatten() -> None:
    it = LIter.from_items([1, 2], [3, 4]).flatten()
    it.next()
    copy = it.copy()

    it.advance_by(1)

    assert it.collect() == [3, 4]
    assert copy.collect() == [2, 3, 4]


def test_flatten_deallocate() -> None:
    m1 = Mock()
    m2 = Mock()

    assert sys.getrefcount(m1) == 2
    assert sys.getrefcount(m2) == 2

    it = LIter.from_items([[Mock()], [m1], [m2], [Mock()], [Mock()], [Mock()]])

    assert sys.getrefcount(m1) == 3
    assert sys.getrefcount(m2) == 3

    it.flatten().collect()

    assert sys.getrefcount(m1) == 3
    assert sys.getrefcount(m2) == 3

    del it

    gc.collect()

    assert sys.getrefcount(m1) == 2
    assert sys.getrefcount(m2) == 2
