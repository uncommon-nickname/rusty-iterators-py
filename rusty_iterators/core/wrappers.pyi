from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import Any, Generic, Iterator, TypeAlias, final

from rusty_iterators._versioned_types import TypeVar
from rusty_iterators.core.interface import IterInterface

T = TypeVar("T", default=Any, covariant=True)
R = TypeVar("R", default=Any, covariant=True)

FilterCallable: TypeAlias = Callable[[T], bool]
MapCallable: TypeAlias = Callable[[T], R]

@final
class SeqWrapper(IterInterface[T], Generic[T]):
    def __init__(self, s: Sequence[T]) -> None: ...
    def copy(self) -> bool: ...

@final
class IterWrapper(IterInterface[T], Generic[T]):
    def __init__(self, it: Iterator[T]) -> None: ...
    def copy(self) -> bool: ...
