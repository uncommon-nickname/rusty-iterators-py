from __future__ import annotations

from typing import TYPE_CHECKING, AsyncIterator, Protocol, Self, final, override

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

    type AMapCallable[T, R] = Callable[[T], Awaitable[R]]


class AIterInterface[T](Protocol):
    """An interface that every async iterator should implement.

    This is a proof of concept, not a final API!

    Provides a lot of default implementations, that should be correct
    in most custom async iterators. Can be iterated over with `async for`
    and chained in Rust style.
    """

    __slots__ = ()

    def __aiter__(self) -> Self:
        return self

    async def __anext__(self) -> T:
        return await self.anext()

    async def acollect(self) -> list[T]:
        return [item async for item in self]

    def amap[R](self, crt: AMapCallable[T, R]) -> AMap[T, R]:
        return AMap(self, crt)

    async def anext(self) -> T:
        raise NotImplementedError


@final
class AIter[T](AIterInterface[T]):
    __slots__ = ("agen",)

    def __init__(self, agen: AsyncIterator[T]) -> None:
        self.agen = agen

    @override
    async def anext(self) -> T:
        return await anext(self.agen)


@final
class AMap[T, R](AIterInterface[R]):
    __slots__ = ("aiter", "crt")

    def __init__(self, aiter: AIterInterface[T], crt: AMapCallable[T, R]) -> None:
        self.aiter = aiter
        self.crt = crt

    @override
    async def anext(self) -> R:
        return await self.crt(await self.aiter.anext())
