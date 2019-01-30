from engine import Player, Game
import tui

# actual code
game=Game()
tui.install(game)

game.reset()
game.play(Player.P1, 0, 0, 1, 1)
game.play(Player.P2, 1, 1, 2, 2)
game.play(Player.P1, 2, 2, 0, 2)
game.play(Player.P2, 0, 2, 0, 0)
game.play(Player.P1, 0, 0, 0, 1)
game.play(Player.P2, 0, 1, 0, 0)
game.play(Player.P1, 0, 0, 2, 1)
game.play(Player.P2, 2, 1, 0, 0)
game.play(Player.P1, 1, 1, 1, 1)
