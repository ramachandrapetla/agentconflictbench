# Task A: Extend trailing inline style spans during right padding

## Problem

When right-padding a Rich `Text` object, added spaces can appear unstyled even
when they conceptually extend styled inline content.

## Desired behavior

Extend trailing inline style spans when right-padding `Text`.

## Constraints

Only trailing inline spans should be extended over added padding. Existing text
content and non-trailing spans should remain unchanged.

## Success criteria

Right-padding styled text extends the final inline style over the inserted
spaces.
