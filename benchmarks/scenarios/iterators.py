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


@Manager.register(arg=[1, 2, 3, 4])
def benchmark_rusty_iter_cycle_copy_no_operations(arg: Iterable[int]) -> None:
    RustyIter.from_items(*arg).cycle(use_cache=False).take(1_000_000).collect()


@Manager.register(arg=[1, 2, 3, 4])
def benchmark_rusty_iter_cycle_cached_no_operations(arg: Iterable[int]) -> None:
    RustyIter.from_items(*arg).cycle(use_cache=True).take(1_000_000).collect()


@Manager.register(arg=[1, 2, 3, 4])
def benchmark_rusty_iter_cycle_copy_operations(arg: Iterable[int]) -> None:
    RustyIter.from_items(*arg).map(lambda x: (x * x) / 4).cycle(use_cache=False).take(1_000_000).collect()


@Manager.register(arg=[1, 2, 3, 4])
def benchmark_rusty_iter_cycle_cached_operations(arg: Iterable[int]) -> None:
    RustyIter.from_items(*arg).map(lambda x: (x * x) / 4).cycle(use_cache=True).take(1_000_000).collect()
