from __future__ import annotations

from collections.abc import Callable, Iterator
from typing import Any, Generic, Literal, Optional, Protocol, TypeAlias, final, overload

from rusty_iterators._versioned_types import Self, TypeVar
from rusty_iterators.lib._async import AsyncIterAdapter

T = TypeVar("T", default=Any)
T_co = TypeVar("T_co", default=Any, covariant=True)
R = TypeVar("R", default=Any)
P = TypeVar("P", default=Any)

AggCallable: TypeAlias = Callable[[T], bool]
FilterCallable: TypeAlias = Callable[[T], bool]
FoldCallable: TypeAlias = Callable[[R, T], R]
MapCallable: TypeAlias = Callable[[T], R]
ReduceCallable: TypeAlias = Callable[[T, T], T]

EnumerateItem: TypeAlias = tuple[int, R]
ZipItem: TypeAlias = tuple[T, R]

class BuildableFromIterator(Protocol[T_co]):
    def __init__(self, iterator: Iterator[T_co]) -> None: ...

class Addable(Protocol):
    def __add__(self: T, other: T) -> T: ...

class IterInterface(Generic[T]):
    T_addable = TypeVar("T_addable", bound=Addable)
    T_buildable = TypeVar("T_buildable", bound=BuildableFromIterator[T])

    def __iter__(self) -> Self: ...
    def __next__(self) -> T: ...
    def advance_by(self, n: int) -> Self: ...
    def all(self, f: Optional[AggCallable[T]] = None) -> bool: ...
    def any(self, f: Optional[AggCallable[T]] = None) -> bool: ...
    def as_async(self) -> AsyncIterAdapter[T]: ...
    def can_be_copied(self) -> bool: ...
    def chain(self, second: IterInterface[T]) -> Chain[T]: ...
    def collect(self) -> list[T]: ...
    @overload
    def collect_into(self, factory: type[tuple[T, ...]]) -> tuple[T, ...]: ...
    @overload
    def collect_into(self, factory: type[list[T]]) -> list[T]: ...
    @overload
    def collect_into(self, factory: type[set[T]]) -> set[T]: ...
    @overload
    def collect_into(self, factory: type[frozenset[T]]) -> frozenset[T]: ...
    @overload
    def collect_into(self, factory: type[T_buildable]) -> T_buildable: ...
    def copy(self) -> Self: ...
    @overload
    def cycle(self, use_cache: Literal[False]) -> CopyCycle[T]: ...
    @overload
    def cycle(self, use_cache: Literal[True] = True) -> CacheCycle[T]: ...
    def enumerate(self) -> Enumerate[T]: ...
    def filter(self, func: FilterCallable[T]) -> Filter[T]: ...
    def fold(self, init: R, func: FoldCallable[R, T]) -> R: ...
    def map(self, func: MapCallable[T, R]) -> Map[T, R]: ...
    @overload
    def moving_window(self, size: int, use_cache: Literal[False]) -> CopyMovingWindow[T]: ...
    @overload
    def moving_window(self, size: int, use_cache: Literal[True] = True) -> CacheMovingWindow[T]: ...
    @overload
    def moving_window(self, size: int, use_cache: bool) -> CopyMovingWindow[T] | CacheMovingWindow[T]: ...
    def next(self) -> T: ...
    def nth(self, n: int) -> T: ...
    def reduce(self, func: ReduceCallable[T]) -> T: ...
    def step_by(self, step: int) -> StepBy[T]: ...
    def sum(self: IterInterface[T_addable]) -> T_addable: ...
    def take(self, amount: int) -> Take[T]: ...
    @overload
    def unzip(self: IterInterface[list[R]]) -> tuple[list[R], list[R]]: ...
    @overload
    def unzip(self: IterInterface[tuple[R, P]]) -> tuple[list[R], list[P]]: ...
    def zip(self, second: IterInterface[R]) -> Zip[T, R]: ...

@final
class Enumerate(IterInterface[EnumerateItem[T]]):
    def __init__(self, it: IterInterface[T]) -> None: ...

@final
class Filter(IterInterface[T], Generic[T]):
    def __init__(self, other: IterInterface[T], func: FilterCallable[T]) -> None: ...

@final
class Map(IterInterface[R], Generic[T, R]):
    def __init__(self, it: IterInterface[T], func: MapCallable[T, R]) -> None: ...

@final
class CacheCycle(IterInterface[T], Generic[T]):
    def __init__(self, it: IterInterface[T]) -> None: ...

@final
class CacheMovingWindow(IterInterface[list[T]], Generic[T]):
    def __init__(self, it: IterInterface[T], size: int) -> None: ...

@final
class CopyCycle(IterInterface[T], Generic[T]):
    def __init__(self, it: IterInterface[T]) -> None: ...

@final
class CopyMovingWindow(IterInterface[list[T]], Generic[T]):
    def __init__(self, it: IterInterface[T], size: int) -> None: ...

@final
class StepBy(IterInterface[T], Generic[T]):
    def __init__(self, it: IterInterface[T], step: int) -> None: ...

@final
class Take(IterInterface[T], Generic[T]):
    def __init__(self, it: IterInterface[T], amount: int) -> None: ...

@final
class Zip(IterInterface[ZipItem[T, R]], Generic[T, R]):
    def __init__(self, first: IterInterface[T], second: IterInterface[R]) -> None: ...

@final
class Chain(IterInterface[T], Generic[T]):
    def __init__(self, first: IterInterface[T], second: IterInterface[R]) -> None: ...
