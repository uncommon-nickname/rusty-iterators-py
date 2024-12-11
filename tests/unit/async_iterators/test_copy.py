import pytest

from rusty_iterators import IterNotCopiableError, RustyIter

from ._utils import agen, parse_item


def test_aiter_is_not_copiable() -> None:
    it = RustyIter.from_ait(agen())

    assert not it.can_be_copied()

    with pytest.raises(IterNotCopiableError):
        it.copy()


def test_aiter_wrapping_iter_is_copiable() -> None:
    it = RustyIter.from_items(1, 2, 3).as_async()

    assert it.can_be_copied()
    it.copy()


async def test_copy_aiter() -> None:
    it = RustyIter.from_items(1, 2, 3).as_async()
    await it.anext()
    copy = it.copy()
    await it.anext()

    await it.acollect() == [3]
    await copy.acollect() == [2, 3]


async def test_copy_amap() -> None:
    it = RustyIter.from_items(1, 2, 3).as_async().amap(parse_item)
    await it.anext()
    copy = it.copy()
    await it.anext()

    await it.acollect() == [9]
    await copy.acollect() == [4, 9]
