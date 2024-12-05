from typing import Generator

import pytest


@pytest.fixture
def empty_gen() -> Generator[int, None, None]:
    empty: list[int] = []
    return (x for x in empty)


@pytest.fixture
def gen() -> Generator[int, None, None]:
    return (x for x in [1, 2, 3, 4])
