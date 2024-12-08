from __future__ import annotations

from typing import Iterator, Sequence, final, override

from ._internal import IterInterface

__all__ = ("IterWrapper", "RustyIter", "SeqWrapper")


class RustyIter[T]:
    """Instantiates a new rusty iterator.

    A main class of the package, should be used as an entrypoint to
    initialize and instantiate a new rusty iterator object. The choice
    of constructor is very important, because it has a direct impact
    on performance of the operation you want to perform.
    """

    __slots__ = ()

    @classmethod
    def from_iterator(cls, it: Iterator[T]) -> IterWrapper[T]:
        return IterWrapper(it)

    @classmethod
    def from_sequence(cls, s: Sequence[T]) -> SeqWrapper[T]:
        return SeqWrapper(s)

    @classmethod
    def from_items(cls, *args: T) -> SeqWrapper[T]:
        return SeqWrapper(args)


@final
class IterWrapper[T](IterInterface[T]):
    """Iterator wrapper keeping a pointer to the python iterator object.

    This type cannot be copied, because it doesn't make sense. All
    copy-related optimizations should keep in mind that this type can
    be a parent of the iterator tree. Some kind of cache is required.
    """

    __slots__ = ("it",)

    def __init__(self, it: Iterator[T]) -> None:
        self.it = it

    @override
    def __str__(self) -> str:
        return f"IterWrapper(id={id(self)}, it={self.it})"

    @override
    def next(self) -> T:
        return next(self.it)


@final
class SeqWrapper[T](IterInterface[T]):
    """Iterator wrapper keeping a pointer to internal sequence.

    This type can be copied, because it cointains pointers only. This
    way I can optimize the use of other iterators that require restarts.
    When copied it is important to remember that the same buffer will
    be reused, so items in the buffer should not be modified.
    """

    __slots__ = ("ptr", "s")

    def __init__(self, s: Sequence[T]) -> None:
        self.ptr = 0
        self.s = s

    @override
    def __str__(self) -> str:
        return f"SeqWrapper(id={id(self)}, ptr={self.ptr})"

    @override
    def next(self) -> T:
        try:
            item = self.s[self.ptr]
        except IndexError as exc:
            raise StopIteration from exc
        self.ptr += 1
        return item
