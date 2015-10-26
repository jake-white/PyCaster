""" Author: Jake White
    Started 10/22/15
    PyCaster is a raycasting engine designed to
    display 2D maps in a pseudo-3D fashion.
"""

import graphics
from world import *
from render import *


def main():
    configure()

    print("Started.")


def configure():
    global world, player
    world = World(5, 5)
    player = Player(2, 2)
    screen = Screen()


    print("Player placed at {}, {} in a {}x{} world.".format(player.getX(), player.getY(), world.getLength(), world.getWidth()))
    print(world.getCoords())

#running code
main()