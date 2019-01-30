from enum import Enum
from datetime import datetime
from time import sleep

class Player(Enum):
	NONE=0
	P1=1
	P2=2

def getWinner(grid):
	if grid[0][0]==grid[1][1] and grid[1][1]==grid[2][2] and grid[1][1]!=Player.NONE:
		return grid[1][1]
	if grid[2][0]==grid[1][1] and grid[1][1]==grid[0][2] and grid[1][1]!=Player.NONE:
		return grid[1][1]
	for i in range(3):
		if grid[i][0]==grid[i][1] and grid[i][1]==grid[i][2] and grid[i][1]!=Player.NONE:
			return grid[i][1]
		if grid[0][i]==grid[1][i] and grid[1][i]==grid[2][i] and grid[1][i]!=Player.NONE:
			return grid[1][i]
	return Player.NONE

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
	def __init__(self):
		self.grids=[]
		for i in range(3):
			self.grids.append([])
			for j in range(3):
				self.grids[i].append([])
				for k in range(3):
					self.grids[i][j].append([Player.NONE, Player.NONE, Player.NONE])
	
	def get(self, x1, y1, x2, y2):
		return self.grids[x1][y1][x2][y2]
	def set(self, x1, y1, x2, y2, val):
		self.grids[x1][y1][x2][y2]=val
	
	def reset(self):
		for i in range(3):
			for j in range(3):
				for k in range(3):
					for l in range(3):
						self.grids[i][j][k][l]=Player.NONE
	
	def isFull(self, x, y):
		for row in self.grids[x][y]:
			for cell in row:
				if cell==Player.NONE:
					return False
		return True
	
	def subWinner(self, x, y):
		return getWinner(self.grids[x][y])
	def winner(self):
		grid=[]
		for i in range(3):
			grid.append([0,0,0])
			for j in range(3):
				grid[i][j]=self.subWinner(i, j)
		return getWinner(grid)


class Game:
	def __init__(self):
		self.board=Board()
		self.turn=0
		self.player=Player.P1
		self.last=None
		
		self.cellTriggers=[]
		self.subWinnerTriggers=[]
		self.winnerTriggers=[]
		self.resetTriggers=[]
	
	def reset(self):
		self.board.reset()
		self.turn=0
		self.player=Player.P1
		self.last=None
		
		for trigger in self.resetTriggers:
			trigger(self)
	
	def addCellTrigger(self, trigger):
		if not trigger in self.cellTriggers:
			self.cellTriggers.append(trigger)
	def addSubWinnerTrigger(self, trigger):
		if not trigger in self.subWinnerTriggers:
			self.subWinnerTriggers.append(trigger)
	def addWinnerTrigger(self, trigger):
		if not trigger in self.winnerTriggers:
			self.winnerTriggers.append(trigger)
	def addResetTrigger(self, trigger):
		if not trigger in self.resetTriggers:
			self.resetTriggers.append(trigger)
	
	def getCell(self, x1, y1, x2, y2):
		return self.board.get(x1, y1, x2, y2)
	
	def play(self, player, x1, y1, x2, y2):
		if self.player!=player:
			raise ValueError('Attempt to play when it\'s not your turn')
		if self.board.get(x1, y1, x2, y2)!=Player.NONE:
			raise ValueError('Attempt to play in an already used cell')
		if self.last and (self.board.subWinner(self.last[0], self.last[1])!=Player.NONE or self.board.isFull(self.last[0], self.last[1])) and (x1!=self.last[0] or y1!=self.last[1]):
			raise ValueError('Attempt to play somewhere not allowed')
		self.board.set(x1, y1, x2, y2, player)
		self.turn+=1
		self.player=(player==Player.P1) and Player.P2 or Player.P1
		
		for trigger in self.cellTriggers:
			trigger(self, player, x1, y1, x2, y2)
		
		sw=self.board.subWinner(x1, y1)
		if sw!=Player.NONE:
			for trigger in self.subWinnerTriggers:
				trigger(self, sw, x1, y1)
				
			w=self.board.winner()
			if w!=Player.NONE:
				for trigger in self.winnerTriggers:
					trigger(self, w)
