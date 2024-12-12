import asyncio
from collections.abc import AsyncIterator


async def parse_item(item: int) -> int:
    await asyncio.sleep(0.001)
    return item**2


async def agen() -> AsyncIterator[int]:
    for x in [1, 2, 3]:
        await asyncio.sleep(0.001)
        yield x
