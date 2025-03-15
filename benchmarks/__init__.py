import logging

from .scenarios import (
    benchmark_itertools_cycle,
    benchmark_more_itertools_filter_map,
    benchmark_more_itertools_flatten,
    benchmark_more_itertools_nth,
    benchmark_more_itertools_take,
    benchmark_more_itertools_unzip,
    benchmark_rusty_iterators_cache_cycle,
    benchmark_rusty_iterators_copy_cycle,
    benchmark_rusty_iterators_count,
    benchmark_rusty_iterators_filter,
    benchmark_rusty_iterators_filter_map,
    benchmark_rusty_iterators_flatten,
    benchmark_rusty_iterators_map,
    benchmark_rusty_iterators_nth,
    benchmark_rusty_iterators_sequence_wrapper,
    benchmark_rusty_iterators_take,
    benchmark_rusty_iterators_unzip,
    benchmark_stdlib_count,
    benchmark_stdlib_filter,
    benchmark_stdlib_map,
)

__all__ = (
    "benchmark_itertools_cycle",
    "benchmark_more_itertools_filter_map",
    "benchmark_more_itertools_flatten",
    "benchmark_more_itertools_nth",
    "benchmark_more_itertools_take",
    "benchmark_more_itertools_unzip",
    "benchmark_rusty_iterators_cache_cycle",
    "benchmark_rusty_iterators_copy_cycle",
    "benchmark_rusty_iterators_count",
    "benchmark_rusty_iterators_filter",
    "benchmark_rusty_iterators_filter_map",
    "benchmark_rusty_iterators_flatten",
    "benchmark_rusty_iterators_map",
    "benchmark_rusty_iterators_nth",
    "benchmark_rusty_iterators_sequence_wrapper",
    "benchmark_rusty_iterators_take",
    "benchmark_rusty_iterators_unzip",
    "benchmark_stdlib_count",
    "benchmark_stdlib_filter",
    "benchmark_stdlib_map",
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s.%(msecs)03d [%(levelname)s]: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
