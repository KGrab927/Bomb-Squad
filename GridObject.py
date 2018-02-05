import pygame
import DrawMethods


class GridObject:

    def __init__(self, i=None, j=None, width=None, x_offset=0, y_offset=0, bg=200):
        self.i = i
        self.j = j
        self.width = width
        self.revealed = False
        self.mine = False
        self.neighbors = 0
        self.flag = False
        self.x_off = x_offset
        self.y_off = y_offset
        self.rc = False
        self.bg = bg
        self.wrong_flag = False

    def show(self, screen):
        if self.mine is True and self.revealed is True:
            if self.bg == 200:
                pygame.draw.rect(screen, [self.bg, self.bg, self.bg], [self.i * self.width + self.x_off, self.j * self.width + self.y_off, self.width, self.width])
            else:
                pygame.draw.rect(screen, [self.bg, 0, 0], [self.i * self.width + self.x_off, self.j * self.width + self.y_off, self.width, self.width])
            pygame.draw.rect(screen, [50, 50, 50], [self.i * self.width + self.x_off, self.j * self.width + self.y_off, self.width, self.width], 1)
            DrawMethods.draw_bomb(screen, self.i * self.width + self.x_off, self.j * self.width + self.y_off, self.width)
        elif self.revealed is False and self.flag is True:
            pygame.draw.rect(screen, [165, 165, 165], [self.i * self.width + self.x_off, self.j * self.width + self.y_off, self.width, self.width])
            if self.rc is False:
                pygame.draw.rect(screen, [255, 255, 255], [self.i * self.width + self.x_off, self.j * self.width + self.y_off, self.width/10, self.width])
                pygame.draw.rect(screen, [255, 255, 255], [self.i * self.width + self.x_off, self.j * self.width + self.y_off, self.width, self.width/10])
                pygame.draw.rect(screen, [100, 100, 100], [self.i * self.width + self.x_off, self.j * self.width + self.y_off + (9 * self.width/10), self.width, self.width/10])
                pygame.draw.rect(screen, [100, 100, 100], [self.i * self.width + self.x_off + (9 * self.width/10), self.j * self.width + self.y_off, self.width/10, self.width])
                pygame.draw.polygon(screen, [255, 255, 255], [[self.i * self.width + self.x_off + (9 * self.width/10), self.j * self.width + self.y_off],
                                        [self.i * self.width + self.x_off + self.width, self.j * self.width + self.y_off],
                                        [self.i * self.width + self.x_off + (9 * self.width/10), self.j * self.width + self.y_off + (self.width/10)]])
                pygame.draw.polygon(screen, [255, 255, 255], [[self.i * self.width + self.x_off, self.j * self.width + self.y_off + (9 * self.width/10) - 1],
                                        [self.i * self.width + self.x_off + (self.width/10) - 1, self.j * self.width + self.y_off + (9 * self.width/10) - 1],
                                        [self.i * self.width + self.x_off - 1, self.j * self.width + self.y_off + self.width]])
            else:
                pygame.draw.rect(screen, [100, 100, 100], [self.i * self.width + self.x_off, self.j * self.width + self.y_off, self.width / 10, self.width])
                pygame.draw.rect(screen, [100, 100, 100], [self.i * self.width + self.x_off, self.j * self.width + self.y_off, self.width, self.width / 10])
                pygame.draw.rect(screen, [255, 255, 255], [self.i * self.width + self.x_off, self.j * self.width + self.y_off + (9 * self.width / 10), self.width, self.width / 10])
                pygame.draw.rect(screen, [255, 255, 255], [self.i * self.width + self.x_off + (9 * self.width / 10), self.j * self.width + self.y_off, self.width / 10, self.width])
                pygame.draw.polygon(screen, [100, 100, 100], [[self.i * self.width + self.x_off + (9 * self.width / 10), self.j * self.width + self.y_off],
                                                              [self.i * self.width + self.x_off + self.width, self.j * self.width + self.y_off],
                                                              [self.i * self.width + self.x_off + (9 * self.width / 10), self.j * self.width + self.y_off + (self.width / 10)]])
                pygame.draw.polygon(screen, [100, 100, 100], [[self.i * self.width + self.x_off, self.j * self.width + self.y_off + (9 * self.width / 10) - 1],
                                                              [self.i * self.width + self.x_off + (self.width / 10) - 1, self.j * self.width + self.y_off + (9 * self.width / 10) - 1],
                                                              [self.i * self.width + self.x_off - 1, self.j * self.width + self.y_off + self.width]])
            DrawMethods.draw_flag(screen, self.i * self.width + self.x_off, self.j * self.width + self.y_off, self.width)
            pygame.draw.rect(screen, [50, 50, 50], [self.i * self.width + self.x_off, self.j * self.width + self.y_off, self.width, self.width], 1)
        elif self.revealed is True:
            pygame.draw.rect(screen, [200, 200, 200], [self.i * self.width + self.x_off, self.j * self.width + self.y_off, self.width, self.width])
            pygame.draw.rect(screen, [50, 50, 50], [self.i * self.width + self.x_off, self.j * self.width + self.y_off, self.width, self.width], 1)
            if self.neighbors > 0:
                if self.neighbors == 1:
                    DrawMethods.text_to_screen(screen, str(self.neighbors), self.i * self.width + (self.width/4.375) + self.x_off, self.j * self.width - 2 + self.y_off, self.width, [0, 0, 255])
                elif self.neighbors == 2:
                    DrawMethods.text_to_screen(screen, str(self.neighbors), self.i * self.width + (self.width/4.375) + self.x_off, self.j * self.width - 2 + self.y_off, self.width, [0, 140, 0])
                elif self.neighbors == 3:
                    DrawMethods.text_to_screen(screen, str(self.neighbors), self.i * self.width + (self.width/4.375) + self.x_off, self.j * self.width - 2 + self.y_off, self.width, [255, 0, 0])
                else:
                    DrawMethods.text_to_screen(screen, str(self.neighbors), self.i * self.width + (self.width/4.375) + self.x_off, self.j * self.width - 2 + self.y_off, self.width)
        else:
            pygame.draw.rect(screen, [165, 165, 165], [self.i * self.width + self.x_off, self.j * self.width + self.y_off, self.width, self.width])
            if self.rc is False:
                pygame.draw.rect(screen, [255, 255, 255], [self.i * self.width + self.x_off, self.j * self.width + self.y_off, self.width/10, self.width])
                pygame.draw.rect(screen, [255, 255, 255], [self.i * self.width + self.x_off, self.j * self.width + self.y_off, self.width, self.width/10])
                pygame.draw.rect(screen, [100, 100, 100], [self.i * self.width + self.x_off, self.j * self.width + self.y_off + (9 * self.width/10), self.width, self.width/10])
                pygame.draw.rect(screen, [100, 100, 100], [self.i * self.width + self.x_off + (9 * self.width/10), self.j * self.width + self.y_off, self.width/10, self.width])
                pygame.draw.polygon(screen, [255, 255, 255], [[self.i * self.width + self.x_off + (9 * self.width/10), self.j * self.width + self.y_off],
                                        [self.i * self.width + self.x_off + self.width, self.j * self.width + self.y_off],
                                        [self.i * self.width + self.x_off + (9 * self.width/10), self.j * self.width + self.y_off + (self.width/10)]])
                pygame.draw.polygon(screen, [255, 255, 255], [[self.i * self.width + self.x_off, self.j * self.width + self.y_off + (9 * self.width/10) - 1],
                                        [self.i * self.width + self.x_off + (self.width/10) - 1, self.j * self.width + self.y_off + (9 * self.width/10) - 1],
                                        [self.i * self.width + self.x_off - 1, self.j * self.width + self.y_off + self.width]])
            else:
                pygame.draw.rect(screen, [100, 100, 100], [self.i * self.width + self.x_off, self.j * self.width + self.y_off, self.width / 10, self.width])
                pygame.draw.rect(screen, [100, 100, 100], [self.i * self.width + self.x_off, self.j * self.width + self.y_off, self.width, self.width / 10])
                pygame.draw.rect(screen, [255, 255, 255], [self.i * self.width + self.x_off, self.j * self.width + self.y_off + (9 * self.width / 10), self.width, self.width / 10])
                pygame.draw.rect(screen, [255, 255, 255], [self.i * self.width + self.x_off + (9 * self.width / 10), self.j * self.width + self.y_off, self.width / 10, self.width])
                pygame.draw.polygon(screen, [100, 100, 100], [[self.i * self.width + self.x_off + (9 * self.width / 10), self.j * self.width + self.y_off],
                                                              [self.i * self.width + self.x_off + self.width, self.j * self.width + self.y_off],
                                                              [self.i * self.width + self.x_off + (9 * self.width / 10), self.j * self.width + self.y_off + (self.width / 10)]])
                pygame.draw.polygon(screen, [100, 100, 100], [[self.i * self.width + self.x_off, self.j * self.width + self.y_off + (9 * self.width / 10) - 1],
                                                              [self.i * self.width + self.x_off + (self.width / 10) - 1, self.j * self.width + self.y_off + (9 * self.width / 10) - 1],
                                                              [self.i * self.width + self.x_off - 1, self.j * self.width + self.y_off + self.width]])
            pygame.draw.rect(screen, [50, 50, 50], [self.i * self.width + self.x_off, self.j * self.width + self.y_off, self.width, self.width], 1)
        if self.wrong_flag is True:
            pygame.draw.line(screen, [255, 0, 0], [self.i * self.width + self.x_off + 1, self.j * self.width + self.y_off + 1],
                             [self.i * self.width + self.x_off + self.width - 1, self.j * self.width + self.y_off + self.width - 1], 3)
            pygame.draw.line(screen, [255, 0, 0], [self.i * self.width + self.x_off + self.width - 1, self.j * self.width + self.y_off + 1],
                             [self.i * self.width + self.x_off + 1, self.j * self.width + self.y_off + self.width - 1], 3)

    def reveal(self, scr):
        self.revealed = True
        self.show(scr)

    def set_mine(self):
        self.mine = True

    def set_flag(self, val):
        self.flag = val

    def remove_flag(self):
        self.flag = False

    def determine_neighbors(self, n):
        self.neighbors = n

    def setRightClicked(self, val):
        self.rc = val

    def set_bg(self, num):
        self.bg = num

    def set_flag_accuracy(self, val):
        self.wrong_flag = val
