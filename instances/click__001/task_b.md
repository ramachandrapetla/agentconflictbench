# Task B: Default-map precedence over auto envvars

## Problem

When both automatic environment variables and `default_map` are available,
applications may need explicit configuration-map values to override ambient
environment settings.

## Desired behavior

Update option resolution so a value from `Context.default_map` takes precedence
over an automatically derived environment variable value.

## Constraints

Explicit command-line arguments must still have the highest precedence. The
change should apply to automatically derived envvars, not necessarily every
custom envvar path.

## Success criteria

If `APP_API_KEY` is set and `default_map` also provides `api_key`, the command
uses the `default_map` value when no CLI argument is supplied.
