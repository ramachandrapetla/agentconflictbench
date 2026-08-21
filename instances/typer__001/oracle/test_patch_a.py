import typer
from typer.testing import CliRunner


def test_underscore_invocation_resolves_dashed_command():
    app = typer.Typer()

    @app.command("foo-bar")
    def foo_bar():
        typer.echo("dash")

    @app.command("other")
    def other():
        typer.echo("other")

    result = CliRunner().invoke(app, ["foo_bar"])

    assert result.output == "dash\n"
