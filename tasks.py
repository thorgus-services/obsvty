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
    c.run("ruff check --fix src tests")


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


@task
def generate_protos(c, ref="main", force=False):
    """Generate gRPC stubs from OTLP proto files.

    Args:
        ref: Branch or tag to fetch (default: main)
        force: Force re-download and regeneration
    """
    cmd = f"python generate_protos.py --ref {ref}"
    if force:
        cmd += " --force"
    c.run(cmd)


@task
def safety_check(c):
    """Run dependency vulnerability scanning using Safety."""
    c.run("safety check --full-report")


@task
def docker_build(c):
    """Build development Docker image."""
    c.run("docker build -t obsvty:dev .")


@task
def setup(c):
    """Run initial setup: generate protos and run dev checks."""
    generate_protos(c)
    dev(c)