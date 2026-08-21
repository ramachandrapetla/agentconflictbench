import typer
from typer.testing import CliRunner


def test_uppercase_invocation_resolves_lowercase_command():
    app = typer.Typer()

    @app.command("status")
    def status():
        typer.echo("ok")

    @app.command("other")
    def other():
        typer.echo("other")

    result = CliRunner().invoke(app, ["STATUS"])

    assert result.output == "ok\n"
