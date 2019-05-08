from enum import Enum
from datetime import datetime
from time import sleep

class State(Enum):
	FULL=-1
	NONE=0
	P1=1
	P2=2

class Player:
	P1=State.P1
	P2=State.P2

class EventLoop:
	tickEventMax=10
	tickDelayMax=1000
	tickDelayMin=10
	
	def __init__(self):
		self.events=[]
		self.timeouts=[]
		self.intervals=[]
		self.tick=0
	
	def add(self, fn, *args):
		self.events.insert(0, (fn, args))
	def addImmediate(self, fn, *args):
		self.events.append((fn, args))
	
	def addTimeout(self, fn, timeout, *args):
		tpl=(datetime.now().timestamp()*1000+timeout, fn, args)
		self.timeouts.append(tpl)
		return tpl
	def addInterval(self, fn, interval, *args):
		tpl=[datetime.now().timestamp()*1000+interval, interval, fn, args]
		self.intervals.append(tpl)
		return tpl
	
	def clearTimeout(self, tpl):
		if tpl in self.timeouts: self.timeouts.remove(tpl)
	def clearInterval(self, tpl):
		if tpl in self.intervals: self.intervals.remove(tpl)
	
	def isAlive(self):
		return len(self.events) or len(self.timeouts) or len(self.intervals)
	
	def runTick(self):
		now=datetime.now().timestamp()*1000
		self.tick+=1
		
		rem=[]
		for to in self.timeouts:
			if to[0]<now:
				to[1](*to[2])
				rem.append(to)
		for to in rem:
			self.timeouts.remove(to)
		
		for it in self.intervals:
			if it[0]<now:
				it[2](*it[3])
				it[0]+=it[1]
		
		n=self.__class__.tickEventMax
		while n and len(self.events):
			evt=self.events.pop()
			evt[0](*evt[1])
	
	def run(self):
		while self.isAlive():
			self.runTick()
			if len(self.events)==0 and self.isAlive():
				now=datetime.now().timestamp()*1000
				shortest=now+self.__class__.tickDelayMax
				for to in self.timeouts:
					if to[0]<shortest: shortest=to[0]
				for it in self.intervals:
					if it[0]<shortest: shortest=it[0]
				if shortest-now>self.__class__.tickDelayMin: sleep((shortest-now)/1000)

class Board:
	def __init__(self, copy=None):
		if copy:
			self.cells=copy.cells.copy()
			self.grid=copy.grid.copy()
			self.state=copy.state
		else:
			self.cells=list(range(81))
			self.grid=[State.NONE, State.NONE, State.NONE, State.NONE, State.NONE, State.NONE, State.NONE, State.NONE, State.NONE]
			self.state=State.NONE
			for i in range(81):
				self.cells[i]=State.NONE
	
	def reset(self):
		"""
		board full reset
		"""
		for i in range(9):
			self.grid[i]=State.NONE
		for i in range(81):
			self.cells[i]=State.NONE
		self.state=State.NONE
	
	@staticmethod
	def __getxy(x1, y1, x2, y2):
		"""
		return the array index for (x1, y1, x2, y2) coordinates
		"""
		return x1*27+y1*9+x2*3+y2
	@staticmethod
	def __getxyB(x, y):
		"""
		return the array index for (x, y) coordinates
		"""
		return x*3+y
	
	def get(self, x1, y1, x2, y2):
		"""
		cell value getter
		"""
		return self.cells[Board.__getxy(x1, y1, x2, y2)]
	
	def getB(self, x, y):
		"""
		grid value getter
		"""
		return self.grid[Board.__getxyB(x, y)]
	
	def set(self, x1, y1, x2, y2, player):
		"""
		cell value setter
		also automatically updates grid
		returns True if state has changed
		"""
		self.cells[Board.__getxy(x1, y1, x2, y2)]=player
		
		# detect sub-wins
		subWin=False
		if self.get(x1, y1, 0, y2)==self.get(x1, y1, 1, y2) and self.get(x1, y1, 1, y2)==self.get(x1, y1, 2, y2):
			# rows
			self.grid[Board.__getxyB(x1, y1)]=player
			subWin=True
		elif self.get(x1, y1, x2, 0)==self.get(x1, y1, x2, 1) and self.get(x1, y1, x2, 1)==self.get(x1, y1, x2, 2):
			# cols
			self.grid[Board.__getxyB(x1, y1)]=player
			subWin=True
		elif x2==y2 and self.get(x1, y1, 0, 0)==self.get(x1, y1, 1, 1) and self.get(x1, y1, 1, 1)==self.get(x1, y1, 2, 2):
			# main diagonal
			self.grid[Board.__getxyB(x1, y1)]=player
			subWin=True
		elif x2==2-y2 and self.get(x1, y1, 0, 2)==self.get(x1, y1, 1, 1) and self.get(x1, y1, 1, 1)==self.get(x1, y1, 2, 0):
			# secondary diagonal
			self.grid[Board.__getxyB(x1, y1)]=player
			subWin=True
		
		# detect full grid
		full=True
		for i in range(3):
			for j in range(3):
				if self.get(x1, y1, i, j)==State.NONE:
					full=False
		if full and not subWin:
			self.grid[Board.__getxyB(x1, y1)]=State.FULL
		
		# detect wins
		if subWin:
			if self.getB(x1, 0)==self.getB(x1, 1) and self.getB(x1, 1)==self.getB(x1, 2):
				# rows
				self.state=player
			elif self.getB(0, y1)==self.getB(1, y1) and self.getB(1, y1)==self.getB(2, y1):
				# cols
				self.state=player
			elif x1==y1 and self.getB(0, 0)==self.getB(1, 1) and self.getB(1, 1)==self.getB(2, 2):
				# main diagonal
				self.state=player
			elif x1==2-y1 and self.getB(0, 2)==self.getB(1, 1) and self.getB(1, 1)==self.getB(2, 0):
				# secondary diagonal
				self.state=player
		
		# detect full board
		if full:
			fullBoard=True
			for i in range(9):
				if self.grid[i]==State.NONE:
					fullBoard=False
			if fullBoard and self.state==State.NONE:
				self.state=State.FULL
		
		# return True if the state of the board changed
		return subWin or full

class Game:
	def __init__(self, copy=None):
		if copy:
			self.board=Board(copy.board)
			self.turn=copy.turn
			self.player=copy.player
			self.last=copy.last
			self.triggers={}
		else:
			self.board=Board()
			self.turn=0
			self.player=Player.P1
			self.last=None
			self.triggers={}
	
	def getPlayer(self):
		return self.player==Player.P1 and 1 or -1
	
	def getStatus(self):
		if self.board.state==Player.P1:
			return 1
		elif self.board.state==Player.P2:
			return -1
		else:
			return -1
	
	def reset(self):
		self.board.reset()
		self.turn=0
		self.player=Player.P1
		self.last=None
		
		self.__trigger('reset')
		self.__trigger('turn', self.player)
	
	def __trigger(self, name, *args):
		if name in self.triggers:
			for fn in self.triggers[name]:
				fn(self, *args)
	
	def addTrigger(self, name, fn):
		if name not in self.triggers:
			self.triggers[name]=[]
		self.triggers[name].append(fn)
	
	def nextGrid(self):
		# you can play anywhere if you're either the first to play or the target grid is full or won
		if (not self.last) or self.board.getB(self.last[0], self.last[1])!=State.NONE:
			return None
		return self.last
	
	def getCell(self, x1, y1, x2, y2):
		return self.board.get(x1, y1, x2, y2)
	
	def canPlay(self, player, x1, y1, x2, y2):
		if self.player!=player:
			return False
		if self.board.get(x1, y1, x2, y2)!=State.NONE:
			return False
		if self.board.getB(x1, y1)!=State.NONE:
			return False
		next=self.nextGrid()
		if next and (x1!=next[0] or y1!=next[1]):
			return False
		return True
	
	def play(self, player, x1, y1, x2, y2):
		# sanity checks
		if self.player!=player:
			raise ValueError('Attempt to play when it\'s not your turn')
		if self.board.get(x1, y1, x2, y2)!=State.NONE:
			raise ValueError('Attempt to play in an already used cell')
		if self.board.getB(x1, y1)!=State.NONE:
			raise ValueError('Attempt to play in an unreachable grid')
		next=self.nextGrid()
		if next and (x1!=next[0] or y1!=next[1]):
			raise ValueError('Attempt to play outside the allowed cell')
		
		changed=self.board.set(x1, y1, x2, y2, player)
		self.turn+=1
		self.player=(player==Player.P1) and Player.P2 or Player.P1
		self.last=(x2, y2)
		
		self.__trigger('cell', x1, y1, x2, y2, player)
		
		if changed:
			self.__trigger('changed', x1, y1, self.board.getB(x1, y1))
			if self.board.state!=State.NONE:
				self.__trigger('end', self.board.state)
		
		self.__trigger('turn', self.player)
	
	def getMoves(self):
		if self.board.state!=State.NONE:
			return []
		moves=[]
		n=[0, 1, 2]
		for x1 in n:
			for y1 in n:
				for x2 in n:
					for y2 in n:
						if self.canPlay(self.player, x1, y1, x2, y2):
							moves.append((self.player, x1, y1, x2, y2))
		return moves
	
	def playClone(self, player, x1, y1, x2, y2):
		copy=Game(self)
		copy.play(player, x1, y1, x2, y2)
		return copy
	
	def getScore(self, coef):
		# convert player to usable value
		def playerToVal(player):
			if self.player==Player.P1:
				return player==Player.P1 and 1 or -1
			else:
				return player==Player.P2 and 1 or -1
		
		# count P1's and P2's in a line
		def count(a, b, c):
			(x, y)=(0, 0)
			if a==Player.P1:
				x+=1
			elif b==Player.P2:
				y+=1
			if b==Player.P1:
				x+=1
			elif b==Player.P2:
				y+=1
			if c==Player.P1:
				x+=1
			elif c==Player.P2:
				y+=1
			return (x, y)
		
		# count open 2-lines
		def count2Lines():
			def getPoints(a, b, c):
				(x, y)=count(a, b, c)
				if x==2 and y==0:
					return self.player==Player.P1 and 1 or -1
				elif y==2 and x==0:
					return self.player==Player.P1 and -1 or 1
				else:
					return 0
			
			for x1 in range(3):
				for y1 in range(3):
					total=0
					for a in range(3):
						total+=getPoints(self.board.get(x1, y1, a, 0), self.board.get(x1, y1, a, 1), self.board.get(x1, y1, a, 2))
						total+=getPoints(self.board.get(x1, y1, 0, a), self.board.get(x1, y1, 1, a), self.board.get(x1, y1, 2, a))
					total+=getPoints(self.board.get(x1, y1, 0, 0), self.board.get(x1, y1, 1, 1), self.board.get(x1, y1, 2, 2))
					total+=getPoints(self.board.get(x1, y1, 0, 2), self.board.get(x1, y1, 1, 1), self.board.get(x1, y1, 2, 0))
			return total
		
		# count big cells
		def countBigCells():
			total=0
			for x in range(3):
				for y in range(3):
					total+=playerToVal(self.board.getB(x, y))
			return total
		
		# count open 2-lines of big cells
		def count2LinesB():
			def getPoints(a, b, c):
				(x, y)=count(a, b, c)
				if x==2 and y==0:
					return self.player==Player.P1 and 1 or -1
				elif y==2 and x==0:
					return self.player==Player.P1 and -1 or 1
				else:
					return 0
			
			total=0
			for a in range(3):
				total+=getPoints(self.board.getB(a, 0), self.board.getB(a, 1), self.board.getB(a, 2))
				total+=getPoints(self.board.getB(0, a), self.board.getB(1, a), self.board.getB(2, a))
			total+=getPoints(self.board.getB(0, 0), self.board.getB(1, 1), self.board.getB(2, 2))
			total+=getPoints(self.board.getB(0, 2), self.board.getB(1, 1), self.board.getB(2, 0))
			return total
		
		# count controlled cells
		def countControlledCells():
			total=0
			for x1 in range(3):
				for y1 in range(3):
					if self.board.getB(x1, y1)==State.NONE:
						for x2 in range(3):
							for y2 in range(3):
								total+=playerToVal(self.board.get(x1, y1, x2, y2))
			return total
		
		# return immediately if game has ended
		if self.board.state!=State.NONE:
			return playerToVal(self.board.state)*1000000
		
		score=0
		score+=coef[0]*count2Lines()
		score+=coef[1]*count2LinesB()
		score+=coef[2]*countBigCells()
		score+=coef[3]*countControlledCells()
		return score
