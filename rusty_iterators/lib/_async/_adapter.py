from __future__ import annotations

from typing import TYPE_CHECKING, Any, Generic, final

from rusty_iterators._versioned_types import TypeVar, override

from ._interface import AsyncIterInterface

if TYPE_CHECKING:
    from collections.abc import Iterator

T = TypeVar("T", default=Any)


@final
class AsyncIterAdapter(AsyncIterInterface[T], Generic[T]):
    __slots__ = ("it",)

    def __init__(self, it: Iterator[T]) -> None:
        self.it = it

    @override
    def __str__(self) -> str:
        return f"AsyncIterAdapter(it={self.it})"

    @override
    async def anext(self) -> T:
        try:
            return next(self.it)
        except StopIteration as exc:
            raise StopAsyncIteration from exc
