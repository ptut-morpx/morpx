from sys import stdout
from enum import Enum

def write(s):
	stdout.write(s)
def flush():
	stdout.flush()

esc=chr(27)+'['

class cursor:
	@staticmethod
	def set(x, y=None):
		if y!=None:
			write(esc+str(int(y))+';'+str(int(x))+'H')
		else:
			write(esc+str(int(x))+'G')
	
	@staticmethod
	def up(n=1):
		write(esc+str(int(n))+'A')
	@staticmethod
	def down(n=1):
		write(esc+str(int(n))+'B')
	@staticmethod
	def left(n=1):
		write(esc+str(int(n))+'D')
	@staticmethod
	def right(n=1):
		write(esc+str(int(n))+'C')
	
	@staticmethod
	def save():
		write(esc+'s')
	@staticmethod
	def restore():
		write(esc+'u')
	
	@staticmethod
	def on():
		write(esc+'?25h')
	def off():
		write(esc+'?25l')

class screen:
	@staticmethod
	def clear(mode=2):
		write(esc+str(mode)+'J')
		if mode==2 or mode==3:
			write(esc+'1;1H')
	@staticmethod
	def clearLine(mode=2):
		write(esc+str(mode)+'K')
		if mode==2:
			write(esc+'1G')

class color(Enum):
	BLACK=0
	RED=1
	GREEN=2
	YELLOW=3
	BLUE=4
	MAGENTA=5
	CYAN=6
	WHITE=7
	
	@classmethod
	def fg(self, name):
		write(esc+'3'+str(self[name.upper()].value)+'m')
	@classmethod
	def bg(self, name):
		write(esc+'4'+str(self[name.upper()].value)+'m')
	
	@staticmethod
	def reset():
		write(esc+'0m')
