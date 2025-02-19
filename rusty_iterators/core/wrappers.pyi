from __future__ import annotations

from collections.abc import AsyncIterator, Iterator, Sequence
from typing import Any, final

from rusty_iterators._versioned_types import TypeVar
from rusty_iterators.core.async_interface import AsyncIterInterface
from rusty_iterators.core.interface import IterInterface

T = TypeVar("T", default=Any)

@final
class SeqWrapper(IterInterface[T]):
    def __init__(self, s: Sequence[T]) -> None: ...

@final
class IterWrapper(IterInterface[T]):
    def __init__(self, it: Iterator[T]) -> None: ...

@final
class AsyncIterWrapper(AsyncIterInterface[T]):
    def __init__(self, ait: AsyncIterator[T]) -> None: ...
