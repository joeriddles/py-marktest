# py-marktest

<p style="align: center">
    <a href="https://pypi.org/project/py-marktest" target="_blank">
        <img src="https://img.shields.io/pypi/v/py-marktest?label=PyPI" alt="Package version" />
    </a>
</p

# <!-- this reset markdown mode somehow -->

### What is py-marktest and why you need it

py-marktest helps you test Python code samples in your markdown files. These code samples can include REPL snippets and code blocks.

---

### Local development

Bootstrap your local environment. This will create a new virtual environment in `./.venv` and install the dev dependencies from `pyproject.toml`.
```shell
make setup
```

Run all tests and report test coverage.
```shell
make test cov
```

---

### Build

Note: these comands assume a valid [`~/.pypirc`](https://packaging.python.org/en/latest/specifications/pypirc/) file is configured.

See the [official packaging docs](https://packaging.python.org/en/latest/tutorials/packaging-projects/) for more info.

```shell
python3 -m pip install --upgrade build twine
python3 -m build
```

Upload to [test.pypi.org](https://test.pypi.org)

```shell
python3 -m twine upload --repository testpypi dist/*
```

Upload to [PyPI](https://pypi.org)

```shell
python3 -m twine upload dist/*
```
