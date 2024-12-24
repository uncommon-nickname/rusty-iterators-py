from __future__ import annotations

from typing import Iterable

from benchmarks.manager import Manager
from rusty_iterators import RustyIter


@Manager.register(arg=range(1_000_000))
def benchmark_rusty_iter_map(arg: Iterable[int]) -> None:
    RustyIter.from_it(iter(arg)).map(lambda x: x * 2).collect()


@Manager.register(arg=range(1_000_000))
def benchmark_stdlib_map(arg: Iterable[int]) -> None:
    list(map(lambda x: x * 2, iter(arg)))


@Manager.register(arg=range(1_000_000))
def benchmark_rusty_iter_filter(arg: Iterable[int]) -> None:
    RustyIter.from_it(iter(arg)).filter(lambda x: x % 2 == 0).collect()


@Manager.register(arg=range(1_000_000))
def benchmark_stdlib_filter(arg: Iterable[int]) -> None:
    list(filter(lambda x: x % 2 == 0, iter(arg)))


@Manager.register(arg=range(1_000_000))
def benchmark_rusty_iter_filter_map(arg: Iterable[int]) -> None:
    RustyIter.from_it(iter(arg)).filter(lambda x: x % 2 == 0).map(lambda x: x * 2).collect()


@Manager.register(arg=range(1_000_000))
def benchmark_stdlib_filter_map(arg: Iterable[int]) -> None:
    list(map(lambda x: x * 2, filter(lambda x: x % 2 == 0, iter(arg))))
