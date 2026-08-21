# commander_control__001

Clean-composition control for `tj/commander.js` at
`ba6d13ddb4243e5913367734f8c159089ffe7834`.

Patch A adds `Argument.isRequired()`. Patch B adds `Option.isNegated()`. The
changes touch separate classes and expose independent introspection behavior, so
the composed patch is expected to pass.

Expected composition outcome: `pass`.
