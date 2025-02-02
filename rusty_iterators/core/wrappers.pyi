from __future__ import annotations

from collections.abc import Callable, Iterator, Sequence
from typing import Any, Generic, TypeAlias, final

from rusty_iterators._versioned_types import TypeVar, override
from rusty_iterators.core.interface import IterInterface

T = TypeVar("T", default=Any, covariant=True)
R = TypeVar("R", default=Any, covariant=True)

FilterCallable: TypeAlias = Callable[[T], bool]
MapCallable: TypeAlias = Callable[[T], R]

@final
class SeqWrapper(IterInterface[T], Generic[T]):
    def __init__(self, s: Sequence[T]) -> None: ...
    @override
    def copy(self) -> SeqWrapper[T]: ...

@final
class IterWrapper(IterInterface[T], Generic[T]):
    def __init__(self, it: Iterator[T]) -> None: ...
    @override
    def copy(self) -> IterWrapper[T]: ...
