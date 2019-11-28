"""
The table class for use in the tetris-like game "yat"

Created 17.08.2012 by Adrian Antonana
Copyright (c) 2012 Adrian Antonana
"""

"""
This file is part of YAT (Yet Another Tetris).

YAT is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

YAT is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with YAT.     If not, see <http://www.gnu.org/licenses/>.
"""
from blocks import *
from colors import *
import pygame as pg

# Table size constants
WIDTH = 12
HEIGHT = 20
BLOCK_SIZE = 30
BLOCK_SIZE_SMALL = BLOCK_SIZE - 5
INNER_BLOCK_OFFSET = (BLOCK_SIZE - BLOCK_SIZE_SMALL) / 2

class table:
    """Table Class definition"""

    """object constructor"""
    def __init__(self, surface):

        self.surface = surface
        self.width = WIDTH
        self.height = HEIGHT
        self.matrix = [[E for y in range(WIDTH)] for x in range(HEIGHT)]
        self.blocksurf = pg.Surface((BLOCK_SIZE, BLOCK_SIZE))
        self.blocksurf.set_alpha(255)
        self.blocksurf.set_clip(
            INNER_BLOCK_OFFSET, INNER_BLOCK_OFFSET, BLOCK_SIZE_SMALL, BLOCK_SIZE_SMALL
        )

    def show(self):
        """show the table contents on its surface"""
        m = self.matrix
        bs = self.blocksurf
        self.surface.fill(BLACK)

        for x in range(self.height):
            for y in range(self.width):
                if m[x][y] == I:
                    bs.fill(RED)
                elif m[x][y] == T:
                    bs.fill(MAGENTA)
                elif m[x][y] == O:
                    bs.fill(GREEN)
                elif m[x][y] == S:
                    bs.fill(YELLOW)
                elif m[x][y] == Z:
                    bs.fill(BLUE)
                elif m[x][y] == L:
                    bs.fill(CYAN)
                elif m[x][y] == J:
                    bs.fill(ORANGE)
                if m[x][y] != E:
                    self.surface.blit(bs, (y * BLOCK_SIZE, x * BLOCK_SIZE))

        pg.display.flip()

    def getHeight(self):
        """get the table height"""
        return self.height

    def getWidth(self):
        """get the table width"""
        return self.width

    def getOcupPosList(self, actblockposlist=None):
        """get a list with the table ocpied positions"""
        h = self.height
        w = self.width
        if actblockposlist == None:
            return [
                (x, y) for x in range(h) for y in range(w) if self.matrix[x][y] != E
            ]
        else:
            return [
                (x, y)
                for x in range(h)
                for y in range(w)
                if self.matrix[x][y] != E and (x, y) not in actblockposlist
            ]

    def adBlock(self, block, blocktype):
        """add a block to the table matrix"""
        for position in block:
            self.matrix[position[0]][position[1]] = blocktype

    def delFullLines(self):
        """remove completed lines"""
        height = self.getHeight()
        width = self.getWidth()
        removedlines = 0
        for row in range(height):
            col = 0
            fullline = False
            while self.matrix[row][col] != E and not fullline:
                col += 1
                if col == width:
                    fullline = True

                    for col in range(width):
                        self.matrix[row][col] = E
                    for upperrow in reversed(range(row)):
                        self.matrix[upperrow + 1] = self.matrix[upperrow]

                    self.matrix[0] = [E for cell in range(width)]
                    removedlines += 1

        return removedlines

    def gameOver(self, bpl):
        """check if the game is over"""
        return set(bpl).intersection(set(self.getOcupPosList())) != set([])

    def __str__(self):
        """print the table content on the terminal"""
        string = ""
        for x in range(self.height):
            for y in range(self.width):
                block = self.matrix[x][y]
                if block == E:
                    string += "."
                elif block == I:
                    string += "I"
                elif block == T:
                    string += "T"
                elif block == O:
                    string += "O"
                elif block == S:
                    string += "S"
                elif block == Z:
                    string += "Z"
                elif block == L:
                    string += "L"
                elif block == J:
                    string += "J"

            string += "\n"

        return string

    def setSurfAlpha(self, alpha):
        self.surface.set_alpha(alpha)
        self.blocksurf.set_alpha(alpha)
