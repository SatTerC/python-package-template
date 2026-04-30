# Default recipe to display available commands.
_:
  @just --list

# Run the cookiecutter template tests.
test *args="":
  uvx ruff format test_cookiecutter_template.py
  uvx ruff check test_cookiecutter_template.py
  uv run test_cookiecutter_template.py -v {{args}}

# Generate project from template, lint, and build docs.
validate:
  uvx cookiecutter . --no-input --overwrite-if-exists \
    --output-dir tmp \
    project_name="Python Package Template" \
    project_description="A cookiecutter template for Python packages." \
    author_name="jmarshrossney" \
    author_email="17361029+jmarshrossney@users.noreply.github.com" \
    github_user_or_org="SatTerC" \
    python_version="3.13"

  # Run just commands within the generated project
  cd tmp/python-package-template && \
    uv run just lint test typecheck docs

# Remove temporary cookiecutter output directory.
clean:
  rm -r tmp/python-package-template
