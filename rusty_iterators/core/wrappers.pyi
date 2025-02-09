from __future__ import annotations

from collections.abc import Iterator, Sequence
from typing import Any, Generic, final

from rusty_iterators._versioned_types import TypeVar
from rusty_iterators.core.interface import IterInterface

T = TypeVar("T", default=Any)

@final
class SeqWrapper(IterInterface[T], Generic[T]):
    def __init__(self, s: Sequence[T]) -> None: ...

@final
class IterWrapper(IterInterface[T], Generic[T]):
    def __init__(self, it: Iterator[T]) -> None: ...
