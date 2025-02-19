from __future__ import annotations

from collections.abc import AsyncIterator, Iterator, Sequence
from typing import Any

from rusty_iterators._versioned_types import TypeVar
from rusty_iterators.core.wrappers import AsyncIterWrapper, IterWrapper, SeqWrapper

T = TypeVar("T", default=Any, contravariant=True)


class LIter:
    @classmethod
    def from_it(cls, it: Iterator[T]) -> IterWrapper[T]:
        return IterWrapper(it)

    @classmethod
    def from_items(cls, *args: T) -> SeqWrapper[T]:
        return SeqWrapper(args)

    @classmethod
    def from_seq(cls, s: Sequence[T]) -> SeqWrapper[T]:
        return SeqWrapper(s)

    @classmethod
    def from_ait(cls, ait: AsyncIterator[T]) -> AsyncIterWrapper[T]:
        return AsyncIterWrapper(ait)
