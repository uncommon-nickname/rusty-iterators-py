from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any, Generic, TypeAlias, final

from rusty_iterators._versioned_types import Self, TypeVar

from .interface import IterInterface

T = TypeVar("T", default=Any)
R = TypeVar("R", default=Any)

AsyncMapCallable: TypeAlias = Callable[[T], Awaitable[R]]

class AsyncIterInterface(Generic[T]):
    def __aiter__(self) -> Self: ...
    async def __anext__(self) -> T: ...
    async def anext(self) -> T: ...
    async def acollect(self) -> list[T]: ...
    def amap(self, afunc: AsyncMapCallable[T, R]) -> AsyncMap[T, R]: ...

@final
class AsyncIterAdapter(AsyncIterInterface[T]):
    def __init__(self, it: IterInterface[T]) -> None: ...

@final
class AsyncMap(AsyncIterInterface[R], Generic[T, R]):
    def __init__(self, ait: AsyncIterInterface[T], afunc: AsyncMapCallable[T, R]) -> None: ...
