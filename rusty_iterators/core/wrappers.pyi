from __future__ import annotations

import sys
from collections.abc import Callable, Sequence
from typing import Any, Generic, Iterator, TypeAlias, final

from rusty_iterators.core.interface import IterInterface

if sys.version_info < (3, 11):
    pass
else:
    pass

if sys.version_info < (3, 13):
    from typing_extensions import TypeVar
else:
    from typing import TypeVar

T = TypeVar("T", default=Any, covariant=True)
R = TypeVar("R", default=Any, covariant=True)

FilterCallable: TypeAlias = Callable[[T], bool]
MapCallable: TypeAlias = Callable[[T], R]

@final
class SeqWrapper(IterInterface[T], Generic[T]):
    def __init__(self, s: Sequence[T]) -> None: ...
    def copy(self) -> bool: ...

@final
class IterWrapper(IterInterface[T], Generic[T]):
    def __init__(self, it: Iterator[T]) -> None: ...
    def copy(self) -> bool: ...
