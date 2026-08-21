import click


def test_explicit_registration_name_updates_command_name():
    cli = click.Group("cli")
    cmd = click.Command("internal")

    cli.add_command(cmd, "public")

    assert cmd.name == "public"
    assert cli.commands["public"] is cmd
