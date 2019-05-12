from engine import Player, Game, State
from ansi import cursor, screen, color, write, flush
from sys import stdin
read=stdin.read
import termios
import atexit

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
	cursor.set(21, 2)
	color.reset()
	if player==Player.P1:
		color.fg('blue')
		write("P1 wins!")
	elif player==Player.P2:
		color.fg('yellow')
		write("P2 wins!")
	else:
		write("It's a draw")
	cursor.set(1, 18)
	color.reset()
	flush()

def install(game):
	cursor.off()
	game.addTrigger('reset', onReset)
	game.addTrigger('turn', onTurn)
	game.addTrigger('cell', onCell)
	game.addTrigger('changed', onChanged)
	game.addTrigger('end', onEnd)

def installPlayer(game, boi):
	fd=stdin.fileno()
	
	old=termios.tcgetattr(fd)
	atexit.register(termios.tcsetattr, fd, termios.TCSANOW, old)
	
	new=termios.tcgetattr(fd)
	new[3]&=~(termios.ECHO|termios.ICANON)
	termios.tcsetattr(fd, termios.TCSANOW, new)
	
	finished=False
	
	def readAction():
		while True:
			byte=read(1)
			if byte=='\n':
				return 'ok'
			elif byte=='\x1b':
				if read(1)=='[':
					byte=read(1)
					if byte=='D':
						return 'left'
					elif byte=='C':
						return 'right'
					elif byte=='A':
						return 'up'
					elif byte=='B':
						return 'down'
	
	def onEnd(game, status):
		finished=True
	
	def onPlayerTurn(game, player):
		if player==boi and not finished:
			(x1, y1, x2, y2)=(0, 0, 0, 0)
			cursor.on()
			while True:
				cursor.set(x2*2+x1*7+1, y2*2+y1*6+1)
				flush()
				action=readAction()
				if action=='ok':
					try:
						game.play(boi, x1, y1, x2, y2)
						break
					except ValueError:
						pass
				elif action=='left':
					x2-=1
					if x2<0:
						x2=2
						x1-=1
						if x1<0:
							x1=2
				elif action=='right':
					x2+=1
					if x2>=3:
						x2=0
						x1+=1
						if x1>=3:
							x1=0
				elif action=='up':
					y2-=1
					if y2<0:
						y2=2
						y1-=1
						if y1<0:
							y1=2
				elif action=='down':
					y2+=1
					if y2>=3:
						y2=0
						y1+=1
						if y1>=3:
							y1=0
			cursot.off()
			flush()
	
	game.addTrigger('turn', onPlayerTurn)
	game.addTrigger('end', onEnd)
