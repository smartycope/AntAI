from Game import Game
import argparse

description = ''
parser = argparse.ArgumentParser(description=description)
parser.add_argument('-v' , '--verbose' , action='store_true')
args = parser.parse_args()

game = Game(args=args, title='Ant AI')
game.run()
game.currentScene.exit()



# TODO Next:
#* finish getting check boxes working with my options class
#* get dropdown menus and option menus and maybe radio buttons working with my options class
# add all the static variables in Ant as options 
# somehow add distance checking for all the ants to motivate them to go towards the nearest food
# find out what's slowing it down so much and optimize it

# add the options menu to it's own thread and pause the simulation so it doesn't have the background thing
# fix the debouncer so instead of a delay it just inhibits escape/o from being pressed
# figure out padding to make the options menu look all pretty
