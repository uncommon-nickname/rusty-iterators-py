from typing import Iterator

import pytest


@pytest.fixture
def empty_gen() -> Iterator[int]:
    empty: list[int] = []
    return (x for x in empty)


@pytest.fixture
def gen() -> Iterator[int]:
    return (x for x in [1, 2, 3, 4])
