from __future__ import annotations

import itertools
from collections.abc import Callable
from typing import Iterable, Iterator, Protocol, Self, final, override

from .option import NoValue, Value

type Option[T] = Value[T] | NoValue
type EnumerateItem[T] = tuple[int, T]


class IterInterface[T](Protocol):
    def advance_by(self, n: int) -> Self:
        if n < 0:
            raise ValueError("Amount to advance by must be greater or equal to 0.")
        for _ in range(n):
            if not self.next().exists:
                break
        return self

    def collect(self) -> list[T]:
        # FIXME: <@uncommon-nickname>
        # Potential perf bottleneck. When appending large number of items
        # to the array, it will resize and reallocate multiple times.
        result = []
        while (item := self.next()).exists:
            result.append(item.value)
        return result

    def copy(self) -> IterInterface[T]:
        raise NotImplementedError

    def count(self) -> int:
        ctr = 0
        while self.next().exists:
            ctr += 1
        return ctr

    def cycle(self) -> Cycle[T]:
        return Cycle(self)

    def enumerate(self) -> Enumerate[T]:
        return Enumerate(self)

    def last(self) -> Option[T]:
        last: Option[T] = NoValue()
        while (curr := self.next()).exists:
            last = curr
        return last

    def map[R](self, f: Callable[[T], R]) -> Map[T, R]:
        return Map(self, f)

    def next(self) -> Option[T]:
        raise NotImplementedError

    def nth(self, n: int) -> Option[T]:
        if n < 0:
            raise ValueError("Nth index must be greater or equal to 0.")
        for _ in range(n):
            if not (item := self.next()).exists:
                return item
        return self.next()

    def filter(self, f: Callable[[T], bool]) -> Filter[T]:
        return Filter(self, f)


@final
class Iter[T](IterInterface[T]):
    __slots__ = ("gen",)

    def __init__(self, gen: Iterator[T]) -> None:
        self.gen = gen

    @classmethod
    def from_items(cls, *items: T) -> Iter[T]:
        return cls(item for item in items)

    @classmethod
    def from_iterable(cls, iter: Iterable[T]) -> Iter[T]:
        return cls(item for item in iter)

    @override
    def copy(self) -> Iter[T]:
        # Generators in python are a simple wrappers around stack frames
        # and Python interface does not really have a way to copy a
        # stack frame. It is theoretically possible from CPython level,
        # but it is not currently supported from Python interface. As a
        # workaround we can rebuild both the original and copied
        # iterators from ground up.
        self.gen, new_copy = itertools.tee(self.gen)
        return Iter(new_copy)

    @override
    def next(self) -> Option[T]:
        try:
            return Value(next(self.gen))
        except StopIteration:
            return NoValue()


@final
class Map[T, R](IterInterface[R]):
    __slots__ = ("f", "iter")

    def __init__(self, iter: IterInterface[T], f: Callable[[T], R]) -> None:
        self.f = f
        self.iter = iter

    @override
    def copy(self) -> Map[T, R]:
        return Map(self.iter.copy(), self.f)

    @override
    def count(self) -> int:
        return self.iter.count()

    @override
    def next(self) -> Option[R]:
        if (item := self.iter.next()).exists:
            return Value(self.f(item.value))
        return item


@final
class Filter[T](IterInterface[T]):
    __slots__ = ("f", "iter")

    def __init__(self, iter: IterInterface[T], f: Callable[[T], bool]) -> None:
        self.f = f
        self.iter = iter

    @override
    def copy(self) -> Filter[T]:
        return Filter(self.iter.copy(), self.f)

    @override
    def next(self) -> Option[T]:
        while (item := self.iter.next()).exists:
            if self.f(item.value):
                return item
        return item


@final
class Cycle[T](IterInterface[T]):
    __slots__ = ("iter", "orig")

    def __init__(self, iter: IterInterface[T]) -> None:
        self.iter = iter.copy()
        self.orig = iter

    @override
    def copy(self) -> Cycle[T]:
        return Cycle(self.iter.copy())

    @override
    def next(self) -> Option[T]:
        if (item := self.iter.next()).exists:
            return item
        self.iter = self.orig.copy()
        return self.iter.next()


@final
class Enumerate[T](IterInterface[EnumerateItem[T]]):
    __slots__ = ("curr_item", "iter")

    def __init__(self, iter: IterInterface[T]) -> None:
        self.curr_item = 0
        self.iter = iter

    @override
    def copy(self) -> Enumerate[T]:
        return Enumerate(self.iter.copy())

    @override
    def count(self) -> int:
        return self.iter.count()

    @override
    def next(self) -> Option[EnumerateItem[T]]:
        if (item := self.iter.next()).exists:
            result = (self.curr_item, item.value)
            self.curr_item += 1
            return Value(result)
        return item

    def __iter__(self) -> Enumerate[T]:
        return self

    def __next__(self) -> EnumerateItem[T]:
        if (item := self.next()).exists:
            return item.value
        raise StopIteration
