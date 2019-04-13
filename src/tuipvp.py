from engine import Game, Player
from ansi import cursor, screen
import tui

game = Game()
tui.install(game)
game.reset()


while True:
	cursor.set(1, 18)
	cursor.save()
	for i in range(5):
		screen.clearLine()
		cursor.down(1)
	cursor.restore()
	print("at {} to play".format(game.player.name))
	x1 = int(input("x1= "))-1
	y1 = int(input("y1= "))-1 # will be optimised later once the engine is finished
	x2 = int(input("x2= "))-1 # atm we'll always enter x1 and y1 even if not needed
	y2 = int(input("y2= "))-1

	game.play(game.player, x1, y1, x2, y2)
