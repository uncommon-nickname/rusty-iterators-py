from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, Self, final, override

if TYPE_CHECKING:
    from ._sync import IterInterface
    from ._types import AMapCallable


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

    @override
    def __repr__(self) -> str:
        return self.__str__()

    async def acollect(self) -> list[T]:
        return [item async for item in self]

    def amap[R](self, af: AMapCallable[T, R]) -> AMap[T, R]:
        return AMap(self, af)

    async def anext(self) -> T:
        raise NotImplementedError


@final
class AIter[T](AIterInterface[T]):
    def __init__(self, it: IterInterface[T]) -> None:
        self.it = it

    @override
    def __str__(self) -> str:
        return f"AIter(it={self.it})"

    @override
    async def anext(self) -> T:
        try:
            return self.it.next()
        except StopIteration as exc:
            raise StopAsyncIteration from exc


@final
class AMap[T, R](AIterInterface[R]):
    __slots__ = ("af", "ait")

    def __init__(self, ait: AIterInterface[T], af: AMapCallable[T, R]) -> None:
        self.af = af
        self.ait = ait

    @override
    def __str__(self) -> str:
        return f"AMap(ait={self.ait})"

    @override
    async def anext(self) -> R:
        return await self.af(await self.ait.anext())
