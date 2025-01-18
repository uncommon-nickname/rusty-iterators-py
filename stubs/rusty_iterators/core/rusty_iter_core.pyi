from __future__ import annotations

from .interface import SeqWrapper

class RustyIter[T]:
    @classmethod
    def from_items(cls, *args: T) -> SeqWrapper[T]: ...
