from __future__ import annotations

from typing import AsyncIterator, Iterator, Sequence, final, override

from rusty_iterators.exceptions import IterNotCopiableError

from ._async import AIterInterface
from ._sync import IterInterface


class RustyIter[T]:
    """Instantiates a new rusty iterator.

    A main class of the package, should be used as an entrypoint to
    initialize and instantiate a new rusty iterator object. The choice
    of constructor is very important, because it has a direct impact
    on performance of the operation you want to perform.
    """

    __slots__ = ()

    @classmethod
    def from_it(cls, it: Iterator[T]) -> IterWrapper[T]:
        return IterWrapper(it)

    @classmethod
    def from_ait(cls, ait: AsyncIterator[T]) -> AIterWrapper[T]:
        return AIterWrapper(ait)

    @classmethod
    def from_seq(cls, s: Sequence[T]) -> SeqWrapper[T]:
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

    Attributes:
        it: A python iterator that is going to be used to retrieve the
            elements when `.next()` is called.
    """

    __slots__ = ("it",)

    def __init__(self, it: Iterator[T]) -> None:
        self.it = it

    @override
    def __str__(self) -> str:
        return f"IterWrapper(it={self.it})"

    @override
    def can_be_copied(self) -> bool:
        return False

    @override
    def copy(self) -> IterWrapper[T]:
        raise IterNotCopiableError(
            "Iterator containing a python generator cannot be copied.\n"
            "Python generators can't be trivially copied, if you really need to create a copy,"
            " you should collect the generator into a Sequence and create a RustyIter from it."
        )

    @override
    def next(self) -> T:
        return next(self.it)


@final
class AIterWrapper[T](AIterInterface[T]):
    __slots__ = ("ait",)

    def __init__(self, ait: AsyncIterator[T]) -> None:
        self.ait = ait

    @override
    def __str__(self) -> str:
        return f"AIterWrapper(ait={self.ait})"

    @override
    async def anext(self) -> T:
        return await anext(self.ait)


@final
class SeqWrapper[T](IterInterface[T]):
    """Iterator wrapper keeping a pointer to internal sequence.

    This type can be copied, because it cointains pointers only. This
    way I can optimize the use of other iterators that require restarts.
    When copied it is important to remember that the same buffer will
    be reused, so items in the buffer should not be modified.

    Attributes:
        ptr: A pointer to the passed sequence that is going to be used
            to retrieve elements when `.next()` is called.
        s: A reference to the original sequence, from which the iterator
            is going to retrieve elements.
    """

    __slots__ = ("ptr", "s")

    def __init__(self, s: Sequence[T]) -> None:
        self.ptr = 0
        self.s = s

    @override
    def __str__(self) -> str:
        return f"SeqWrapper(ptr={self.ptr}, s={len(self.s)})"

    @override
    def can_be_copied(self) -> bool:
        return True

    @override
    def copy(self) -> SeqWrapper[T]:
        obj = SeqWrapper(self.s)
        obj.ptr = self.ptr
        return obj

    @override
    def next(self) -> T:
        try:
            item = self.s[self.ptr]
        except IndexError as exc:
            raise StopIteration from exc
        self.ptr += 1
        return item
