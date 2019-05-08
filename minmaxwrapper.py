from engine import Player, Game, State
from minmax.minmax import Minmax

def install(game, boi, depth=3, weights=[1, 1, 1, 1]):
	finished=False
	
	def onEnd(game, winner):
		finished=True
	
	def onTurn(game, player):
		if player==boi and not finished:
			move=Minmax.getBestMove(game, depth, weights)
			if len(move[0]):
				game.play(*move[0][0])
	
	game.addTrigger('end', onEnd)
	game.addTrigger('turn', onTurn)
