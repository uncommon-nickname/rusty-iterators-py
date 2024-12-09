from typing import TYPE_CHECKING

if not TYPE_CHECKING:
    raise ImportError("Do not import directly from _types module.")

from collections.abc import Callable

from rusty_iterators.maybe import Maybe

type FilterCallable[T] = Callable[[T], bool]
type MapCallable[T, R] = Callable[[T], R]
type FilterMapCallable[T, R] = Callable[[T], Maybe[R]]
type ForEachCallable[T] = Callable[[T], None]
type InspectCallable[T] = ForEachCallable[T]

type StandardIterable[T] = list[T] | tuple[T, ...] | set[T] | frozenset[T]
type StandardIterableClass[T] = type[StandardIterable[T]]
