# Python Package Template

A cookiecutter template for creating modern Python packages with:
- [`uv`](https://docs.astral.sh/uv/) - Fast Python package manager
- [`just`](https://just.systems/) - Command runner
- [`ruff`](https://docs.astral.sh/ruff/) - Linting and formatting
- [`pyright`](https://github.com/microsoft/pyright) - Static type checking
- [`pytest`](https://pytest.org/) with [`hypothesis`](https://hypothesis.readthedocs.io/) - Testing
- [`zensical`](https://zensical.org/) - Documentation (MkDocs-based)

## Usage

Install cookiecutter if you haven't already:

```bash
pip install cookiecutter
```

Generate a new package:

```bash
cookiecutter gh:SatTerC/python-package-template
```

Or clone and run locally:

```bash
git clone https://github.com/SatTerC/python-package-template.git
cd python-package-template
cookiecutter .
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
