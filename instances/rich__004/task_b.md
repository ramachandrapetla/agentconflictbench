Refactor the no-separator branch of `Text.split()` through `divide([])`.

`split()` currently handles the no-separator case by returning `self.copy()`.
Delegate that edge case through `divide([])` so split and divide share the same
segmentation path.
