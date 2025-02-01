from collections.abc import AsyncIterator


async def async_iter() -> AsyncIterator[int]:
    for x in range(3):
        yield x
