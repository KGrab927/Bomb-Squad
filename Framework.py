import pygame
import GridObject as go
import numpy
from random import uniform
import DrawMethods
import Button as b
import Settings as s
import threading
import os

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (100, 50)
is_rpi = 0
NUM_MINES = 10
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 780
X_OFFSET = int((SCREEN_WIDTH - (SCREEN_WIDTH/2)) / 2)
Y_OFFSET = int((SCREEN_HEIGHT - (SCREEN_WIDTH/2)) / 2)
MINE_X = 10
MINE_Y = 10
MINE_WIDTH = int((SCREEN_WIDTH - (2 * X_OFFSET)) / MINE_X)
DIFFICULTIES = ["Beginner", "Intermediate", "Advanced"]
CURRENT_SETTING = 0
TIMER = -1
clock = pygame.time.Clock()
icon = pygame.image.load('squad.png')
title = pygame.image.load('Intro.png')
pygame.display.set_icon(icon)
Matrix = [[go.GridObject() for x in range(MINE_X)] for y in range(MINE_Y)]
Buttons = [b.Button() for i in range(3)]
Settings = [s.Settings() for j in range(3)]
keepListening = True
num_mines_remaining = NUM_MINES
runGame = True
player_won = False
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption("Bomb Squad")
pygame.init()
pygame.RESIZABLE = False
is_cell_held = False
frame_count = 0
temp_held_x = -1
temp_held_y = -1


def setup():
    temp = 0
    screen.blit(title, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.flip()

    while temp < 50:
        clock.tick(10)
        temp = temp + 1

    for x in range(0, MINE_X):
        for y in range(0, MINE_Y):
            Matrix[x][y] = go.GridObject(x, y, MINE_WIDTH, X_OFFSET, Y_OFFSET)

    button_y = Y_OFFSET + ((MINE_Y * MINE_WIDTH) / len(DIFFICULTIES)) / 4
    for x in range(len(Buttons)):
        Buttons[x] = b.Button(X_OFFSET + (MINE_X * MINE_WIDTH) + (0.2 * X_OFFSET), button_y, 0.6 * X_OFFSET, SCREEN_HEIGHT / 8, DIFFICULTIES[x])
        button_y = button_y + ((MINE_Y * MINE_WIDTH) / len(DIFFICULTIES))

    for x in range(len(Settings)):
        if x == 0:
            Settings[x] = s.Settings(10, 10)
        if x == 1:
            Settings[x] = s.Settings(20, 50)
        if x == 2:
            Settings[x] = s.Settings(25, 99)

    place_mines()
    determine_numbers()


def update():
    global is_cell_held, frame_count, runGame, keepListening, CURRENT_SETTING, num_mines_remaining, temp_held_x, temp_held_y
    if is_cell_held is True:
        frame_count = frame_count + 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runGame = False
        if is_rpi == 0:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if keepListening:
                    if X_OFFSET < pygame.mouse.get_pos()[0] < (SCREEN_WIDTH - X_OFFSET) and Y_OFFSET < pygame.mouse.get_pos()[1] < (SCREEN_HEIGHT - Y_OFFSET):
                        if event.button == 1:
                            x_index = int(numpy.floor((pygame.mouse.get_pos()[0] - X_OFFSET) / MINE_WIDTH))
                            y_index = int(numpy.floor((pygame.mouse.get_pos()[1] - Y_OFFSET) / MINE_WIDTH))
                            if Matrix[x_index][y_index].flag is not True:
                                if Matrix[x_index][y_index].neighbors == 0:
                                    flood_fill(x_index, y_index)
                                else:
                                    Matrix[x_index][y_index].reveal(screen)
                                if Matrix[x_index][y_index].mine is True:
                                    Matrix[x_index][y_index].set_bg(255)
                                    for x in range(MINE_X):
                                        for y in range(MINE_Y):
                                            if Matrix[x][y].flag is True and Matrix[x][y].mine is True:
                                                pass
                                            elif Matrix[x][y].flag is True and Matrix[x][y].mine is False:
                                                Matrix[x][y].set_flag_accuracy(True)
                                                Matrix[x][y].reveal(screen)
                                            else:
                                                Matrix[x][y].reveal(screen)
                                    keepListening = False
                        elif event.button == 3:
                            temp_held_x = int(numpy.floor((pygame.mouse.get_pos()[0] - X_OFFSET) / MINE_WIDTH))
                            temp_held_y = int(numpy.floor((pygame.mouse.get_pos()[1] - Y_OFFSET) / MINE_WIDTH))
                            Matrix[temp_held_x][temp_held_y].setRightClicked(True)
                for i in range(len(Buttons)):
                    if Buttons[i].is_clicked(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                        CURRENT_SETTING = i
                        reset(CURRENT_SETTING)
                        Buttons[i].set_clicked(True)
            if event.type == pygame.MOUSEBUTTONUP:
                if keepListening:
                    for i in range(len(Buttons)):
                        if Buttons[i].clicked is True:
                            Buttons[i].set_clicked(False)
                    if X_OFFSET < pygame.mouse.get_pos()[0] < (SCREEN_WIDTH - X_OFFSET) and Y_OFFSET < pygame.mouse.get_pos()[1] < (SCREEN_HEIGHT - Y_OFFSET):
                        if event.button == 3:
                            if Matrix[temp_held_x][temp_held_y].flag is False and Matrix[temp_held_x][temp_held_y].revealed is False:
                                Matrix[temp_held_x][temp_held_y].set_flag(True)
                                num_mines_remaining = num_mines_remaining - 1
                            elif Matrix[temp_held_x][temp_held_y].flag is True and Matrix[temp_held_x][temp_held_y].revealed is False:
                                Matrix[temp_held_x][temp_held_y].remove_flag()
                                num_mines_remaining = num_mines_remaining + 1
                        Matrix[temp_held_x][temp_held_y].setRightClicked(False)
                        temp_held_x = -1
                        temp_held_y = -1
        elif is_rpi == 1:
            if event.type == pygame.MOUSEBUTTONDOWN and 200 < pygame.mouse.get_pos()[0] < 600 and 40 < pygame.mouse.get_pos()[1] < 440:
                if event.button == 1:
                    for i in range(len(Buttons)):
                        if Buttons[i].is_clicked(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                            CURRENT_SETTING = i
                            reset(CURRENT_SETTING)
                            Buttons[i].set_clicked(True)
                    for i in range(len(Buttons)):
                        if Buttons[i].clicked is True:
                            Buttons[i].set_clicked(False)
                    is_cell_held = True
            if event.type == pygame.MOUSEBUTTONUP and 200 < pygame.mouse.get_pos()[0] < 600 and 40 < pygame.mouse.get_pos()[1] < 440:
                if frame_count >= 20:
                    if keepListening:
                        if X_OFFSET < pygame.mouse.get_pos()[0] < (SCREEN_WIDTH - X_OFFSET) and Y_OFFSET < pygame.mouse.get_pos()[1] < (SCREEN_HEIGHT - Y_OFFSET):
                            if Matrix[temp_held_x][temp_held_y].flag is False and Matrix[temp_held_x][temp_held_y].revealed is False:
                                Matrix[temp_held_x][temp_held_y].set_flag(True)
                                num_mines_remaining = num_mines_remaining - 1
                            elif Matrix[temp_held_x][temp_held_y].flag is True and Matrix[temp_held_x][temp_held_y].revealed is False:
                                Matrix[temp_held_x][temp_held_y].remove_flag()
                                num_mines_remaining = num_mines_remaining + 1
                            Matrix[temp_held_x][temp_held_y].setRightClicked(False)
                            temp_held_x = -1
                            temp_held_y = -1
                else:
                    if keepListening:
                        if X_OFFSET < pygame.mouse.get_pos()[0] < (SCREEN_WIDTH - X_OFFSET) and Y_OFFSET < pygame.mouse.get_pos()[1] < (SCREEN_HEIGHT - Y_OFFSET):
                            x_index = int(numpy.floor((pygame.mouse.get_pos()[0] - X_OFFSET) / MINE_WIDTH))
                            y_index = int(numpy.floor((pygame.mouse.get_pos()[1] - Y_OFFSET) / MINE_WIDTH))
                            if Matrix[x_index][y_index].flag is not True:
                                if Matrix[x_index][y_index].neighbors == 0:
                                    flood_fill(x_index, y_index)
                                else:
                                    Matrix[x_index][y_index].reveal(screen)
                                if Matrix[x_index][y_index].mine is True:
                                    Matrix[x_index][y_index].set_bg(255)
                                    for x in range(MINE_X):
                                        for y in range(MINE_Y):
                                            if Matrix[x][y].flag is True and Matrix[x][y].mine is True:
                                                pass
                                            elif Matrix[x][y].flag is True and Matrix[x][y].mine is False:
                                                Matrix[x][y].set_flag_accuracy(True)
                                                Matrix[x][y].reveal(screen)
                                            else:
                                                Matrix[x][y].reveal(screen)
                                    keepListening = False
                frame_count = 0
                is_cell_held = False


def draw():
    screen.fill([125, 125, 255])
    for x in range(0, MINE_X):
        for y in range(0, MINE_Y):
            Matrix[x][y].show(screen)
    for x in range(len(Buttons)):
        Buttons[x].draw(screen, int(X_OFFSET/10))
    DrawMethods.draw_mines_remaining(screen, num_mines_remaining, int(X_OFFSET/10), X_OFFSET, SCREEN_HEIGHT)
    DrawMethods.draw_timer(screen, TIMER, int(X_OFFSET/10), X_OFFSET, SCREEN_HEIGHT)
    if not keepListening and player_won is False:
        font = pygame.font.SysFont('Arial', int(SCREEN_WIDTH/14))
        text_width, text_height = font.size("YOU LOST")
        DrawMethods.text_to_screen(screen, str("YOU LOST"), (SCREEN_WIDTH/6) - text_width/2, (SCREEN_HEIGHT/2) - text_height/2, int(SCREEN_WIDTH/19), [200, 0, 0])
    if player_won is True:
        font = pygame.font.SysFont('Arial', int(SCREEN_WIDTH/14))
        text_width, text_height = font.size("YOU WON")
        DrawMethods.text_to_screen(screen, str("YOU WON"), (SCREEN_WIDTH/6) - text_width/2, (SCREEN_HEIGHT/2) - text_height/2, int(SCREEN_WIDTH/19), [0, 200, 0])


def place_mines():
    x_values = []
    y_values = []
    for x in range(0, NUM_MINES):
        duplicate = False
        if x != 0:
            while True:
                x_ind = int(uniform(0, MINE_X))
                y_ind = int(uniform(0, MINE_Y))
                for val in range(0, len(x_values)):
                    if x_values[val] == x_ind and y_values[val] == y_ind:
                        duplicate = True
                if duplicate is False:
                    break
                else:
                    duplicate = False
        else:
            x_ind = int(uniform(0, MINE_X))
            y_ind = int(uniform(0, MINE_Y))
        Matrix[x_ind][y_ind].set_mine()
        x_values.append(x_ind)
        y_values.append(y_ind)


def determine_numbers():
    for x in range(0, MINE_X):
        for y in range(0, MINE_Y):
            neighbor = 0
            if Matrix[x][y].mine is True:
                Matrix[x][y].determine_neighbors(-1)
                continue
            for a in range(-1, 2):
                for c in range(-1, 2):
                    i = x + a
                    j = y + c
                    if -1 < i < MINE_X and -1 < j < MINE_Y:
                        if Matrix[i][j].mine is True:
                            neighbor = neighbor + 1
            Matrix[x][y].determine_neighbors(neighbor)


def flood_fill(x, y):
    global num_mines_remaining
    for a in range(-1, 2):
        for d in range(-1, 2):
            i = x + a
            j = y + d
            if -1 < i < MINE_X and -1 < j < MINE_Y:
                if Matrix[i][j].neighbors >= 0 and Matrix[i][j].mine is False and Matrix[i][j].revealed is False:
                    if Matrix[i][j].flag is True:
                        num_mines_remaining = num_mines_remaining + 1
                        Matrix[i][j].set_flag(False)
                    Matrix[i][j].reveal(screen)
                    if Matrix[i][j].neighbors == 0:
                        flood_fill(i, j)


def increment_timer():
    global t
    t = threading.Timer(1.0, increment_timer)
    t.start()
    global TIMER
    if keepListening:
        TIMER = TIMER + 1


def is_done():
    global keepListening
    global player_won
    global num_mines_remaining
    num_left = 0
    hidden_x = []
    hidden_y = []
    for x in range(MINE_X):
        for y in range(MINE_Y):
            if Matrix[x][y].revealed is False and Matrix[x][y].flag is False:
                num_left = num_left + 1
                hidden_x.append(x)
                hidden_y.append(y)

    if num_left == num_mines_remaining:
        for x in range(num_left):
            Matrix[hidden_x[x]][hidden_y[x]].set_flag(True)
            keepListening = False
            player_won = True
            num_mines_remaining = 0

    done = False
    if num_mines_remaining == 0:
        for x in range(MINE_X):
            for y in range(MINE_Y):
                if Matrix[x][y].flag is False and Matrix[x][y].revealed is False:
                    return
                if Matrix[x][y].flag is True:
                    if Matrix[x][y].mine is False:
                        done = False
                        break
        done = True

    if done is True:
        keepListening = False
        player_won = True


def reset(setting):
    global Matrix, keepListening, num_mines_remaining, runGame, screen, is_cell_held, frame_count, NUM_MINES, MINE_X, MINE_Y, MINE_WIDTH, TIMER, player_won
    NUM_MINES = Settings[setting].mines
    MINE_X = Settings[setting].mine_xbx
    MINE_Y = Settings[setting].mine_xbx
    MINE_WIDTH = int((SCREEN_WIDTH - (2 * X_OFFSET)) / MINE_X)
    Matrix = [[go.GridObject() for x in range(MINE_X)] for y in range(MINE_Y)]
    keepListening = True
    runGame = True
    is_cell_held = False
    player_won = False
    num_mines_remaining = NUM_MINES
    frame_count = 0
    for x in range(0, MINE_X):
        for y in range(0, MINE_Y):
            Matrix[x][y] = go.GridObject(x, y, MINE_WIDTH, X_OFFSET, Y_OFFSET)
    place_mines()
    determine_numbers()
    TIMER = 0


setup()
t = threading.Timer(0, increment_timer)
increment_timer()

while runGame:
    draw()
    pygame.display.flip()
    clock.tick(120)
    update()
    is_done()

pygame.quit()
t.cancel()
exit()
