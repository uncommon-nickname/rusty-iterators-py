from rusty_iterators.lib import LIter


def test_filter_map() -> None:
    it = LIter.from_items(1, 2, 3, 4).filter(lambda x: x % 2 == 0).map(lambda x: x.to_bytes())

    assert it.collect() == [b"\x02", b"\x04"]
