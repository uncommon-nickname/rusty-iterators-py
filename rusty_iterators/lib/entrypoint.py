from __future__ import annotations

import sys
from collections.abc import AsyncIterator, Iterator, Sequence
from typing import Any, Generic

from rusty_iterators.core.interface import IterWrapper, SeqWrapper

from ._async import AsyncIterWrapper

# NOTE: 30.01.2025 <@uncommon-nickname>
# TypeVar contains the `default` argument from Python 3.13. Earlier
# versions should use the backported one. We need the `default` to make
# types work correctly with empty iterators.
if sys.version_info < (3, 13):
    from typing_extensions import TypeVar
else:
    from typing import TypeVar


T = TypeVar("T", default=Any, contravariant=True)


class LIter(Generic[T]):
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
