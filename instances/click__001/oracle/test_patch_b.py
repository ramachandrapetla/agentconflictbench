import click
from click.testing import CliRunner


def test_default_map_overrides_auto_envvar():
    @click.command()
    @click.option("--api-key")
    def cli(api_key):
        click.echo(api_key)

    result = CliRunner().invoke(
        cli,
        [],
        auto_envvar_prefix="APP",
        default_map={"api_key": "from-map"},
        env={"APP_API_KEY": "from-env"},
    )

    assert result.output == "from-map\n"
