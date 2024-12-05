from __future__ import annotations

from collections.abc import Callable
from typing import Generator, Optional, Protocol, Self, Sequence, final, override


class IterInterface[T](Protocol):
    def collect(self) -> list[T]:
        result = []
        while item := self.next():
            result.append(item)
        return result

    def count(self) -> int:
        ctr = 0
        while self.next():
            ctr += 1
        return ctr

    def map[R](self, f: Callable[[T], R]) -> Map[T, R]:
        return Map(self, f)

    def next(self) -> Optional[T]:
        raise NotImplementedError

    def filter(self, f: Callable[[T], bool]) -> Filter[T]:
        return Filter(self, f)


@final
class Iterator[T](IterInterface[T]):
    def __init__(self, gen: Generator[T, None, None]) -> None:
        self.gen = gen

    @classmethod
    def from_items(cls, *items: T) -> Self:
        return cls(item for item in items)

    @classmethod
    def from_iterable(cls, iter: Sequence[T]) -> Self:
        return cls(item for item in iter)

    @override
    def next(self) -> Optional[T]:
        try:
            return next(self.gen)
        except StopIteration:
            return None


@final
class Map[T, R](IterInterface[R]):
    def __init__(self, iter: IterInterface[T], f: Callable[[T], R]) -> None:
        self.iter = iter
        self.f = f

    @override
    def count(self) -> int:
        return self.iter.count()

    @override
    def next(self) -> Optional[R]:
        if (item := self.iter.next()) is None:
            return None
        return self.f(item)


@final
class Filter[T](IterInterface[T]):
    def __init__(self, iter: IterInterface[T], f: Callable[[T], bool]) -> None:
        self.iter = iter
        self.f = f

    @override
    def next(self) -> Optional[T]:
        while item := self.iter.next():
            if self.f(item) is True:
                return item
        return None
