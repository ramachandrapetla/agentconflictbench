import click
from click.testing import CliRunner


def test_uppercase_underscore_does_not_transitively_resolve_dashed_command():
    @click.group()
    def cli():
        pass

    @cli.command("foo-bar")
    def foo_bar():
        click.echo("dash")

    result = CliRunner().invoke(cli, ["FOO_BAR"])

    assert result.exit_code != 0
    assert "No such command 'foo_bar'" in result.output
