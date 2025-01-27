from __future__ import annotations

from collections.abc import Iterator, Sequence

from ..core.interface import IterWrapper, SeqWrapper

class LIter[T]:
    # TODO!: to remove after rewrite tests to use common constructor
    @classmethod
    def from_items(cls, *args: T) -> SeqWrapper[T]: ...
    @classmethod
    def build(cls, *args: Iterator[T] | Sequence[T]) -> IterWrapper[T] | SeqWrapper[T]: ...
