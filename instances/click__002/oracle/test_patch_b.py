import click
from click.testing import CliRunner


def test_uppercase_invocation_resolves_lowercase_command():
    @click.group()
    def cli():
        pass

    @cli.command("status")
    def status():
        click.echo("ok")

    result = CliRunner().invoke(cli, ["STATUS"])

    assert result.output == "ok\n"
