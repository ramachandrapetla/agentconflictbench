# Task A: Inherit metadata IDs across schema clones

## Problem

Zod schema variants produced through cloning can lose metadata IDs that callers
use to track schema identity.

## Desired behavior

Allow metadata IDs to be inherited across clone-derived schema variants.

## Constraints

Other metadata behavior should remain stable, and explicit metadata on the
derived schema should take precedence over inherited values.

## Success criteria

A schema with metadata `{ id: "UserName" }` retains that ID after creating a
clone-derived variant.
