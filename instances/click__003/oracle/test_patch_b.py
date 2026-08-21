import pytest
import click


def test_distinct_command_with_duplicate_public_name_is_rejected():
    cli = click.Group("cli")
    cli.add_command(click.Command("sync"))

    with pytest.raises(TypeError, match="already registered"):
        cli.add_command(click.Command("sync"), "sync-alias")
