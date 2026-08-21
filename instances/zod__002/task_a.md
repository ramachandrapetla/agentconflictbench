# Task A: Clear object refinements on catchall variants

## Problem

Changing an object schema's catchall policy can produce a variant intended to
validate unknown keys independently from previous object-level refinements.

## Desired behavior

Clear object-level refinements when creating a catchall object-schema variant.

## Constraints

The new catchall schema should still validate known properties and unknown keys
according to the supplied catchall type.

## Success criteria

An object schema with a failing refinement can produce a `.catchall(z.unknown())`
variant that accepts an otherwise valid object with extra keys.
