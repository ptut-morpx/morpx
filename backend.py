# syntax: python3 backend.py <player> <depth> <c0> <c1> <c2> <c3>

from engine import Game, Player
import minmaxwrapper
import sys

# read CLI arguments
player=sys.argv[1]=='P1' and Player.P1 or Player.P2
depth=int(sys.argv[2])
weights=[float(sys.argv[i+3]) for i in range(4)]

# print XYXY coordinates of played move
def cellListener(game, x1, y1, x2, y2, state):
	if state==player:
		print("{}{}{}{}".format(x1, y1, x2, y2))

# install a game and start it
game=Game()
minmaxwrapper.install(game, player, depth, weights)
game.addTrigger('cell', cellListener)
game.reset()

# listen for actions on stdin
while True:
	xyxy=input()
	if xyxy=='end':
		break
	game.play(game.player, int(xyxy[0]), int(xyxy[1]), int(xyxy[2]), int(xyxy[3]))
