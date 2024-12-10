import asyncio


async def parse_item(item: int) -> int:
    await asyncio.sleep(0.001)
    return item**2
