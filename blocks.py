#======================================================================#
# This file is part of YAT (Yet Another Tetris).                       #
#                                                                      #
# YAT is free software: you can redistribute it and/or modify          #
# it under the terms of the GNU General Public License as published by #
# the Free Software Foundation, either version 3 of the License, or    #
# (at your option) any later version.                                  #
#                                                                      #
# YAT is distributed in the hope that it will be useful,               #
# but WITHOUT ANY WARRANTY; without even the implied warranty of       #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the        #
# GNU General Public License for more details.                         #
#                                                                      #
# You should have received a copy of the GNU General Public License    #
# along with YAT.     If not, see <http://www.gnu.org/licenses/>.      #
#======================================================================#


#===============================================================#
# Name       : block.py                                         #
# Description: The block class for use in the tetris-like game. #
# Athor      : Adrian Antonana                                  #
# Date       : 17.08.2012                                       #
# Copyright  : Adrian Antonana 2012                             #
#===============================================================#
import random as rnd
import colors as clr
import pygame as pg

#===============================================================#
#                     Block Type Constants                      #
#===============================================================#
E = 0
I = 1
T = 2
S = 3
Z = 4
O = 5
L = 6
J = 7

#===============================================================#
#                    Block class definition                     #
#===============================================================#
class block:

	#-------------------- Object constructor -------------------#
	def __init__(self,(x,y),blocktype=None):
 
		# if no type is given as a parameter, the block is randomly
		# generated
		if blocktype == None:
			self.blocktype = rnd.randint(I,J)
		else:
			self.blocktype = blocktype

		# set the block position	
		self.posx      = x
		self.posy      = y

		# set blocktype, color and the shape of the block
		if self.blocktype == I:
			self.positions = [[True],[True],[True],[True]]
			self.color     = clr.RED
		elif self.blocktype == T:
			self.positions = [[True,True,True],[False,True,False]]
			self.color     = clr.MAGENTA
		elif self.blocktype == S:
			self.positions = [[False,True,True],[True,True,False]]
			self.color     = clr.YELLOW
		elif self.blocktype == Z:
			self.positions = [[True,True,False],[False,True,True]]
			self.color     = clr.BLUE
		elif self.blocktype == O:
			self.positions = [[True,True],[True,True]]
			self.color     = clr.GREEN
		elif self.blocktype == L:
			self.positions = [[True,False],[True,False],[True,True]]
			self.color     = clr.CYAN
		elif self.blocktype == J:
			self.positions = [[False,True],[False,True],[True,True]]
			self.color     = clr.ORANGE

#===============================================================#
#                    Function definitions                       #
#===============================================================#

#--------------------- get the block type ----------------------#
	def getType(self):
		return self.blocktype

#------------------- rotate a block clockwise ------------------#
	def rotRight(self,maxx,maxy,opl):
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

		newpos = [[l[row][col] for row in reversed(range(len(l)))] for col in range(len(l[0]))]

		exceedx = False
		exceedy = False

		if len(newpos)+x > maxx or x < 0:
				exceedx = True		

		if len(newpos[0])+y > maxy:
				exceedy = True
				deltay = len(newpos[0])+y-maxy

		if not exceedx:
			if exceedy:
				y -= deltay
			newposlist = [(row+x,col+y) for row in range(len(newpos)) for col in range(len(newpos[0])) if newpos[row][col] == True]
			if set(newposlist).intersection(set(opl)) == set([]):
				self.positions = newpos
				self.posx = x
				self.posy = y
				return True

		return False

#---------------- rotate a block counterclockwise --------------#
	def rotLeft(self,maxx,maxy,opl):
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

		newpos = [[l[row][col] for row in range(len(l))] for col in reversed(range(len(l[0])))]

		exceedx = False
		exceedy = False

		if len(newpos)+x > maxx or x < 0:
				exceedx = True

		if len(newpos[0])+y > maxy:
				exceedy = True
				deltay = len(newpos[0])+y-maxy

		if not exceedx:
			if exceedy:
				y -= deltay
			newposlist = [(row+x,col+y) for row in range(len(newpos)) for col in range(len(newpos[0])) if newpos[row][col] == True]
			if set(newposlist).intersection(set(opl)) == set([]):
				self.positions = newpos
				self.posx = x
				self.posy = y
				return True

		return False

#-------------------- move a block down ------------------------#
	def movDown(self):
		self.posx += 1

#-------------------- move a block left ------------------------#
	def movLeft(self):
		self.posy -= 1

#-------------------- move a block right -----------------------#
	def movRight(self):
		self.posy += 1

#------------- check if a block can move down ------------------#
	def canMovDown(self,theight,topl):
		lowest = (0,0)
		bpl = self.getPosList()
		for pos in bpl:
			if lowest[0] < pos[0]: lowest = pos

		notbottomedge = lowest[0] < theight - 1
		movdownposlist = [(pos[0]+1,pos[1]) for pos in bpl]
		return notbottomedge and set(movdownposlist).intersection(set(topl)) == set([])

#---------------- check if a bloc can move right ---------------#
	def canMovRight(self,twidth,topl):
		rightest = (0,0)
		bpl      = self.getPosList()
		for pos in bpl:
			if rightest[1] < pos[1]: rightest = pos

		notrightedge = rightest[1] < twidth - 1
		movrightposlist = [(pos[0],pos[1]+1) for pos in bpl]
		return notrightedge and set(movrightposlist).intersection(set(topl)) == set([])

#---------------- check if a block can move left ---------------#
	def canMovLeft(self,twidth,topl):
		leftest = (0,twidth)
		bpl     = self.getPosList()
		for pos in bpl:
			if leftest[1] > pos[1]: leftest = pos

		notleftedge = leftest[1] > 0
		movleftposlist = [(pos[0],pos[1]-1) for pos in bpl]
		return notleftedge and set(movleftposlist).intersection(set(topl)) == set([])
				
#------------- get the block position (upper left)--------------#
	def getPos(self):
		return (self.posx,self.posy)

#------------- get the bloc ocupied positions list -------------#
	def getPosList(self):
		l = self.positions
		x = self.posx
		y = self.posy
		return [(row+x,col+y) for row in range(len(l)) for col in range(len(l[0])) if l[row][col] == True]

#------------- show a block on the given surface ---------------#
	def show(self,surface,offx,offy,size):
		l           = self.positions
		inner_block_size = size - 4
		clip_offset = size - (size - inner_block_size) / 2
		block = pg.Surface((size,size))
		block.set_alpha(255)
		block.set_clip(2,2,inner_block_size,inner_block_size)
		block.fill(self.color)

		for row in range(len(l)):
			for col in range(len(l[0])):
				if l[row][col]:
					surface.blit(block,((offx+(col*size),offy+(row*size))))
