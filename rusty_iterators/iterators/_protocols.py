from typing import TYPE_CHECKING, Iterator, Protocol

if not TYPE_CHECKING:
    raise ImportError("Do not import directly from _protocols module.")


class BuildableFromIterator[T](Protocol):
    def __init__(self, iterator: Iterator[T]) -> None: ...
