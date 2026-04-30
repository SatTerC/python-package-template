# /// script
# dependencies = ["pytest", "cookiecutter", "ruff"]
# ///

"""Tests for cookiecutter template generation."""

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest


@pytest.fixture
def template_dir():
    """Return the path to the cookiecutter template."""
    return Path(__file__).parent


@pytest.fixture
def cookiecutter_json(template_dir):
    """Load and return the cookiecutter.json configuration."""
    with open(template_dir / "cookiecutter.json") as f:
        return json.load(f)


def run_cookiecutter(template_path, output_dir, context, no_input=True):
    """Run cookiecutter with given context and return the generated project path."""
    # Build the command
    cmd = ["cookiecutter", str(template_path), "--output-dir", str(output_dir)]
    if no_input:
        cmd.append("--no-input")

    # Add context as environment variables
    env = os.environ.copy()
    for key, value in context.items():
        env[f"COOKIECUTTER_{key}"] = str(value)

    # Run with context values passed as command-line overrides
    for key, value in context.items():
        cmd.extend(["--overwrite-if-exists", f"{key}={value}"])

    result = subprocess.run(cmd, capture_output=True, text=True, env=env)
    if result.returncode != 0:
        raise RuntimeError(f"Cookiecutter failed: {result.stderr}")

    # Find the generated project directory
    dirs = [d for d in output_dir.iterdir() if d.is_dir()]
    if not dirs:
        raise RuntimeError("No project directory generated")
    return dirs[0]


class TestBasicGeneration:
    """Test basic template generation with default values."""

    def test_generates_project_directory(self, template_dir, tmp_path):
        """Test that cookiecutter generates a project directory."""
        context = {
            "project_name": "My Test Project",
            "project_description": "A test project",
            "author_name": "Test Author",
            "author_email": "test@example.com",
            "github_user_or_org": "testuser",
            "python_version": "3.13",
        }

        project_dir = run_cookiecutter(template_dir, tmp_path, context)

        assert project_dir.exists()
        assert project_dir.is_dir()

    def test_repo_name_is_dashed(self, template_dir, tmp_path):
        """Test that repo_name uses dashes (slugified from project_name)."""
        context = {
            "project_name": "My Test Project",
            "project_description": "A test project",
            "author_name": "Test Author",
            "author_email": "test@example.com",
            "github_user_or_org": "testuser",
            "python_version": "3.13",
        }

        project_dir = run_cookiecutter(template_dir, tmp_path, context)

        # project_name="My Test Project" should become repo_name="my-test-project"
        assert project_dir.name == "my-test-project"

    def test_package_name_is_underscored(self, template_dir, tmp_path):
        """Test that package_name uses underscores."""
        context = {
            "project_name": "My Test Project",
            "project_description": "A test project",
            "author_name": "Test Author",
            "author_email": "test@example.com",
            "github_user_or_org": "testuser",
            "python_version": "3.13",
        }

        project_dir = run_cookiecutter(template_dir, tmp_path, context)

        # Check that src/ contains the underscored package name
        src_dir = project_dir / "src"
        package_dirs = [d for d in src_dir.iterdir() if d.is_dir()]
        assert len(package_dirs) == 1
        assert package_dirs[0].name == "my_test_project"


class TestGeneratedFiles:
    """Test that generated files have correct content."""

    @pytest.fixture
    def generated_project(self, template_dir, tmp_path):
        """Generate a project and return its path."""
        context = {
            "project_name": "Cool Package",
            "project_description": "A really cool package",
            "author_name": "Jane Doe",
            "author_email": "jane@example.com",
            "github_user_or_org": "janedoe",
            "python_version": "3.12",
        }
        return run_cookiecutter(template_dir, tmp_path, context)

    def test_pyproject_toml_has_correct_name(self, generated_project):
        """Test that pyproject.toml has the correct package name."""
        pyproject = generated_project / "pyproject.toml"
        content = pyproject.read_text()

        assert 'name = "cool_package"' in content
        assert 'description = "A really cool package"' in content
        assert "Jane Doe" in content
        assert "jane@example.com" in content
        assert 'requires-python = ">=3.12"' in content

    def test_readme_has_correct_urls(self, generated_project):
        """Test that README.md has correct GitHub URLs with dashes."""
        readme = generated_project / "README.md"
        content = readme.read_text()

        assert "janedoe.github.io/cool-package" in content
        assert "github.com/janedoe/cool-package" in content
        assert "Cool Package" in content

    def test_zensical_toml_has_correct_urls(self, generated_project):
        """Test that zensical.toml has correct URLs."""
        zensical = generated_project / "zensical.toml"
        content = zensical.read_text()

        assert 'site_name = "Cool Package"' in content
        assert "janedoe.github.io/cool-package" in content
        assert "Jane Doe" in content

    def test_ci_workflow_preserves_github_expressions(self, generated_project):
        """Test that ci.yml preserves ${{ }} syntax for GitHub Actions."""
        ci_yml = generated_project / ".github" / "workflows" / "ci.yml"
        content = ci_yml.read_text()

        # Should have preserved the GitHub Actions expressions
        assert "${{ matrix.python-version }}" in content

    def test_docs_workflow_preserves_github_expressions(self, generated_project):
        """Test that docs.yml preserves ${{ }} syntax for GitHub Actions."""
        docs_yml = generated_project / ".github" / "workflows" / "docs.yml"
        content = docs_yml.read_text()

        # Should have preserved the GitHub Actions expressions
        assert "${{ steps.deployment.outputs.page_url }}" in content

    def test_justfile_has_correct_coverage_path(self, generated_project):
        """Test that justfile uses package_name for coverage."""
        justfile = generated_project / "justfile"
        content = justfile.read_text()

        assert "--cov=cool_package" in content
        assert "pyright src/cool_package" in content

    def test_source_files_exist(self, generated_project):
        """Test that source files are created with correct package name."""
        src_dir = generated_project / "src" / "cool_package"
        assert (src_dir / "__init__.py").exists()
        assert (src_dir / "_version.py").exists()
        assert (src_dir / "main.py").exists()

    def test_tests_exist(self, generated_project):
        """Test that test files are created."""
        tests_dir = generated_project / "tests"
        assert (tests_dir / "conftest.py").exists()
        assert (tests_dir / "test_main.py").exists()

    def test_docs_structure(self, generated_project):
        """Test that docs are created with correct structure."""
        docs_dir = generated_project / "docs"
        assert (docs_dir / "index.md").exists()
        assert (docs_dir / "getting-started.md").exists()
        assert (docs_dir / "API_Reference").exists()
        assert (docs_dir / "API_Reference" / "cool_package.md").exists()
        assert (docs_dir / "API_Reference" / "__init__.md").exists()


class TestSpecialCharacters:
    """Test handling of special characters in project names."""

    def test_project_name_with_apostrophe(self, template_dir, tmp_path):
        """Test that project names with apostrophes are handled correctly."""
        context = {
            "project_name": "It's a Project",
            "project_description": "Test",
            "author_name": "Author",
            "author_email": "author@example.com",
            "github_user_or_org": "author",
            "python_version": "3.13",
        }

        project_dir = run_cookiecutter(template_dir, tmp_path, context)

        # Slugify converts apostrophes to hyphens: "It's a Project" -> "it-s-a-project"
        assert project_dir.name == "it-s-a-project"

    def test_project_name_with_special_chars(self, template_dir, tmp_path):
        """Test that special characters are removed/cleaned by slugify."""
        context = {
            "project_name": "Project! @ #123",
            "project_description": "Test",
            "author_name": "Author",
            "author_email": "author@example.com",
            "github_user_or_org": "author",
            "python_version": "3.13",
        }

        project_dir = run_cookiecutter(template_dir, tmp_path, context)

        # Should produce a clean slug
        assert "!" not in project_dir.name
        assert "@" not in project_dir.name
        assert "#" not in project_dir.name


class TestTemplateStructure:
    """Test the overall template structure is correct."""

    def test_required_files_exist(self, template_dir):
        """Test that the template directory has all required files."""
        assert (template_dir / "cookiecutter.json").exists()
        assert (template_dir / "{{cookiecutter.repo_name}}").exists()
        assert (template_dir / "{{cookiecutter.repo_name}}" / "pyproject.toml").exists()
        assert (template_dir / "{{cookiecutter.repo_name}}" / "README.md").exists()
        assert (template_dir / "{{cookiecutter.repo_name}}" / "justfile").exists()
        assert (template_dir / "{{cookiecutter.repo_name}}" / "zensical.toml").exists()
        assert (
            template_dir
            / "{{cookiecutter.repo_name}}"
            / ".github"
            / "workflows"
            / "ci.yml"
        ).exists()
        assert (
            template_dir
            / "{{cookiecutter.repo_name}}"
            / ".github"
            / "workflows"
            / "docs.yml"
        ).exists()

    def test_cookiecutter_json_valid(self, template_dir):
        """Test that cookiecutter.json is valid and has required fields."""
        with open(template_dir / "cookiecutter.json") as f:
            config = json.load(f)

        assert "_extensions" in config
        assert "cookiecutter.extensions.SlugifyExtension" in config["_extensions"]
        assert "project_name" in config
        assert "repo_name" in config
        assert "package_name" in config
        assert "author_name" in config
        assert "github_user_or_org" in config

    def test_slugify_in_cookiecutter_json(self, template_dir):
        """Test that repo_name and package_name use slugify correctly."""
        with open(template_dir / "cookiecutter.json") as f:
            config = json.load(f)

        assert "slugify" in config["repo_name"]
        assert "slugify" in config["package_name"]
        assert "separator='_'" in config["package_name"]


if __name__ == "__main__":
    sys.exit(pytest.main([__file__] + sys.argv[1:]))
