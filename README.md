# Rusty iterators

Have you ever worked with a script in `Python` and wondered, why you can't have fast, light, lazy and easy-to-use iterators just like in `Rust`? Don't worry, we've got you covered - `rusty-iterators` bring the same interface to `Python`! And all of that without taking any shortcuts:

- Thanks to `Cython`, the performance is comparable with `itertools` and `stdlib`, but with friendly functional programming syntax!
- No production dependencies!
- Full support for modern static typing, compatible with `Python >= 3.10`!
- Basic support for async programming, with even more to come!

Project heavily inspired by great `Rust` iterators and crates like `Rayon` and `Itertools`. Make sure to check them out as well!

## 🛠 Local build and installation

As a build system and dependency manager we use [uv](https://docs.astral.sh/uv/getting-started/installation/). As a build backend we use `setuptools` with `cython`. We provide a simple `Makefile` for easier development command access. To install the development dependencies, you can run:

```bash
make install
```

To create a distributable package (`.whl`), run:

```bash
make build
```

this will generate the `C` code from cython files, compile them into the `.so` libraries and build the final package with type stubs. A new `dist/` directory will appear in the project root, where your distributable will be stored.

To install the built package for local testing:

```bash
pip3 install dist/rusty_iterators-<your-build-version>.whl
```

## Coding code of conduct

Any contributions are welcome, but please adhere to our code of conduct.

#### Conventional commits

We utilize [conventional commits](https://gist.github.com/qoomon/5dfcdf8eec66a051ecd85625518cfd13). We don't maintain a `changelog` manually. Squashed commits, keeping the correct convention should be more than enough to create a release summary.

#### Linting and formatting

As a linter and formatter, we use [ruff](https://docs.astral.sh/ruff/). You can run it via:

```bash
make lint
```

All changes, should ship with proper format and no lint errors, which will be verified in CI.

#### Static typing

We are huge advocates of statically typed Python and put a lot of effort into keeping the types as clean as possible. We also maintain the types static tests located in the `tests/types/` directory. All of the contributed code should be properly typed and make changes in the type stubs if needed. To check the types:

```bash
make mypy
```

#### Testing

All changes should ship with proper tests. We support multiple `python` versions, so to ensure everything works on every version, you can run the test on all of the via `tox`:

```bash
make tox
```

You can also run the tests on your current version:

```bash
make test
```

## Examples

Project is still in development and we don't have any proper documentation, so for now you can check out some very simple examples. More complex code can be found in the `examples/` directory.

#### Count all even numbers in the iterator

```python
from rusty_iterators import LIter

result = LIter.from_items(1, 2, 3, 4).filter(lambda x: x % 2 == 0).count()
```

#### Check if iterator is incremental

```python
from rusty_iterators import LIter

result = (
        LIter.from_items(1, 2, 4, 3)
        .moving_window(2)
        .map(lambda pair: pair[0] <= pair[1])
        .all()
)
```

#### Iterate with indices over all even numbers in the iterator

```python
from rusty_iterators import LIter

it = LIter.from_items(1, 2, 3, 4).filter(lambda x: x % 2 == 0).enumerate()

for idx, value in it:
        print(idx, value)
```

#### Get `n` items from cycle iterator

```python
from rusty_iterators import LIter

result = (
        LIter.from_items(1, 2, 3, 4)
        .map(lambda x: x**2)
        .cycle()
        .take(30)
        .collect()
)
```

#### Parse file line by line

```python
from rusty_iterators import LIter

with open("example.txt", "r") as file:
    result = (
        LIter.from_it(file)
        .map(lambda l: LIter.from_seq(l).filter(lambda c: c.isnumeric()).map(lambda c: int(c)).collect())
        .collect()
    )
```

#### Dispatch asyncio tasks and wait for their execution

```python
async def fetch_data(url: str) -> Optional[bytes]:
        # Some blocking api call.
        ...

async def wait_for_task[T](task: asyncio.Task[T]) -> T:
        return await task

tasks = (
    LIter.from_items(1, 2, 3)
    .map(lambda num: f"https://mywebsite/api/items/{num}")
    .map(lambda url: fetch_data(url))
    .map(lambda crt: asyncio.create_task(crt))
    .collect_into(tuple)
)

results = await LIter.from_seq(tasks).as_async().amap(wait_for_task).acollect()
```

## Authors

- [Wiktor Nowak](@uncommon-nickname)
- [Dawid Sielużycki](@Leghart)
