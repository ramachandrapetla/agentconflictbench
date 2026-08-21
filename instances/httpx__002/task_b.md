# Task B: Treat localhost aliases as same-origin

## Problem

Loopback services may use `localhost` and `127.0.0.1` interchangeably, but
origin checks can treat them as unrelated hosts.

## Desired behavior

Treat `localhost` and `127.0.0.1` as same-origin aliases when scheme and port
match.

## Constraints

The alias should only apply to loopback names and addresses. Scheme and port
must still be considered.

## Success criteria

`http://localhost:8000` and `http://127.0.0.1:8000` are considered same-origin,
while different schemes or ports are not.
