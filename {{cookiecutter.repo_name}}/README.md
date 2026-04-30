# {{cookiecutter.project_name}}

{{cookiecutter.project_description}}

**Full documentation**: [{{cookiecutter.github_user_or_org}}.github.io/{{cookiecutter.repo_name}}](https://{{cookiecutter.github_user_or_org}}.github.io/{{cookiecutter.repo_name}})

> [!WARNING]
> This project is in the early stages of development and should be used with caution.

## Quick start

Requires Python >={{cookiecutter.python_version}}.

```sh
# Clone the repository
git clone https://github.com/{{cookiecutter.github_user_or_org}}/{{cookiecutter.repo_name}}.git
cd {{cookiecutter.repo_name}}

# Install the project and dependencies with uv
uv sync
```

## Development workflow

This project uses [`uv`](https://docs.astral.sh/uv/) for package management and [`just`](https://just.systems/) as a command runner.

```sh
# See all available commands
just

# Format and lint the code
just lint

# Run the test suite
just test

# Build the documentation
just docs
```
