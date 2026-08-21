Allow `Command.addArgument()` to accept a prepared required `Argument` with a
default value by treating that argument as optional instead of throwing during
registration.

The default should still be used as the fallback value when the argument is not
provided on the command line.
