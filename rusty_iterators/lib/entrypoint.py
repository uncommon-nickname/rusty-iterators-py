from collections.abc import AsyncIterator, Iterator, Sequence
from typing import NoReturn

from rusty_iterators.core.interface import IterWrapper, SeqWrapper


class LIter[T]:
    @classmethod
    def from_it(cls, it: Iterator[T]) -> "IterWrapper[T]":
        return IterWrapper(it)

    @classmethod
    def from_items(cls, *args: T) -> "SeqWrapper[T]":
        return SeqWrapper(args)

    @classmethod
    def from_seq(cls, s: Sequence[T]) -> "SeqWrapper[T]":
        return SeqWrapper(s)

    @classmethod
    def from_ait(cls, ait: AsyncIterator[T]) -> NoReturn:
        raise NotImplementedError
