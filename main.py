""" Author: Jake White
    Started 10/22/15
    PyCaster is a raycasting engine designed to
    display 2D maps in a pseudo-3D fashion.
"""
import sys
import pygame
from game import *


def main():
    game = Game()
    game.start()
    print("Started.")



if __name__ == "__main__":
  main()