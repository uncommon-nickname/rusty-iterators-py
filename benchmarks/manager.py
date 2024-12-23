from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING, Any, ClassVar, Iterable, final

if TYPE_CHECKING:
    type BenchmarkCallable[T] = Callable[[Iterable[T]], None]
    type BenchmarksStorage[T] = dict[str, tuple[BenchmarkCallable[T], Iterable[T]]]


@final
class Manager:
    scenarios: ClassVar[BenchmarksStorage[Any]] = {}

    @classmethod
    def register[T](cls, *, arg: Iterable[T]) -> Callable[[BenchmarkCallable[T]], BenchmarkCallable[T]]:
        def inner(benchmark: BenchmarkCallable[T]) -> BenchmarkCallable[T]:
            cls.scenarios[benchmark.__name__] = (benchmark, arg)
            return benchmark

        return inner
