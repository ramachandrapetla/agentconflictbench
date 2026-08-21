import typer
from typer.testing import CliRunner


def test_uppercase_prefix_does_not_transitively_resolve_command():
    app = typer.Typer()

    @app.command("status")
    def status():
        typer.echo("ok")

    @app.command("other")
    def other():
        typer.echo("other")

    result = CliRunner().invoke(app, ["STA"])

    assert result.exit_code != 0
