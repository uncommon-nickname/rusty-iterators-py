from __future__ import annotations

from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    type Maybe[T] = Value[T] | NoValue


class Value[T]:
    __slots__ = ("exists", "value")

    def __init__(self, value: T) -> None:
        self.value = value
        self.exists: Literal[True] = True


class NoValue:
    __slots__ = ("exists",)

    def __init__(self) -> None:
        self.exists: Literal[False] = False
