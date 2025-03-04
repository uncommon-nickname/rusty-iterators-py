import gc

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
    it = LIter.from_items([[1, 2, 3], [4, 5, 6]]).flatten()
    obj_id = id(it)

    del it
    gc.collect()

    assert not any(id(obj) == obj_id for obj in gc.get_objects())
