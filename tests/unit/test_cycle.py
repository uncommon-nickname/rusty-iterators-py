from rusty_iterators.lib import LIter


def test_default_iterator_returns_cache_based_cycle() -> None:
    _iter = (x for x in [1, 2, 3])
    it = LIter.from_it(_iter).cycle()

    assert not it.can_be_copied()
    assert str(it) == f"CycleCached(ptr=0, cache=0, it=IterWrapper(it={_iter}))"

    output = []
    for i, item in enumerate(it):
        if i == 7:
            break
        output.append(item)

    assert output == [1, 2, 3, 1, 2, 3, 1]


def test_when_specified_cycle_returns_cached() -> None:
    it = LIter.from_items("a", "b", "c").cycle(use_cache=True)

    assert str(it) == "CycleCached(ptr=0, cache=0, it=SeqWrapper(ptr=0, s=3))"

    output = []
    for i, item in enumerate(it):
        if i == 7:
            break
        output.append(item)

    assert output == ["a", "b", "c", "a", "b", "c", "a"]


def test_when_specified_cycle_returns_copy() -> None:
    it = LIter.from_items("a", "b", "c").cycle(use_cache=False)
    assert str(it) == "CycleCopy(it=SeqWrapper(ptr=0, s=3), orig=SeqWrapper(ptr=0, s=3))"

    output = []
    for i, item in enumerate(it):
        if i == 7:
            break
        output.append(item)

    assert output == ["a", "b", "c", "a", "b", "c", "a"]
