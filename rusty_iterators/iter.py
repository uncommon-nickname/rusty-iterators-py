from __future__ import annotations

from collections.abc import Callable
from typing import Iterator, Protocol, Self, Sequence, final, override

from .option import NoValue, Value

type Option[T] = Value[T] | NoValue


class IterInterface[T](Protocol):
    def collect(self) -> list[T]:
        result = []
        while (item := self.next()).exists:
            result.append(item.value)
        return result

    def count(self) -> int:
        ctr = 0
        while self.next().exists:
            ctr += 1
        return ctr

    def last(self) -> Option[T]:
        last: Option[T] = NoValue()
        while (curr := self.next()).exists:
            last = curr
        return last

    def map[R](self, f: Callable[[T], R]) -> Map[T, R]:
        return Map(self, f)

    def next(self) -> Option[T]:
        raise NotImplementedError

    def filter(self, f: Callable[[T], bool]) -> Filter[T]:
        return Filter(self, f)


@final
class Iter[T](IterInterface[T]):
    def __init__(self, gen: Iterator[T]) -> None:
        self.gen = gen

    @classmethod
    def from_items(cls, *items: T) -> Self:
        return cls(item for item in items)

    @classmethod
    def from_iterable(cls, iter: Sequence[T]) -> Self:
        return cls(item for item in iter)

    @override
    def next(self) -> Option[T]:
        try:
            return Value(next(self.gen))
        except StopIteration:
            return NoValue()


@final
class Map[T, R](IterInterface[R]):
    def __init__(self, iter: IterInterface[T], f: Callable[[T], R]) -> None:
        self.iter = iter
        self.f = f

    @override
    def count(self) -> int:
        # Map doesn't influence the iterator size. We consume the
        # iterator anyway, so we can avoid unnecessary computation
        # by skipping the map evaluation and using the underlying
        # iterator directly.
        return self.iter.count()

    @override
    def next(self) -> Option[R]:
        if (item := self.iter.next()).exists:
            return Value(self.f(item.value))
        return item


@final
class Filter[T](IterInterface[T]):
    def __init__(self, iter: IterInterface[T], f: Callable[[T], bool]) -> None:
        self.iter = iter
        self.f = f

    @override
    def next(self) -> Option[T]:
        while (item := self.iter.next()).exists:
            if self.f(item.value):
                return item
        return item
