from typing import Iterator

from rusty_iterators import Iter, NoValue, Value


class TestFilterMap:
    def test_apply_filter_map(self, gen: Iterator[int]) -> None:
        result = Iter(gen).filter_map(lambda x: Value(x**2) if x % 2 == 0 else NoValue()).collect()

        assert result == [4, 16]
