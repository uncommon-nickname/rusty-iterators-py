from __future__ import annotations

from collections.abc import AsyncIterator
from typing import TYPE_CHECKING, assert_type

from rusty_iterators import LIter

if TYPE_CHECKING:
    from rusty_iterators.core.async_interface import AsyncIterAdapter, AsyncMap
    from rusty_iterators.core.wrappers import AsyncIterWrapper


async def async_iter() -> AsyncIterator[int]:
    for x in range(3):
        yield x


async def verify_async_iterator_type() -> None:
    ait = LIter.from_ait(async_iter())

    assert_type(ait, AsyncIterWrapper[int])
    assert_type(await ait.anext(), int)
    assert_type(await ait.acollect(), list[int])
    assert_type(ait.copy(), AsyncIterWrapper[int])


async def verify_async_map_type() -> None:
    async def apply_change(item: int) -> str:
        return str(item)

    ait = LIter.from_ait(async_iter()).amap(apply_change)

    assert_type(ait, AsyncMap[str])
    assert_type(await ait.anext(), str)
    assert_type(await ait.acollect(), list[str])
    assert_type(ait.copy(), AsyncMap[str])


async def verify_async_adapter_iterator_type() -> None:
    ait = LIter.from_items(1, 2, 3).as_async()

    assert_type(ait, AsyncIterAdapter[int])
    assert_type(await ait.anext(), int)
    assert_type(await ait.acollect(), list[int])
