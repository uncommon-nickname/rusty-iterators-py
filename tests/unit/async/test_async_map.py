from rusty_iterators import LIter

from ._utils import async_iter


async def apply(item: int) -> str:
    return str(item)


async def test_async_map() -> None:
    assert await LIter.from_ait(async_iter()).amap(apply).acollect() == ["0", "1", "2"]
