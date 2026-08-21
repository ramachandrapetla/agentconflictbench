# Task B: Reject duplicate public command names

## Problem

A group can become ambiguous if two distinct command objects expose the same
public command name.

## Desired behavior

Reject registration of a distinct command object when its public command name is
already registered on the same group.

## Constraints

Re-registering the same command object should not be treated as a distinct-name
collision unless existing Click behavior already rejects it.

## Success criteria

Attempting to add two different command objects with the same public name raises
a registration error.
