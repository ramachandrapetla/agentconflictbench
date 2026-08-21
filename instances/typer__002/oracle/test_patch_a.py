import typer
from typer.testing import CliRunner


def test_unique_prefix_invocation_resolves_command():
    app = typer.Typer()

    @app.command("status")
    def status():
        typer.echo("ok")

    @app.command("stop")
    def stop():
        typer.echo("stop")

    result = CliRunner().invoke(app, ["sta"])

    assert result.output == "ok\n"
