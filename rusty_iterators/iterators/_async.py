from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Self, final, override

from ._shared import CopyIterInterface

if TYPE_CHECKING:
    from ._sync import IterInterface
    from ._types import AMapCallable, MapCallable


class AIterInterface[T](CopyIterInterface, ABC):
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

    @abstractmethod
    async def anext(self) -> T:
        raise NotImplementedError

    async def acollect(self) -> list[T]:
        return [item async for item in self]

    def amap[R](self, af: AMapCallable[T, R]) -> AMap[T, R]:
        return AMap(self, af)

    def map[R](self, f: MapCallable[T, R]) -> Map[T, R]:
        return Map(self, f)


@final
class AIter[T](AIterInterface[T]):
    """An iterator serving as a proxy between a sync and async iterator.

    Convers a sync iterator interface into an async iterator interface.

    Attributes:
        it: A synchronous iterator that is used to retrieve items, before
            they are passed to the async interface.
    """

    __slots__ = ("it",)

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

    @override
    def can_be_copied(self) -> bool:
        return self.it.can_be_copied()

    @override
    def copy(self) -> AIter[T]:
        return AIter(self.it.copy())


@final
class AMap[T, R](AIterInterface[R]):
    """An async mapping iterator applying async callable to every element.

    Modifies the elements, may be blocking when `anext()` is called.

    Attributes:
        af: An asynchronous callable used to modify the iterator item.
        ait: An asynchronous iterator that should be evaluated to retrieve
            the item that is going to be modified.
    """

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

    @override
    def can_be_copied(self) -> bool:
        return self.ait.can_be_copied()

    @override
    def copy(self) -> AMap[T, R]:
        return AMap(self.ait.copy(), self.af)


@final
class Map[T, R](AIterInterface[R]):
    """A mapping iterator, applying changes to the iterator elements.

    Modifies the elements, but not the size of the iterator itself.

    Attributes:
        f: A callable taking one argument of type `T` and returning value
            of type `R` used to modify the iterator elements.
        ait: The preceding async iterator that should be evaluated before
            the map is applied.
    """

    __slots__ = ("ait", "f")

    def __init__(self, ait: AIterInterface[T], f: MapCallable[T, R]) -> None:
        self.ait = ait
        self.f = f

    @override
    def __str__(self) -> str:
        return f"Map(ait={self.ait})"

    @override
    async def anext(self) -> R:
        return self.f(await self.ait.anext())

    @override
    def can_be_copied(self) -> bool:
        return self.ait.can_be_copied()

    @override
    def copy(self) -> Map[T, R]:
        return Map(self.ait.copy(), self.f)
