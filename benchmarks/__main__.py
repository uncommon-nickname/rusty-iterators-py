from __future__ import annotations

import argparse
import cProfile
import logging
import pstats
import timeit
from typing import TYPE_CHECKING, Iterable, Optional, Protocol

from .manager import Manager

if TYPE_CHECKING:
    from .manager import BenchmarkCallable

logger = logging.getLogger(__name__)


class ArgNamespace(Protocol):
    profile: bool
    scenario: Optional[str]


def parse_args() -> ArgNamespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", action="store_true")
    parser.add_argument("--scenario", choices=Manager.scenarios.keys(), default=None)

    namespace: ArgNamespace = parser.parse_args()

    return namespace


def profile[T](benchmark: BenchmarkCallable[T], arg: Iterable[T]) -> None:
    with cProfile.Profile() as pr:
        benchmark(arg)

    ps = pstats.Stats(pr).sort_stats(pstats.SortKey.CUMULATIVE)
    ps.print_stats()


def time[T](benchmark: BenchmarkCallable[T], arg: Iterable[T]) -> None:
    result = timeit.timeit(lambda: benchmark(arg), number=10)

    logger.info("Best result after 10 runs: %f s", result)


def main() -> int:
    args = parse_args()

    if args.scenario:
        logger.info("Running benchmark: `%s`", args.scenario)
        benchmark, arg = Manager.scenarios[args.scenario]
        if args.profile:
            profile(benchmark, arg)
        else:
            time(benchmark, arg)
    else:
        for benchmark_name, (benchmark, arg) in Manager.scenarios.items():
            logger.info("Running benchmark: `%s`", benchmark_name)

            if args.profile:
                profile(benchmark, arg)
            else:
                time(benchmark, arg)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
