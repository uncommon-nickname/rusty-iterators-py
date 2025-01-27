from collections.abc import AsyncIterator, Iterator, Sequence

from rusty_iterators.core.interface import IterWrapper, SeqWrapper


class LIter:
    @classmethod
    def build(cls, *args):
        if isinstance(args, (Sequence, list, tuple)):
            return SeqWrapper(args)

        elif isinstance(args, Iterator):
            return IterWrapper(args)

        elif isinstance(args, AsyncIterator):
            raise Exception("not implemented")

        raise Exception("unreachable")

    def __init__(self, generator):
        self.generator = generator

    # TODO! : remove after rewrite tests to use common constructor
    @classmethod
    def from_items(cls, *args):
        return SeqWrapper(args)
