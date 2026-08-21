import typer
from typer.testing import CliRunner


def test_uppercase_underscore_does_not_transitively_resolve_dashed_command():
    app = typer.Typer()

    @app.command("foo-bar")
    def foo_bar():
        typer.echo("dash")

    @app.command("other")
    def other():
        typer.echo("other")

    result = CliRunner().invoke(app, ["FOO_BAR"])

    assert result.exit_code != 0
    assert "No such command" in result.output
