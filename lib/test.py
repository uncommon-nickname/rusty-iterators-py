from rusty_iterators import RustyIter

r = RustyIter.from_items(1, 2).map(lambda x: x * 2).collect()
print(r)
