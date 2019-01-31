from engine import EventLoop

loop=EventLoop()

it=loop.addInterval(print, 1000, 'every 1s')
loop.addTimeout(print, 2000, 'in 2s')
loop.add(print, 'now')
loop.addImmediate(print, 'immediately')

def remIt():
	print('in 10s')
	loop.clearInterval(it)
	loop.add(print, 'after 10s')
loop.addTimeout(remIt, 10000)

loop.run()
