import pytest

from rusty_iterators import AIterInterface, RustyIter

from ._utils import parse_item


@pytest.mark.parametrize(
    ("ait", "expected"),
    (
        (RustyIter.from_items(3).as_async(), 3),
        (RustyIter.from_items(3).as_async().amap(parse_item), 9),
    ),
)
async def test_next(ait: AIterInterface[int], expected: int) -> None:
    assert await ait.anext() == expected


@pytest.mark.parametrize(
    "ait",
    (
        RustyIter.from_items().as_async(),
        RustyIter.from_items().as_async().amap(parse_item),
    ),
)
async def test_next_on_empty(ait: AIterInterface[int]) -> None:
    with pytest.raises(StopAsyncIteration):
        await ait.anext()
