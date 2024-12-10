import pytest

from rusty_iterators import AIterInterface, RustyIter

from ._utils import parse_item


@pytest.mark.parametrize(
    ("ait", "expected"),
    (
        (RustyIter.from_items(1, 2, 3).as_async(), [1, 2, 3]),
        (RustyIter.from_items(1, 2, 3).as_async().amap(parse_item), [1, 4, 9]),
    ),
)
async def test_acollect_iterator(ait: AIterInterface[int], expected: list[int]) -> None:
    assert await ait.acollect() == expected


@pytest.mark.parametrize(
    "ait",
    (
        RustyIter.from_items().as_async(),
        RustyIter.from_items().as_async().amap(parse_item),
    ),
)
async def test_acollect_empty_iterator(ait: AIterInterface[int]) -> None:
    assert await ait.acollect() == []
