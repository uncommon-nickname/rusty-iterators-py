from __future__ import annotations

from typing import TYPE_CHECKING, Any, Generic, final

from rusty_iterators._versioned_types import TypeVar, override

from ._interface import AsyncIterInterface

if TYPE_CHECKING:
    from collections.abc import AsyncIterator

T = TypeVar("T", default=Any)


@final
class AsyncIterWrapper(AsyncIterInterface[T], Generic[T]):
    __slots__ = ("ait",)

    def __init__(self, ait: AsyncIterator[T]) -> None:
        self.ait = ait

    @override
    def __str__(self) -> str:
        return f"AsyncIterWrapper(ait={self.ait})"

    @override
    async def anext(self) -> T:
        return await anext(self.ait)
