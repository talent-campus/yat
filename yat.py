"""
Yet Another Tetris. Main game file for the tetris like game "yat"

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
import pygame as pg
import table as tb
import blocks as bk
import colors as col

# Global Variables and Constants
GAME_SPEED = 500
SPEED_INC_TICK = 50
LINES_INC_TICK = 10
LEVEL = 1
REMOVED_LINES = 0
MAX_LEVEL = 10
FPS = 100

def delay(ticks):
    """Checks when blocks have to move down"""
    return (ticks % GAME_SPEED) >= GAME_SPEED - 10


def incSpeed(remlines):
    """Increases the Game Level and Game Speed"""
    global GAME_SPEED
    global LEVEL

    if LEVEL < MAX_LEVEL:
        if remlines / (LEVEL * LINES_INC_TICK) == 1:
            LEVEL += 1
            GAME_SPEED -= SPEED_INC_TICK
            return True
    return False


def updateInfo(nb):
    """Updates the information surface"""
    global LEVEL_NUM_TEXT
    global LINES_NUM_TEXT
    global infosurface

    LEVEL_NUM_TEXT = font.render(str(LEVEL), True, col.WHITE)
    LINES_NUM_TEXT = font.render(str(REMOVED_LINES), True, col.WHITE)
    infosurface.fill(col.GREY_DARK)
    infosurface.blit(LEVEL_TEXT, LEVEL_TEXT_OFFSET)
    infosurface.blit(LEVEL_NUM_TEXT, LEVEL_NUM_TEXT_OFFSET)
    infosurface.blit(LINES_TEXT, LINES_TEXT_OFFSET)
    infosurface.blit(LINES_NUM_TEXT, LINES_NUM_TEXT_OFFSET)
    nb.show(infosurface, NEXT_BLOCK_OFFSET, 20, INF_BLOCK_SIZE)


# Initialize pygame (display,mixer and clock)
pg.init()
pg.mixer.init()
sndblockplaced = pg.mixer.Sound("sounds/block_placed.wav")
sndblockrotate = pg.mixer.Sound("sounds/block_rotate.wav")
sndremovelines = pg.mixer.Sound("sounds/remove_lines.wav")
sndlevelup = pg.mixer.Sound("sounds/level_up.wav")
sndgameover = pg.mixer.Sound("sounds/game_over.wav")
clock = pg.time.Clock()
pg.display.set_caption("yat - yet another tetris")
pg.key.set_repeat(10, 50)

# Information surface
INFO_SURFACE_HEIGHT = 105
FONT_SIZE = 30
FONT_SIZE_GAME_OVER = 60
UPPER_OFFSET = 20
LEFT_OFFSET = 10
INF_BLOCK_SIZE = 20
font = pg.font.SysFont(pg.font.get_default_font(), FONT_SIZE)
font_game_over = pg.font.SysFont(pg.font.get_default_font(), FONT_SIZE_GAME_OVER)
LEVEL_TEXT = font.render("Level : ", True, col.WHITE)
LINES_TEXT = font.render("Lines : ", True, col.WHITE)
LEVEL_TEXT_OFFSET = (LEFT_OFFSET, UPPER_OFFSET)
LEVEL_NUM_TEXT_OFFSET = (70 + LEFT_OFFSET, UPPER_OFFSET)
LINES_TEXT_OFFSET = (LEFT_OFFSET, INFO_SURFACE_HEIGHT - 40)
LINES_NUM_TEXT_OFFSET = (70 + LEFT_OFFSET, INFO_SURFACE_HEIGHT - 40)
NEXT_BLOCK_OFFSET = tb.BLOCK_SIZE * tb.WIDTH - INF_BLOCK_SIZE * 5

# Game over text
GAME_OVER_TEXT = font_game_over.render("GAME OVER", True, col.WHITE)
GAME_OVER_TEXT_OFFSET = (
    (tb.BLOCK_SIZE * tb.WIDTH / 2) - 120,
    (tb.BLOCK_SIZE * tb.HEIGHT / 2) - 50,
)

# Initialize surfaces
screen = pg.display.set_mode(
    (tb.BLOCK_SIZE * tb.WIDTH, tb.BLOCK_SIZE * tb.HEIGHT + INFO_SURFACE_HEIGHT)
)
tablesurface = screen.subsurface(
    (0, INFO_SURFACE_HEIGHT, tb.BLOCK_SIZE * tb.WIDTH, tb.BLOCK_SIZE * tb.HEIGHT)
)
infosurface = screen.subsurface((0, 0, tb.BLOCK_SIZE * tb.WIDTH, INFO_SURFACE_HEIGHT))

# Block spawn position
BLOCK_SPAWN_POS = (0, (tb.WIDTH / 2) - 1)

# Create the table and an initial block
t = tb.table(tablesurface)
b = bk.block(BLOCK_SPAWN_POS)
nextb = bk.block(BLOCK_SPAWN_POS)

# Draw initial information surface
updateInfo(nextb)

# Main loop
running = True

while running:
    clock.tick_busy_loop(FPS)
    t.adBlock(b.getPosList(), b.getType())
    t.show()

    # check if the fall delay has been reached. If yes, move block down.
    if delay(pg.time.get_ticks()):
        if b.canMovDown(t.getHeight(), t.getOcupPosList(b.getPosList())):
            t.adBlock(b.getPosList(), bk.E)
            b.movDown()
        else:
            # if the block can't move down, spawn a new block
            t.adBlock(b.getPosList(), b.getType())
            sndblockplaced.play()
            retval = t.delFullLines()
            if retval != 0:
                sndremovelines.play()
                REMOVED_LINES += retval
                if incSpeed(REMOVED_LINES):
                    sndlevelup.play()
            b.__init__(BLOCK_SPAWN_POS, nextb.getType())
            nextb = bk.block(BLOCK_SPAWN_POS)
            updateInfo(nextb)

            # check if the game is over
            if t.gameOver(b.getPosList()):
                t.adBlock(b.getPosList(), b.getType())
                t.show()
                running = False

    # get one event from the queue and perform action
    event = pg.event.poll()
    if event.type == pg.KEYDOWN:
        key = event.key
        if key == pg.K_ESCAPE:
            running = False
        elif key == pg.K_DOWN:
            if b.canMovDown(t.getHeight(), t.getOcupPosList(b.getPosList())):
                t.adBlock(b.getPosList(), bk.E)
                b.movDown()
            else:
                # if the block can't move down, spawn a new block
                t.adBlock(b.getPosList(), b.getType())
                sndblockplaced.play()
                retval = t.delFullLines()
                if retval != 0:
                    sndremovelines.play()
                    REMOVED_LINES += retval
                    if incSpeed(REMOVED_LINES):
                        sndlevelup.play()
                b.__init__(BLOCK_SPAWN_POS, nextb.getType())
                nextb = bk.block(BLOCK_SPAWN_POS)
                updateInfo(nextb)

                # check if the game is over
                if t.gameOver(b.getPosList()):
                    t.adBlock(b.getPosList(), b.getType())
                    t.show()
                    running = False

        # move/rotate block left/right
        elif key == pg.K_LEFT:
            if b.canMovLeft(t.getWidth(), t.getOcupPosList(b.getPosList())):
                t.adBlock(b.getPosList(), bk.E)
                b.movLeft()
        elif key == pg.K_RIGHT:
            if b.canMovRight(t.getWidth(), t.getOcupPosList(b.getPosList())):
                t.adBlock(b.getPosList(), bk.E)
                b.movRight()
        elif key == pg.K_LCTRL:
            t.adBlock(b.getPosList(), bk.E)
            if b.rotLeft(t.getHeight(), t.getWidth(), t.getOcupPosList(b.getPosList())):
                sndblockrotate.play()
        elif key == pg.K_LALT:
            t.adBlock(b.getPosList(), bk.E)
            if b.rotRight(
                t.getHeight(), t.getWidth(), t.getOcupPosList(b.getPosList())
            ):
                sndblockrotate.play()

# The game is over
tablesurface.fill(col.BLACK)
t.setSurfAlpha(60)
t.show()
tablesurface.blit(GAME_OVER_TEXT, GAME_OVER_TEXT_OFFSET)
pg.display.flip()
sndgameover.play()

quit = False
while not quit:
    event = pg.event.wait()
    if event.type == pg.QUIT:
        quit = True
    if event.type == pg.KEYDOWN:
        if event.key == pg.K_ESCAPE:
            quit = True
