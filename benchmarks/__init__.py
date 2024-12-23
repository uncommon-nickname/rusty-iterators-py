import logging

from .scenarios.iterators import (
    benchmark_rusty_iter_filter,
    benchmark_rusty_iter_filter_map,
    benchmark_rusty_iter_map,
    benchmark_stdlib_filter,
    benchmark_stdlib_filter_map,
    benchmark_stdlib_map,
)

__all__ = (
    "benchmark_rusty_iter_filter",
    "benchmark_rusty_iter_filter_map",
    "benchmark_rusty_iter_map",
    "benchmark_stdlib_filter",
    "benchmark_stdlib_filter_map",
    "benchmark_stdlib_map",
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s.%(msecs)03d [%(levelname)s]: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
