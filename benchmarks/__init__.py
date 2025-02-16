import logging

from .scenarios import benchmark_rusty_iterators_map, benchmark_stdlib_iterators_map

__all__ = ("benchmark_rusty_iterators_map", "benchmark_stdlib_iterators_map")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s.%(msecs)03d [%(levelname)s]: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
