from __future__ import annotations

from collections.abc import AsyncIterator, Iterator, Sequence
from typing import Any, Generic, final

from rusty_iterators._versioned_types import Self, TypeVar
from rusty_iterators.core.async_interface import AsyncIterInterface
from rusty_iterators.core.interface import IterInterface

T = TypeVar("T", default=Any)

@final
class CopiableGenerator(Generic[T]):
    def __init__(self, it: Iterator[T], cache: list[T], ptr: int) -> None: ...
    def __iter__(self) -> Self: ...
    def __next__(self) -> T: ...
    def copy(self) -> Self: ...

@final
class SeqWrapper(IterInterface[T]):
    def __init__(self, s: Sequence[T]) -> None: ...

@final
class IterWrapper(IterInterface[T]):
    def __init__(self, it: Iterator[T]) -> None: ...

@final
class AsyncIterWrapper(AsyncIterInterface[T]):
    def __init__(self, ait: AsyncIterator[T]) -> None: ...
