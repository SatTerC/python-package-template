# Python Package Template

A cookiecutter template for creating modern Python packages with:
- [`uv`](https://docs.astral.sh/uv/) - Fast Python package manager
- [`just`](https://just.systems/) - Command runner
- [`ruff`](https://docs.astral.sh/ruff/) - Linting and formatting
- [`pyright`](https://github.com/microsoft/pyright) - Static type checking
- [`pytest`](https://pytest.org/) - Testing
- [`zensical`](https://zensical.org/) - Documentation (MkDocs-based)

## Requirements

- [uv](https://docs.astral.sh/uv/)

## Usage

```bash
uvx cookiecutter gh:SatTerC/python-package-template
```


## Resulting Structure

```
your-package/
├── .github/workflows/   # CI and docs deployment
├── .gitignore
├── .pre-commit-config.yaml
├── .python-version
├── LICENSE
├── README.md
├── justfile
├── pyproject.toml
├── zensical.toml
├── docs/
├── src/your_package/
└── tests/
```
