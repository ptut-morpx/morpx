from engine import Game, Player
from ansi import cursor, screen
import tui

game = Game()
tui.install(game)
tui.installPlayer(game, Player.P1)
tui.installPlayer(game, Player.P2)
game.reset()
