# Rusty iterators

Have you ever written a script in Python and wondered why you can't have lightweight, lazy, and easy-to-use iterators just like in Rust? Don't worry, we've got you covered - `rusty-iterators` bring the same interface to Python!"

## Coding code of conduct

Any contributions are welcome, but please adhere to our code of conduct.

### Conventional Commits

We utilize [conventional commits](https://gist.github.com/qoomon/5dfcdf8eec66a051ecd85625518cfd13). We don't maintain a `changelog` manually. Squashed commits, keeping the correct convention should be more than enough to create a release summary.

## Examples

Here are some quick and easy examples to show the power of lazy iterators!

### Parsing file input

Lazily loading a file to the memory by lines, and parsing each line into the list containing only numeric characters casted into integers.

```python
file_handle = open("p.txt", "r")

result = Iter(file_handle)
        .map(lambda l: Iter(c for c in l).filter(lambda c: c.isnumeric()).map(lambda c: int(c)).collect())
        .collect()

file_handle.close()
```

## Authors

- [Wiktor Nowak](@uncommon-nickname)
