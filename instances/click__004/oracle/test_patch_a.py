import click
from click.testing import CliRunner


def test_unique_prefix_invocation_resolves_command():
    @click.group()
    def cli():
        pass

    @cli.command("status")
    def status():
        click.echo("ok")

    @cli.command("stop")
    def stop():
        click.echo("stop")

    result = CliRunner().invoke(cli, ["sta"])

    assert result.output == "ok\n"
