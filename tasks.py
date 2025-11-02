"""Development tasks for the obsvty project."""
from invoke import task


@task
def test(c):
    """Run tests with coverage."""
    c.run("pytest --cov=src --cov-fail-under=80")


@task
def lint(c):
    """Run linting and formatting checks."""
    c.run("ruff check src tests")
    c.run("ruff format --check src tests")


@task
def typecheck(c):
    """Run type checking."""
    c.run("mypy src")


@task
def format_code(c):
    """Format code with ruff."""
    c.run("ruff format src tests")


@task
def install_hooks(c):
    """Install pre-commit hooks."""
    c.run("pre-commit install")


@task
def dev(c):
    """Run all development checks."""
    print("Running linting...")
    lint(c)
    print("Running type checking...")
    typecheck(c)
    print("Running tests...")
    test(c)
    print("All checks passed! 🎉")