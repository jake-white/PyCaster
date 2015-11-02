""" Author: Jake White
    Started 10/22/15
    PyCaster is a raycasting engine designed to
    display 2D maps in a pseudo-3D fashion.
"""
from world import *
from render import *
from gamelogic import *
from raycaster import *


def main():
    configure()
    loop.start()
    print("Started.")


def configure():
    global world, player, screen, loop, caster
    world = World(5, 5)
    player = Player(2, 2)
    caster = RayCaster()
    screen = Screen(caster, "PyCaster", 400, 300)
    loop = GameLoop(screen, caster)
    print("Player placed at {}, {} in a {}x{} world.".format(player.getX(), player.getY(), world.getLength(), world.getWidth()))
    print(world.getCoords())

#running code
main()