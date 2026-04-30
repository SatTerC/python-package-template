---
title: Getting Started
icon: lucide/rocket
---

# Getting Started

## Installation

Install the package via `pip` or `uv`.

=== "pip"

    ``` sh
    pip install git+https://github.com/{{cookiecutter.github_user_or_org}}/{{cookiecutter.repo_name}}
    ```

=== "uv"

    ``` sh
    uv add git+https://github.com/{{cookiecutter.github_user_or_org}}/{{cookiecutter.repo_name}}
    ```

## Basic usage

```python
from {{cookiecutter.package_name}} import main

# Your code here
result = main()
print(result)
```

See the [API Reference](API_Reference/{{cookiecutter.package_name}}.md) for full documentation.
