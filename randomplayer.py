from engine import Game, Player
from random import choice

def install(game, boi):
	finished=False
	
	def onEnd(game, winner):
		finished=True
	
	def onTurn(game, player):
		if player==boi and not finished:
			game.play(*choice(game.getMoves()))
	
	game.addTrigger('end', onEnd)
	game.addTrigger('turn', onTurn)
