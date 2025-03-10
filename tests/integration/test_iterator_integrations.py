from rusty_iterators import LIter


def test_filter_map() -> None:
    it = LIter.from_items(1, 2, 3, 4).filter(lambda x: x % 2 == 0).map(lambda x: x.to_bytes(length=1, byteorder="big"))

    assert it.collect() == [b"\x02", b"\x04"]


def test_unzip_iterator_built_via_map() -> None:
    left, right = LIter.from_items("ac", "bde", "casd").map(lambda x: (len(x), x)).unzip()

    assert left == [2, 3, 4]
    assert right == ["ac", "bde", "casd"]
