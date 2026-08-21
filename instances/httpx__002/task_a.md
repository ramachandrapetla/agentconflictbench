# Task A: Preserve credentials for loopback HTTP-to-HTTPS redirects

## Problem

Local development services often redirect from HTTP to HTTPS on loopback hosts,
and dropping credentials can break authenticated local workflows.

## Desired behavior

Preserve `Authorization` headers for redirects that stay on a loopback host
while upgrading from HTTP to HTTPS.

## Constraints

Credential preservation should remain conservative and should not forward
credentials to unrelated external hosts.

## Success criteria

A redirect from `http://localhost` to `https://localhost` preserves the
`Authorization` header.
