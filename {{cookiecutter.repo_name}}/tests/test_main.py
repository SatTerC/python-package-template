"""Tests for main module."""


def test_main():
    """Test that main function returns expected output."""
    from {{cookiecutter.package_name}}.main import main

    result = main()
    assert isinstance(result, str)
    assert "{{cookiecutter.package_name}}" in result
