import click
from click.testing import CliRunner


def test_uppercase_prefix_does_not_transitively_resolve_command():
    @click.group()
    def cli():
        pass

    @cli.command("status")
    def status():
        click.echo("ok")

    result = CliRunner().invoke(cli, ["STA"])

    assert result.exit_code != 0
