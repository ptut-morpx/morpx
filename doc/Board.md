# Board
```python
from engine import Board
```
***Do not use this unless you know what you're doing!***

## `Board()`
Creates a new `Board` instance.

`Board` objects hold the state of the game board and exposes methods to read and alter it.

## `board.reset()`
Resets the `Board` instance so that it may be reused.

## `board.get(x1, y1, x2, y2)`
Reads the state of the cell at the coordinates `(x1, y1, x2, y2)`.

## `board.getB(x, y)`
Reads the state of the big grid at the coordinates `(x, y)`.

## `board.set(x1, y1, x2, y2, player)`
Sets the state of the cell at the coordinates `(x1, y1, x2, y2)` and updates state accordingly.
Returns `True` if the big grid's state has changed, `False` otherwise.
