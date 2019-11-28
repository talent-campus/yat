"""
The block class for use in the tetris-like game.

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

Copyright (c) 17.08.2012 by Adrian Antonana
"""
import random as rnd
import pygame as pg
import colors as clr

# Block Type Constants
E = 0
I = 1
T = 2
S = 3
Z = 4
O = 5
L = 6
J = 7


class block:
    """Block class definition"""

    def __init__(self, (x, y), blocktype=None):
        """Object constructor"""

        # if no type is given as a parameter, the block is randomly
        # generated
        if blocktype is None:
            self.blocktype = rnd.randint(I, J)
        else:
            self.blocktype = blocktype

        # set the block position
        self.posx = x
        self.posy = y

        # set blocktype, color and the shape of the block
        if self.blocktype == I:
            self.positions = [[True], [True], [True], [True]]
            self.color = clr.RED
        elif self.blocktype == T:
            self.positions = [[True, True, True], [False, True, False]]
            self.color = clr.MAGENTA
        elif self.blocktype == S:
            self.positions = [[False, True, True], [True, True, False]]
            self.color = clr.YELLOW
        elif self.blocktype == Z:
            self.positions = [[True, True, False], [False, True, True]]
            self.color = clr.BLUE
        elif self.blocktype == O:
            self.positions = [[True, True], [True, True]]
            self.color = clr.GREEN
        elif self.blocktype == L:
            self.positions = [[True, False], [True, False], [True, True]]
            self.color = clr.CYAN
        elif self.blocktype == J:
            self.positions = [[False, True], [False, True], [True, True]]
            self.color = clr.ORANGE

    def getType(self):
        """get the block type"""
        return self.blocktype

    def rotRight(self, maxx, maxy, opl):
        """rotate a block clockwise"""
        l = self.positions
        x = self.posx
        y = self.posy
        btype = self.blocktype

        if len(self.positions) < len(self.positions[0]):
            x -= 1
            if btype == I:
                y += 1
        elif len(self.positions) > len(self.positions[0]):
            x += 1
            if btype == I and y >= 1:
                y -= 1

        newpos = [
            [l[row][col] for row in reversed(range(len(l)))] for col in range(len(l[0]))
        ]

        exceedx = False
        exceedy = False

        if len(newpos) + x > maxx or x < 0:
            exceedx = True

        if len(newpos[0]) + y > maxy:
            exceedy = True
            deltay = len(newpos[0]) + y - maxy

        if not exceedx:
            if exceedy:
                y -= deltay
            newposlist = [
                (row + x, col + y)
                for row in range(len(newpos))
                for col in range(len(newpos[0]))
                if newpos[row][col] is True
            ]
            if set(newposlist).intersection(set(opl)) == set([]):
                self.positions = newpos
                self.posx = x
                self.posy = y
                return True

        return False

    def rotLeft(self, maxx, maxy, opl):
        """rotate a block counterclockwise"""
        l = self.positions
        x = self.posx
        y = self.posy
        btype = self.blocktype

        if len(self.positions) < len(self.positions[0]):
            x -= 1
            if btype == I:
                y += 1
        elif len(self.positions) > len(self.positions[0]):
            x += 1
            if btype == I and y >= 1:
                y -= 1

        newpos = [
            [l[row][col] for row in range(len(l))] for col in reversed(range(len(l[0])))
        ]

        exceedx = False
        exceedy = False

        if len(newpos) + x > maxx or x < 0:
            exceedx = True

        if len(newpos[0]) + y > maxy:
            exceedy = True
            deltay = len(newpos[0]) + y - maxy

        if not exceedx:
            if exceedy:
                y -= deltay
            newposlist = [
                (row + x, col + y)
                for row in range(len(newpos))
                for col in range(len(newpos[0]))
                if newpos[row][col] is True
            ]
            if set(newposlist).intersection(set(opl)) == set([]):
                self.positions = newpos
                self.posx = x
                self.posy = y
                return True

        return False

    def movDown(self):
        """move a block down"""
        self.posx += 1

    def movLeft(self):
        """move a block left"""
        self.posy -= 1

    def movRight(self):
        """move a block right"""
        self.posy += 1

    def canMovDown(self, theight, topl):
        """check if a block can move down"""
        lowest = (0, 0)
        bpl = self.getPosList()
        for pos in bpl:
            if lowest[0] < pos[0]:
                lowest = pos

        notbottomedge = lowest[0] < theight - 1
        movdownposlist = [(pos[0] + 1, pos[1]) for pos in bpl]
        return notbottomedge and set(movdownposlist).intersection(set(topl)) == set([])

    def canMovRight(self, twidth, topl):
        """check if a bloc can move right"""
        rightest = (0, 0)
        bpl = self.getPosList()
        for pos in bpl:
            if rightest[1] < pos[1]:
                rightest = pos

        notrightedge = rightest[1] < twidth - 1
        movrightposlist = [(pos[0], pos[1] + 1) for pos in bpl]
        return notrightedge and set(movrightposlist).intersection(set(topl)) == set([])

    def canMovLeft(self, twidth, topl):
        """check if a block can move left"""
        leftest = (0, twidth)
        bpl = self.getPosList()
        for pos in bpl:
            if leftest[1] > pos[1]:
                leftest = pos

        notleftedge = leftest[1] > 0
        movleftposlist = [(pos[0], pos[1] - 1) for pos in bpl]
        return notleftedge and set(movleftposlist).intersection(set(topl)) == set([])

    def getPos(self):
        """get the block position (upper left)"""
        return (self.posx, self.posy)

    def getPosList(self):
        """get the block occupied positions list"""
        l = self.positions
        x = self.posx
        y = self.posy
        return [
            (row + x, col + y)
            for row in range(len(l))
            for col in range(len(l[0]))
            if l[row][col] is True
        ]

    def show(self, surface, offx, offy, size):
        """show a block on the given surface"""
        l = self.positions
        inner_block_size = size - 4
        clip_offset = size - (size - inner_block_size) / 2
        block = pg.Surface((size, size))
        block.set_alpha(255)
        block.set_clip(2, 2, inner_block_size, inner_block_size)
        block.fill(self.color)

        for row in range(len(l)):
            for col in range(len(l[0])):
                if l[row][col]:
                    surface.blit(block, ((offx + (col * size), offy + (row * size))))
