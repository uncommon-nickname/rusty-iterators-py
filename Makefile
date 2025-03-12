sources = benchmarks examples rusty_iterators tests

.uv:
	@uv -V || echo "Missing `uv`. Installation guide: https://docs.astral.sh/uv/getting-started/installation/"

.PHONY: install
install: .uv
	uv sync --frozen --group dev --all-extras
	uv pip install pre-commit
	uv run pre-commit install --install-hooks

.PHONY: build
build: .uv
	uv build

.PHONY: format
format: .uv
	uv run ruff format $(sources)

.PHONY: lint
lint: .uv
	uv run ruff check $(sources)
	uv run mypy $(sources) --check

.PHONY: tox
tox: .uv
	uv run tox

.PHONY: test
test: .uv
	uv run pytest -s -v

.PHONY: bench
bench: .uv
	uv run python3 -m benchmarks

.PHONY: clean
clean:
	rm -rf `find . -name __pycache__`
	rm -rf *.egg-info
	rm -rf .mypy_cache
	rm -rf .ruff_cache
	rm -rf .pytest_cache
	rm -rf .tox
	rm -rf build
	rm -rf dist
