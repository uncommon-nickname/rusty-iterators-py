import pytest

from rusty_iterators import IterInterface, IterNotCopiableError, RustyIter


@pytest.mark.parametrize("it", (RustyIter.from_seq([1, 2, 3]), RustyIter.from_items(1, 2, 3)))
def test_sequence_iter_is_copiable(it: IterInterface[int]) -> None:
    assert it.can_be_copied()
    it.copy()


def test_it_iter_is_not_copiable() -> None:
    it = RustyIter.from_it(x for x in [1, 2, 3])

    assert not it.can_be_copied()

    with pytest.raises(IterNotCopiableError):
        it.copy()
