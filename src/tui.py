from engine import Player, Game, State
from ansi import cursor, screen, color, write, flush

#BEGIN drawing functions

def drawGrid(x, y):
	for i in range(3):
		cursor.set(x*7+2, y*6+2*i+1)
		write('|')
		cursor.set(x*7+4)
		write('|')
	for i in range(2):
		cursor.set(x*7+1, y*6+2*i+2)
		write('-+-+-')

def drawBoard():
	screen.clear()
	color.bg('black')
	color.fg('white')
	for i in range(17):
		write('                   \n')
	for i in range(3):
		for j in range(3):
			drawGrid(i, j)
	color.fg('magenta')
	for i in range(2):
		cursor.set(1, 6*i+6)
		write('=====##=====##=====')
	for i in range(3):
		for j in range(5):
			cursor.set(6, j+6*i+1)
			write('||')
			cursor.set(13)
			write('||')
	color.reset()
	write('\n')
	flush()

#END drawing functions

def onReset(game):
	drawBoard()

last=None
def onTurn(game, player):
	global last
	color.bg('black')
	if last:
		color.fg('white')
		drawGrid(last[0], last[1])
	last=game.nextGrid()
	if last:
		color.fg('green')
		drawGrid(last[0], last[1])
	cursor.set(21, 1)
	color.reset()
	if player==Player.P1:
		color.fg('blue')
	else:
		color.fg('yellow')
	write(player.name+"'s turn")
	cursor.set(1, 18)
	flush()

def onCell(game, x1, y1, x2, y2, state):
	cursor.save()
	cursor.set(x2*2+x1*7+1, y2*2+y1*6+1)
	color.bg('black')
	if state==Player.P1:
		color.fg('blue')
		write('X')
	else:
		color.fg('yellow')
		write('O')
	color.reset()
	cursor.restore()
	flush()

def onChanged(game, x, y, state):
	cursor.save()
	if state==Player.P1:
		color.bg('blue')
	elif state==Player.P2:
		color.bg('yellow')
	else:
		color.bg('white')
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

def onEnd(game, player):
	print(player.name, 'wins')

def install(game):
	game.addTrigger('reset', onReset)
	game.addTrigger('turn', onTurn)
	game.addTrigger('cell', onCell)
	game.addTrigger('changed', onChanged)
	game.addTrigger('end', onEnd)
