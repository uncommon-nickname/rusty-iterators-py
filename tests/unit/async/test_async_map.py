from rusty_iterators import LIter

from ._utils import async_iter


async def apply(item: int) -> str:
    return str(item)


async def test_async_map() -> None:
    assert await LIter.from_ait(async_iter()).amap(apply).acollect() == ["0", "1", "2"]


async def test_async_map_copy() -> None:
    ait = LIter.from_ait(async_iter()).amap(apply)
    acp = ait.copy()

    await ait.anext()

    assert await ait.acollect() == ["1", "2"]
    assert await acp.acollect() == ["0", "1", "2"]
