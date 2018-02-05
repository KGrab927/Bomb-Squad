import pygame


def text_to_screen(screen, text, x, y, size=16, color=(000, 000, 000), font_type='Arial'):
    try:
        my_font = pygame.font.SysFont(font_type, size)
        label = my_font.render(text, True, color)
        screen.blit(label, (x, y))
    except Exception as e:
        print('Font Error, didn''t init pygame')
        raise e


def draw_flag(screen, x, y, width):
    pygame.draw.rect(screen, [0, 0, 0], [x + width/2, y + width/4, 2, width/2 + 1])
    pygame.draw.polygon(screen, [0, 0, 0],
                        [[x + width/2, y + (3 * width/4)], [x + width/2 - (width/4), y + ((7 * width)/8)], [x + width/2 + (width / 4), y + ((7 * width)/8)]])
    pygame.draw.polygon(screen, [255, 0, 0],
                        [[x + width / 2 + 1, y + (width/4)], [x + width/2, y + (width/4)], [x + width / 2 - (width/4), y + ((3 * width)/8)],
                         [x + width/2, y + (width/2)], [x + width / 2 + 1, y + (width/2)]])


def draw_bomb(screen, x, y, width):
    pygame.draw.ellipse(screen, [0, 0, 0], [x + width / 4, y + width / 4, 2 * width / 4 + 1, 2 * width / 4 + 1])
    pygame.draw.rect(screen, [0, 0, 0], [x + width / 2 - 1, y + width / 8 + 1, 2, width / 8])
    pygame.draw.rect(screen, [0, 0, 0], [x + width / 2 - 1, y + 6 * width / 8, 2, width / 8])
    pygame.draw.rect(screen, [0, 0, 0], [x + width / 8, y + width / 2 - 1, 3 * width / 16, 2])
    pygame.draw.rect(screen, [0, 0, 0], [x + 6 * width / 8, y + width / 2 - 1, width / 8, 2])
    pygame.draw.line(screen, [0, 0, 0], [x + width / 4, y + width / 4], [x + width / 2, y + width / 2], 3)
    pygame.draw.line(screen, [0, 0, 0], [x + width / 4, y + 3 * width / 4], [x + width / 2, y + width / 2], 3)
    pygame.draw.line(screen, [0, 0, 0], [x + 3 * width / 4, y + width / 4], [x + width / 2, y + width / 2], 3)
    pygame.draw.line(screen, [0, 0, 0], [x + 3 * width / 4, y + 3 * width / 4], [x + width / 2, y + width / 2], 3)
    pygame.draw.ellipse(screen, [255, 255, 255], [x + 3.55 * width / 9, y + 3.55 * width / 9, width / 8, width / 8])


def draw_mines_remaining(screen, num, size, x_off, height):
    mines = str("MINES")
    remaining = str("REMAINING:")
    font = pygame.font.SysFont('Arial', size)
    m_dim = font.size(mines)
    r_dim = font.size(remaining)
    n_dim = font.size(str(num))
    text_to_screen(screen, mines, (x_off/2) - m_dim[0]/2, 3*height/16, size, [255, 255, 255])
    text_to_screen(screen, remaining, (x_off/2) - r_dim[0]/2, 4*height/16, size, [255, 255, 255])
    text_to_screen(screen, str(num), (x_off/2) - n_dim[0]/2, 5*height/16, size, [255, 255, 255])
    pygame.draw.rect(screen, [0, 0, 0], [(x_off/2 - r_dim[0]/2) / 2, 2.35 * height / 16, (x_off/2 - r_dim[0]/2) + r_dim[0], height/4], 4)


def draw_timer(screen, timer, size, x_off, height):
    time = str("TIME:")
    font = pygame.font.SysFont('Arial', size)
    t_dim = font.size(time)
    clock_dim = font.size(str(timer))
    text_to_screen(screen, time, (x_off/2) - t_dim[0]/2, 10 * height / 16, size, [255, 255, 255])
    text_to_screen(screen, str(timer), (x_off/2) - clock_dim[0]/2, 12 * height / 16, size, [255, 255, 255])
    pygame.draw.rect(screen, [0, 0, 0], [(x_off/2 - t_dim[0]/2) / 2, 9.35 * height / 16, (x_off/2 - t_dim[0]/2) + t_dim[0], height / 4], 4)
