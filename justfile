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
    --output-dir tmp/cookiecutter-output \
    project_name="Test Project" \
    project_description="Test" \
    author_name="Test Author" \
    author_email="test@example.com" \
    github_username="testuser" \
    python_version="3.13"

  # Run just commands within the generated project
  cd tmp/cookiecutter-output/test-project && \
    uv run just lint test typecheck docs

# Remove temporary cookiecutter output directory.
clean:
  rm -r tmp/cookiecutter-output
