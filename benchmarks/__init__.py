import logging

from .scenarios import (
    benchmark_itertools_cycle,
    benchmark_rusty_iterators_cache_cycle,
    benchmark_rusty_iterators_copy_cycle,
    benchmark_rusty_iterators_filter,
    benchmark_rusty_iterators_flatten,
    benchmark_rusty_iterators_map,
    benchmark_stdlib_filter,
    benchmark_stdlib_flatten,
    benchmark_stdlib_map,
)

__all__ = (
    "benchmark_itertools_cycle",
    "benchmark_rusty_iterators_cache_cycle",
    "benchmark_rusty_iterators_copy_cycle",
    "benchmark_rusty_iterators_filter",
    "benchmark_rusty_iterators_flatten",
    "benchmark_rusty_iterators_map",
    "benchmark_stdlib_filter",
    "benchmark_stdlib_flatten",
    "benchmark_stdlib_map",
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s.%(msecs)03d [%(levelname)s]: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
