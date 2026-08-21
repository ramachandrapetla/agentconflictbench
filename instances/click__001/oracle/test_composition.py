import click
from click.testing import CliRunner


def test_dashed_default_map_alias_does_not_override_auto_envvar():
    @click.command()
    @click.option("--api-key")
    def cli(api_key):
        click.echo(api_key)

    result = CliRunner().invoke(
        cli,
        [],
        auto_envvar_prefix="APP",
        default_map={"api-key": "from-map"},
        env={"APP_API_KEY": "from-env"},
    )

    assert result.output == "from-env\n"
