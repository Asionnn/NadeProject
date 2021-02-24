import math
import pygame
import time
import random

circles = 0
runOnce = True
circle_list = []
black = [0, 0, 0]
reset = False
timer_status = 0


def generate_circle_lists():
    global circle_list
    global circles
    global runOnce

    num_generated = 0

    while num_generated <= 100:
        trial = []
        while circles <= 50:
            r = 20
            x = random.randint(10 + r, window.get_width() - r - 10)
            y = random.randint(10 + r, window.get_height() - r - 10)

            if not any((x2, y2, r2) for x2, y2, r2 in trial
                       if euclidean_distance(x, y, x2, y2) < r + r2) and circles <= 50:
                trial.append((x, y, r))
            circles = circles + 1
            r = 30
            x = random.randint(10 + r, window.get_width() - r - 10)
            y = random.randint(10 + r, window.get_height() - r - 10)
            if not any((x2, y2, r2) and not runOnce
                       for x2, y2, r2 in trial if euclidean_distance(x, y, x2, y2) < r + r2) and runOnce:
                trial.append((x, y, r))
                runOnce = False
        circle_list.append(trial)
        num_generated = num_generated + 1
        circles = 0
        runOnce = True


def euclidean_distance(x1, y1, x2, y2):
    return math.hypot((x1 - x2), (y1 - y2))


def draw_rect_alpha(surface, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)


def reset_variables():
    global circles
    global runOnce
    global circle_list

    circles = 0
    runOnce = True


def draw_circles():

    index = random.randint(0, 100)
    for x, y, r in circle_list[index]:
        pygame.draw.circle(window, (255, 255, 255), (round(x), round(y)), int(r), 1)
    pygame.display.flip()


def reset_circles():
    window.fill(black)
    reset_variables()
    draw_circles()


def highlight_screen(rect):
    global black
    draw_rect_alpha(window, (100, 100, 100), rect)
    pygame.display.update()
    pygame.time.wait(100)
    draw_rect_alpha(window, (0, 0, 0), rect)
    reset_circles()


if __name__ == "__main__":

    pygame.init()
    window = pygame.display.set_mode([1024, 768])
    generate_circle_lists()
    pygame.display.set_caption('SuRT Clone')
    font50 = pygame.font.SysFont(None, 50)
    window.fill(black)

    run = True

    leftRect = pygame.draw.rect(window, (0, 0, 0), (0, 0, 512, 768), 1)
    rightRect = pygame.draw.rect(window, (0, 0, 0), (512, 0, 512, 768), 1)

    draw_circles()
    start = time.time()
    interval = random.randint(3000, 5000)
    elapsed = 0

    INTERVAL_EXCEEDED = pygame.USEREVENT + 1
    pygame.time.set_timer(INTERVAL_EXCEEDED, interval, True)

    print("initial start: " + str(start))
    print("initial interval: " + str(interval))

    while run:
        if pygame.event.get(INTERVAL_EXCEEDED):
            print("interval: " + str(interval))
            print("time: " + str(time.time() - start))
            reset_circles()

            pygame.event.clear()
            interval = random.randint(3000, 5000)
            pygame.time.set_timer(INTERVAL_EXCEEDED, interval, True)

            start = time.time()
            timer_status = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                pygame.event.clear()
                if event.key == pygame.K_a:
                    highlight_screen(leftRect)
                if event.key == pygame.K_d:
                    highlight_screen(rightRect)

                interval = random.randint(3000, 5000)
                pygame.time.set_timer(INTERVAL_EXCEEDED, interval, True)

                start = time.time()


        pygame.display.flip()

    pygame.quit()
    exit()



