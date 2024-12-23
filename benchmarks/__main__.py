from __future__ import annotations

import argparse
import cProfile
import logging
import pstats
import timeit
from typing import TYPE_CHECKING, Iterable

from .manager import Manager

if TYPE_CHECKING:
    from .manager import BenchmarkCallable

logger = logging.getLogger(__name__)


def parse_args() -> bool:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", action="store_true")

    run_profiler: bool = parser.parse_args().profile

    return run_profiler


def profile[T](benchmark: BenchmarkCallable[T], arg: Iterable[T]) -> None:
    with cProfile.Profile() as pr:
        benchmark(arg)

    ps = pstats.Stats(pr).sort_stats(pstats.SortKey.CUMULATIVE)
    ps.print_stats()


def time[T](benchmark: BenchmarkCallable[T], arg: Iterable[T]) -> None:
    result = timeit.timeit(lambda: benchmark(arg), number=10)

    logger.info("Best result after 10 runs: %f s", result)


def main() -> int:
    run_profiler = parse_args()

    for benchmark_name, (benchmark, arg) in Manager.scenarios.items():
        logger.info("Running benchmark: `%s`", benchmark_name)

        try:
            if run_profiler:
                profile(benchmark, arg)
            else:
                time(benchmark, arg)
        except Exception as exc:
            logger.error("Something went wrong: %s", exc)
            return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
