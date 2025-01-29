# Rusty iterators

Have you ever written a script in Python and wondered why you can't have lightweight, lazy, and easy-to-use iterators just like in Rust? Don't worry, we've got you covered - `rusty-iterators` bring the same interface to Python! And all of that with modern, strong static typing!

## Coding code of conduct

Any contributions are welcome, but please adhere to our code of conduct.

### Conventional Commits

We utilize [conventional commits](https://gist.github.com/qoomon/5dfcdf8eec66a051ecd85625518cfd13). We don't maintain a `changelog` manually. Squashed commits, keeping the correct convention should be more than enough to create a release summary.

## Examples

Some interesting use cases showing the power of lazy iteration.

### Count all even numbers in the iterator

```python
result = LIter.build(iter(range(10, 1500))).filter(lambda x: x % 2 == 0).count()
```

### Check if iterator is incremental

```python
result = (
        LIter.build(1, 2, 3, 6, 5)
        .moving_window(2)
        .map(lambda arr: arr[0] <= arr[1])
        .all()
)
```

### Iterate with indices over all even numbers in the iterator

```python
it = LIter.build(iter(range(10))).filter(lambda x: x % 2 == 0).enumerate()

for idx, value in it:
        print(idx, value)
```

### Get `n` items from cycle iterator

```python
result = (
        LIter.build(1, 2, 3, 4)
        .map(lambda x: x**2)
        .cycle()
        .take(30)
        .collect()
)
```

### Parse file line by line

```python
file_handle = open("p.txt", "r")

result = (
    LIter.build(file_handle)
    .map(lambda l: LIter.build(c for c in l).filter(lambda c: c.isnumeric()).map(lambda c: int(c)).collect())
    .collect()
)

file_handle.close()
```

### Dispatch asyncio tasks and wait for their execution

```python
async def fetch_data(url: str) -> Optional[bytes]:
        # Some blocking api call.
        ...

async def wait_for_task[T](task: asyncio.Task[T]) -> T:
        return await task

tasks = (
    LIter.build(1, 2, 3)
    .map(lambda num: f"https://mywebsite/api/items/{num}")
    .map(lambda url: fetch_data(url))
    .map(lambda crt: asyncio.create_task(crt))
    .collect_into(tuple)
)

results = await LIter.build(tasks).as_async().amap(wait_for_task).acollect()
```
## 🛠 Build & Installation
To create a distributable package (.whl):
```
poetry build
```
this command will compile cython extensions, copy stubs into package and create `dist/` directory.

To install the built package for local testing:
```
pip install dist/rusty_iterators-{your_build_version}.whl
```

## Authors

- [Wiktor Nowak](@uncommon-nickname)
- [Dawid Sielużycki](@Leghart)
