from engine import Player, Game
import tui
import minmaxwrapper as minmax

# actual code
game=Game()
tui.install(game)
minmax.install(game, Player.P1, 4)
minmax.install(game, Player.P2, 4)
game.reset()
