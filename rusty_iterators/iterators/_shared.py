from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Self


class CopyIterInterface(ABC):
    """An interface providing copy support for the iterator class."""

    __slots__ = ()

    @abstractmethod
    def can_be_copied(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def copy(self) -> Self:
        raise NotImplementedError
