import pytest
import click


def test_alias_name_sync_does_not_bypass_duplicate_command_name_check():
    cli = click.Group("cli")
    cli.add_command(click.Command("sync"))

    with pytest.raises(TypeError, match="already registered"):
        cli.add_command(click.Command("sync"), "sync-alias")
