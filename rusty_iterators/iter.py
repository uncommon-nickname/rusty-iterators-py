from __future__ import annotations

import itertools
from collections.abc import Callable
from typing import Iterable, Iterator, Protocol, Self, final, override

from .option import NoValue, Value

type Option[T] = Value[T] | NoValue
type EnumerateItem[T] = tuple[int, T]


class IterInterface[T](Protocol):
    def __iter__(self) -> Self:
        return self

    def __next__(self) -> T:
        return self.next()

    def advance_by(self, n: int) -> Self:
        if n < 0:
            raise ValueError("Amount to advance by must be greater or equal to 0.")
        for _ in range(n):
            try:
                self.next()
            except StopIteration:
                break
        return self

    def collect(self) -> list[T]:
        return [item for item in self]

    def copy(self) -> IterInterface[T]:
        raise NotImplementedError

    def count(self) -> int:
        ctr = 0
        for _ in self:
            ctr += 1
        return ctr

    def cycle(self) -> Cycle[T]:
        return Cycle(self)

    def enumerate(self) -> Enumerate[T]:
        return Enumerate(self)

    def for_each(self, f: Callable[[T], None]) -> None:
        for item in self:
            f(item)

    def last(self) -> Option[T]:
        last: Option[T] = NoValue()
        for item in self:
            last = Value(item)
        return last

    def map[R](self, f: Callable[[T], R]) -> Map[T, R]:
        return Map(self, f)

    def next(self) -> T:
        raise NotImplementedError

    def next_noexcept(self) -> Option[T]:
        try:
            return Value(self.next())
        except StopIteration:
            return NoValue()

    def nth(self, n: int) -> Option[T]:
        self.advance_by(n)
        return self.next_noexcept()

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
    def next(self) -> T:
        return next(self.gen)


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
    def next(self) -> R:
        return self.f(self.iter.next())


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
    def next(self) -> T:
        while True:
            if self.f(item := self.iter.next()):
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
    def next(self) -> T:
        try:
            return self.iter.next()
        except StopIteration:
            self.iter = self.orig.copy()
            return self.iter.next()


@final
class Enumerate[T](IterInterface[EnumerateItem[T]]):
    __slots__ = ("curr_idx", "iter")

    def __init__(self, iter: IterInterface[T]) -> None:
        self.curr_idx = 0
        self.iter = iter

    @override
    def copy(self) -> Enumerate[T]:
        return Enumerate(self.iter.copy())

    @override
    def count(self) -> int:
        return self.iter.count()

    @override
    def next(self) -> EnumerateItem[T]:
        item = self.iter.next()
        result = (self.curr_idx, item)
        self.curr_idx += 1
        return result
