# `Game`
```python
from engine import Game
```

## Events
### `reset`
```python
def onReset(game)
```
Triggered when the game is reset.

### `turn`
```python
def onTurn(game, player)
```
Triggered when the next player should play.

### `cell`
```python
def onCell(game, x1, y1, x2, y2, state)
```
Triggered when a cell changes state.

### `changed`
```python
def onChanged(game, x, y, state)
```
Triggered when the big grid changes state.

### `end`
```python
def onEnd(game, state)
```
Triggered when the game ends.

## `Game()`
Creates a new `Game` instance.

`Game` objects hold the full state of a game, and need to be reset between games.
`Game` objects should be manipulated using its methods and events.

## `game.reset()`
Resets this `Game` instance so that it may be reused.

Also activates all `reset` and `turn` triggers attached to it.

## `game.addTrigger(name, fn)`
Adds `fn` to the list of triggers for the event `name`.

## `game.nextGrid()`
Returns a tuple containing the `(x, y)` coordinate pairs of the grid the next player should play, or `None` if they can play wherever they want.

## `game.getCell(x1, y1, x2, y2)`
Returns the state of the cell at the coordinates `(x1, y1, x2, y2)`.

## `game.play(player, x1, y1, x2, y2)`
Makes `player` play at the coordinates `(x1, y1, x2, y2)`.
Handles invalid moves by raising a `ValueError`.
Automatically updates state and activates `cell`, `changed`, `end` and `turn` triggers as needed.
