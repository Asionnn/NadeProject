import math
import pygame
import time
import random


def euclidean_distance(x1, y1, x2, y2):
    # return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    return math.hypot((x1 - x2), (y1 - y2))


def draw_rect_alpha(surface, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)


if __name__ == "__main__":
    pygame.init()
    clock = pygame.time.Clock()
    window = pygame.display.set_mode([1024, 768])
    pygame.display.set_caption('SuRT Clone')
    font50 = pygame.font.SysFont(None, 50)
    black = [0, 0, 0]
    window.fill(black)

    run = True
    runOnce = True
    circle_list = []
    circles = 0

    leftRect = pygame.draw.rect(window, (0, 0, 0), (0, 0, 512, 768), 1)
    rightRect = pygame.draw.rect(window, (0, 0, 0), (512, 0, 512, 768), 1)

    while run:
        r = 20
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    draw_rect_alpha(window, (100, 100, 100), leftRect)
                    pygame.display.update()
                    pygame.time.wait(300)
                    draw_rect_alpha(window, (0, 0, 0), leftRect)
                if event.key == pygame.K_d:
                    draw_rect_alpha(window, (100, 100, 100), rightRect)
                    pygame.display.update()
                    pygame.time.wait(300)
                    draw_rect_alpha(window, (0, 0, 0), rightRect)

        x = random.randint(10 + r, window.get_width() - r - 10)
        y = random.randint(10 + r, window.get_height() - r - 10)

        if not any((x2, y2, r2) for x2, y2, r2 in circle_list
                   if euclidean_distance(x, y, x2, y2) < r + r2) and circles <= 50:
            circle_list.append((x, y, r))
            circles = circles + 1

        r = 30
        x = random.randint(10 + r, window.get_width() - r - 10)
        y = random.randint(10 + r, window.get_height() - r - 10)
        if not any((x2, y2, r2) and not runOnce
                   for x2, y2, r2 in circle_list if euclidean_distance(x, y, x2, y2) < r + r2) and runOnce:
            circle_list.append((x, y, r))
            runOnce = False

        for x, y, r in circle_list:
            pygame.draw.circle(window, (255, 255, 255), (round(x), round(y)), int(r), 1)
        # window.blit(font50.render(str(circles), True, (255, 0, 0)), (10, 10))
        pygame.display.flip()

    pygame.quit()
    exit()



