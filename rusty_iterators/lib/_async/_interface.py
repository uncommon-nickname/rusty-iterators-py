from __future__ import annotations

from typing import TYPE_CHECKING, Any, Generic, Protocol, TypeAlias, final

from rusty_iterators._versioned_types import Self, TypeVar, override

T = TypeVar("T", default=Any)
R = TypeVar("R", default=Any)

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

    AsyncMapCallable: TypeAlias = Callable[[T], Awaitable[R]]


class AsyncIterInterface(Protocol, Generic[T]):
    __slots__ = ()

    def __aiter__(self) -> Self:
        return self

    async def __anext__(self) -> T:
        return await self.anext()

    @override
    def __repr__(self) -> str:
        return self.__str__()

    async def anext(self) -> T:
        raise NotImplementedError

    async def acollect(self) -> list[T]:
        return [item async for item in self]

    def amap(self, afunc: AsyncMapCallable[T, R]) -> AsyncMap[T, R]:
        return AsyncMap(self, afunc)


@final
class AsyncMap(AsyncIterInterface[R], Generic[T, R]):
    __slots__ = ("afunc", "ait")

    def __init__(self, ait: AsyncIterInterface[T], afunc: AsyncMapCallable[T, R]) -> None:
        self.afunc = afunc
        self.ait = ait

    @override
    def __str__(self) -> str:
        return f"AsyncMap(ait={self.ait})"

    @override
    async def anext(self) -> R:
        return await self.afunc(await self.ait.anext())
