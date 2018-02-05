import pygame
import DrawMethods as dm


class Button:

    def __init__(self, x=0, y=0, w=0, h=0, text=""):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.text = text
        self.clicked = False

    def draw(self, screen, size):
        pygame.draw.rect(screen, [200, 200, 200], [self.x, self.y, self.w, self.h])
        if self.clicked is False:
            pygame.draw.rect(screen, [255, 255, 255], [self.x, self.y, self.w / 20, self.h])
            pygame.draw.rect(screen, [255, 255, 255], [self.x, self.y, self.w, self.h / 10])
            pygame.draw.rect(screen, [100, 100, 100], [self.x, self.y + (9 * self.h / 10) + 1, self.w, self.h / 10])
            pygame.draw.rect(screen, [100, 100, 100], [self.x + (19 * self.w / 20) + 1, self.y, self.w / 20, self.h])
            pygame.draw.polygon(screen, [255, 255, 255], [[self.x + (19 * self.w / 20), self.y],
                                                          [self.x + self.w - 2, self.y],
                                                          [self.x + (19 * self.w / 20), self.y + (self.h / 10) - 1]])
            pygame.draw.polygon(screen, [255, 255, 255], [[self.x, self.y + (9 * self.h / 10) - 1],
                                                          [self.x + (self.w / 20) - 1, self.y + (9 * self.h / 10) - 1],
                                                          [self.x, self.y + self.h - 1]])
        else:
            pygame.draw.rect(screen, [100, 100, 100], [self.x, self.y, self.w / 20, self.h])
            pygame.draw.rect(screen, [100, 100, 100], [self.x, self.y, self.w, self.h / 10])
            pygame.draw.rect(screen, [255, 255, 255], [self.x, self.y + (9 * self.h / 10), self.w, self.h / 10 + 1])
            pygame.draw.rect(screen, [255, 255, 255], [self.x + (19 * self.w / 20) + 1, self.y, self.w / 20, self.h])
            pygame.draw.polygon(screen, [100, 100, 100], [[self.x + (19 * self.w / 20), self.y],
                                                          [self.x + self.w - 1, self.y],
                                                          [self.x + (19 * self.w / 20), self.y + (self.h / 10) - 1]])
            pygame.draw.polygon(screen, [100, 100, 100], [[self.x, self.y + (9 * self.h / 10) - 1],
                                                          [self.x + (self.w / 20) - 1, self.y + (9 * self.h / 10) - 1],
                                                          [self.x, self.y + self.h]])

        font = pygame.font.SysFont('Arial', size)
        text_width, text_height = font.size(self.text)
        dm.text_to_screen(screen, self.text, self.x + (self.w - text_width)/2, self.y + (self.h - text_height)/2, size)

    def is_clicked(self, x, y):
        if self.x < x < (self.x + self.w) and self.y < y < (self.y + self.h):
            return True
        else:
            return False

    def set_clicked(self, val):
        self.clicked = val
