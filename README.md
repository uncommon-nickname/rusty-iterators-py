# Rusty iterators

Have you ever written a script in Python and wondered why you can't have lightweight, lazy, and easy-to-use iterators just like in Rust? Don't worry, we've got you covered - `rusty-iterators` bring the same interface to Python! And all of that with modern, strong static typing!

## Coding code of conduct

Any contributions are welcome, but please adhere to our code of conduct.

### Conventional Commits

We utilize [conventional commits](https://gist.github.com/qoomon/5dfcdf8eec66a051ecd85625518cfd13). We don't maintain a `changelog` manually. Squashed commits, keeping the correct convention should be more than enough to create a release summary.

## Examples

Here are some quick and easy examples to show you the power of lazy iterators!

### Parsing file input

```python
file_handle = open("p.txt", "r")

result = Iter(file_handle)
        .map(lambda l: Iter(c for c in l).filter(lambda c: c.isnumeric()).map(lambda c: int(c)).collect())
        .collect()

file_handle.close()
```

### Counting all even numbers in the iterator

```python
it = iter(range(10, 1500))
result = Iter(it).filter(lambda x: x % 2 == 0).count()
```

### Creating a cycle iterator over all odd numbers in the array

```python
it = Iter.from_iterable([1, 2, 3, 4]).filter(lambda x: x % 2 != 0).cycle()
```

### Iterating with indices over all even numbers in the iterator

```python
it = iter(range(10))
for idx, value in Iter(it).filter(lambda x: x % 2 == 0).enumerate():
        print(idx, value)
```

## Authors

- [Wiktor Nowak](@uncommon-nickname)
