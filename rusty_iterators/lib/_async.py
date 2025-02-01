from __future__ import annotations

import sys
from typing import TYPE_CHECKING, Any, Generic, Protocol, TypeAlias, final

if sys.version_info < (3, 11):
    from typing_extensions import Self
else:
    from typing import Self

if sys.version_info < (3, 12):
    from typing_extensions import override
else:
    from typing import override

if sys.version_info < (3, 13):
    from typing_extensions import TypeVar
else:
    from typing import TypeVar


T = TypeVar("T", default=Any)
R = TypeVar("R", default=Any)


if TYPE_CHECKING:
    from collections.abc import AsyncIterator, Awaitable, Callable

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
