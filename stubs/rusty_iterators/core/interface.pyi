from __future__ import annotations

import sys
from collections.abc import Callable
from typing import Any, Generic, Iterator, Self, Sequence, TypeAlias, final, override

if sys.version_info < (3, 11):
    from typing_extensions import Self
else:
    from typing import Self

if sys.version_info < (3, 13):
    from typing_extensions import TypeVar
else:
    from typing import TypeVar

T = TypeVar("T", default=Any, covariant=True)
R = TypeVar("R", default=Any, covariant=True)

FilterCallable: TypeAlias = Callable[[T], bool]
MapCallable: TypeAlias = Callable[[T], R]

class IterInterface(Generic[T]):
    def __iter__(self) -> Self: ...
    def __next__(self) -> T: ...
    def collect(self) -> list[T]: ...
    def filter(self, func: FilterCallable[T]) -> Filter[T]: ...
    def map[R](self, func: MapCallable[T, R]) -> Map[T, R]: ...
    def next(self) -> T: ...

@final
class Filter(IterInterface[T], Generic[T]):
    def __init__(self, other: IterInterface[T], func: FilterCallable[T]) -> None: ...
    @override
    def next(self) -> T: ...

@final
class Map(IterInterface[R], Generic[T, R]):
    def __init__(self, other: IterInterface[T], func: MapCallable[T, R]) -> None: ...
    @override
    def next(self) -> R: ...

@final
class SeqWrapper(IterInterface[T], Generic[T]):
    def __init__(self, s: Sequence[T]) -> None: ...
    def copy(self) -> bool: ...

@final
class IterWrapper(IterInterface[T], Generic[T]):
    def __init__(self, it: Iterator[T]) -> None: ...
    def copy(self) -> bool: ...
