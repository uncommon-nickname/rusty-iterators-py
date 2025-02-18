import io
from contextlib import redirect_stdout

from rusty_iterators import LIter


def test_inspect_self() -> None:
    with io.StringIO() as buf, redirect_stdout(buf):
        LIter.from_items(1, 2).inspect().map(lambda x: x * 2).collect()
        assert buf.getvalue() == "SeqWrapper(ptr=1, s=2): 1\nSeqWrapper(ptr=2, s=2): 2\n"


def test_inspect_function() -> None:
    n = 0

    def incr(x: int) -> None:
        nonlocal n
        n += x

    LIter.from_items(1, 2, 3, 4).inspect(incr).collect()

    assert n == 10
