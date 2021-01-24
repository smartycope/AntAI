from Game import Game
import argparse

description = ''
parser = argparse.ArgumentParser(description=description)
parser.add_argument('-v' , '--verbose' , action='store_true')
args = parser.parse_args()

# import time
# from Cope import getTime
# with getTime('test', 20):
#     time.sleep(1)

game = Game(args=args, title='Ant AI')
game.run()
game.currentScene.exit()
