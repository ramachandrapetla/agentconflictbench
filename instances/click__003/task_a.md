# Task A: Reflect explicit registration aliases on command objects

## Problem

When a command is registered under an explicit name, the group exposes that
alias but the command object may still report its original public name.

## Desired behavior

Update a command object's public name to match the explicit API name used during
registration.

## Constraints

Only explicit registration aliases should trigger the rename. Commands added
without an alias should preserve their existing names.

## Success criteria

After registering a command with an explicit alias, inspecting the command's
public name returns the alias.
