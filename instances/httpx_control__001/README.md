# httpx_control__001

Clean-composition control for `encode/httpx` at
`b5addb64f0161ff6bfe94c124ef76f6a1fba5254`.

Patch A adds `Headers.has_multiple()`. Patch B adds `QueryParams.has_key()`.
The changes touch independent model types, so the composed patch is expected to
pass.

Expected composition outcome: `pass`.
