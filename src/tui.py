from engine import Player, Game
from ansi import cursor, screen, color, write, flush

# drawing functions
def drawBoard(game):
	def a():
		color.fg('white')
		write(" | | ")
		color.fg('magenta')
		write("||")
		color.fg('white')
		write(" | | ")
		color.fg('magenta')
		write("||")
		color.fg('white')
		write(" | | \n")
	def b():
		color.fg('white')
		write("-+-+-")
		color.fg('magenta')
		write("||")
		color.fg('white')
		write("-+-+-")
		color.fg('magenta')
		write("||")
		color.fg('white')
		write("-+-+-\n")
	def c():
		color.fg('magenta')
		write("=====##=====##=====\n")
	
	screen.clear();
	color.bg('black')
	a()
	b()
	a()
	b()
	a()
	c()
	a()
	b()
	a()
	b()
	a()
	c()
	a()
	b()
	a()
	b()
	a()
	color.reset()
	flush()

def drawCell(game, player, x1, y1, x2, y2):
	cursor.save()
	cursor.set(x2*2+x1*7+1, y2*2+y1*6+1)
	color.bg('black')
	if player==Player.P1:
		color.fg('blue')
		write('X')
	else:
		color.fg('yellow')
		write('O')
	color.reset()
	cursor.restore()
	flush()

def drawSubWin(game, player, x, y):
	print(player.name, 'wins', x, y)
	cursor.save()
	if player==Player.P1:
		color.bg('blue')
	else:
		color.bg('yellow')
	for i in range(3):
		for j in range(3):
			cursor.set(i*2+x*7+1, j*2+y*6+1)
			color.fg('black')
			p=game.getCell(x, y, i, j)
			if p==Player.P1:
				write('X')
			elif p==Player.P2:
				write('O')
			else:
				write(' ')
	color.reset()
	cursor.restore()
	flush()

def drawWin(game, player):
	print(player.name, 'wins')

def install(game):
	game.addResetTrigger(drawBoard)
	game.addCellTrigger(drawCell)
	game.addSubWinnerTrigger(drawSubWin)
	game.addWinnerTrigger(drawWin)
