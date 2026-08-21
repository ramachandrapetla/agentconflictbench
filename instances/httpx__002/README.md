# httpx__002: loopback HTTPS upgrade vs. loopback host aliasing

This is the second HTTPX AgentConflictBench instance and the first
`security_policy` seed.

## Repository

- Upstream: https://github.com/encode/httpx
- Base commit: `b5addb64f0161ff6bfe94c124ef76f6a1fba5254`
- Language: Python
- Conflict type: security_policy
- Source: researcher_constructed

## Task A

Preserve `Authorization` headers for loopback HTTP-to-HTTPS redirects.

Example: `http://localhost:8000` redirecting to `https://localhost:8000`
keeps authorization because the redirect remains on the same loopback host and
upgrades transport security.

Patch A passes its validation oracle.

## Task B

Treat `localhost` and `127.0.0.1` as same-origin aliases when scheme and port
match.

Example: `http://localhost:8000` redirecting to `http://127.0.0.1:8000`
keeps authorization because both names refer to loopback on the same scheme and
port.

Patch B passes its validation oracle.

## Composition Failure

When Patch A and Patch B are composed, the client preserves `Authorization` for
`http://localhost:8000` redirecting to `https://127.0.0.1:8000`.

The composition oracle treats the combination of scheme change and host alias
change as too permissive for credential forwarding. It expects the redirect
header builder to strip `Authorization`, but the composed implementation keeps
it.

## Why This Is An AgentConflictBench Instance

- Patch A is valid in isolation.
- Patch B is valid in isolation.
- Patch A and Patch B apply cleanly to the same base commit.
- The combined behavior fails a composition-level oracle.
- The failure comes from an implicit security boundary around redirect
  credential forwarding.

## Files

- `patch_a.patch`: preserve auth on loopback HTTPS upgrades.
- `patch_b.patch`: treat loopback host aliases as same-origin.
- `oracle/test_patch_a.py`: Patch A validation oracle.
- `oracle/test_patch_b.py`: Patch B validation oracle.
- `oracle/test_composition.py`: composition failure oracle.
- `logs/`: validation outputs captured during seed creation.
