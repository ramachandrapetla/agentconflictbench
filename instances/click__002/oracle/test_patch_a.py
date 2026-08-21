import click
from click.testing import CliRunner


def test_underscore_invocation_resolves_dashed_command():
    @click.group()
    def cli():
        pass

    @cli.command("foo-bar")
    def foo_bar():
        click.echo("dash")

    result = CliRunner().invoke(cli, ["foo_bar"])

    assert result.output == "dash\n"
