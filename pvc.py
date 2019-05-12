from engine import Game, Player
from ansi import cursor, screen
import tui
import minmaxwrapper

depth=int(input("Minmax depth: "))
weights=[0, 0, 0, 0]
for i in range(4):
	weights[i]=int(input("Weight #{}: ".format(i)))

game=Game()
tui.install(game)
tui.installPlayer(game, Player.P1)
minmaxwrapper.install(game, Player.P2, depth, weights)
game.reset()
