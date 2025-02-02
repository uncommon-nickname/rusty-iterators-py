from rusty_iterators import LIter

from ._utils import async_iter


async def test_async_iterator_constructor() -> None:
    assert await LIter.from_ait(async_iter()).acollect() == [0, 1, 2]


async def test_async_iterator_adapter() -> None:
    assert await LIter.from_items(1, 2, 3).as_async().acollect() == [1, 2, 3]
