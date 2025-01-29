from collections.abc import AsyncIterator, Iterator, Sequence
from typing import TYPE_CHECKING, Protocol, overload

from rusty_iterators.core.interface import IterWrapper, SeqWrapper

if TYPE_CHECKING:

    class LIter[T](Protocol):
        @overload
        @classmethod
        def build(cls) -> SeqWrapper[T]: ...

        @overload
        @classmethod
        def build(cls, it: Iterator[T]) -> IterWrapper[T]: ...

        @overload
        @classmethod
        def build(cls, s: Sequence[T]) -> SeqWrapper[T]: ...

        @overload
        @classmethod
        def build(cls, _: T, *args: T) -> SeqWrapper[T]: ...

else:

    class LIter:
        @classmethod
        def build(cls, *args):
            if len(args) == 1:
                arg = args[0]
                if isinstance(arg, Iterator):
                    return IterWrapper(arg)

                elif isinstance(arg, (list, tuple, Sequence)):
                    return SeqWrapper(arg)

                elif isinstance(arg, AsyncIterator):
                    raise NotImplementedError("not implemented yet")

            return SeqWrapper(args)

        def __init__(self, generator):
            self.generator = generator
