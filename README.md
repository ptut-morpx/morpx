# MorpX
A test implementation of Thomas Montero's game in Python3

# Rules of the game
The core mechanic is the same as for tic-tac-toe: 2 players taking turns to place an X or an O on the grid and trying to align 3 to win the grid.
However there is a twist, here the objective is to win multiple little grids to win the corresponding big cells.
Let x1 and y1 be the coordinates of the big grid and x2 and y2 the coordinates in the corresponding small grids.
Flow of the game:
- the first player plays wherever he wants
- the next player has to play in the big cell with the coordinates (x2, y2) of the previous player
- every turn goes with this patern, the old (x2, y2) becomes te new (x1, y1)
- if you manage to win a small grid you win the corresponding big cell
- if your opponent redirects you in a big cell that is either full or won you get to choose both (x1, y1) and (x2, y2) coordinates you play in
- the player that manages to align 3 big cells wins the game
- if no one is able to align 3 big cells the game ends in a tie
