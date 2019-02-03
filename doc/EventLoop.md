# `EventLoop`
```python
from engine import EventLoop
```

## `EventLoop()`
Creates an `EventLoop` instance.

## `loop.add(fn, *args)`
Adds a callback to be called later on.

## `loop.addImmediate(fn, *args)`
Adds a callback to be called as soon as possible.

## `loop.addTimeout(fn, timeout, *args)`
Adds a callback to be called in approximately `timeout` milliseconds.
Returns an object that can be used to clear the timeout.

## `loop.addInterval(fn, interval, *args)`
Adds a callback to be called approximately every `interval` milliseconds.
Returns an object that can be used to clear the interval.

## `loop.clearTimeout(obj)`
Clears the timeout associated with the object `obj` so that it doesn't trigger.

## `loop.clearInterval(obj)`
Clears the interval associated with the object `obj` so that it doesn't trigger.

## `loop.isAlive()`
Returns `True` if the loop is still alive, `False` otherwise.

A loop is said to be alive if it still has callbacks, timeouts or intervals.

## `loop.runTick()`
Runs a single iteration of the event loop.

## `loop.run()`
Runs the event loop until it becomes dead (that is, not alive).
