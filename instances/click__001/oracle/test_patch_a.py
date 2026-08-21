import click
from click.testing import CliRunner


def test_default_map_accepts_dashed_option_name():
    @click.command()
    @click.option("--api-key")
    def cli(api_key):
        click.echo(api_key)

    result = CliRunner().invoke(cli, [], default_map={"api-key": "from-map"})

    assert result.output == "from-map\n"
