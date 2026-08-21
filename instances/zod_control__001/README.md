# zod_control__001

Clean-composition control for `colinhacks/zod` at
`e516c3baf22615e20934116abebfed6c000222c2`.

Patch A adds string-schema email format introspection. Patch B adds number-schema
integer format introspection. The changes are independent helper methods, so the
composed patch is expected to pass.

Expected composition outcome: `pass`.
