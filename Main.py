import math
import pygame
import time
import random

circle_list = []
correct_circle_location = []
black = [0, 0, 0]
circles = 0
random_circle_index = 0
runOnce = True


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
                if x <= 512:
                    correct_circle_location.append(0)
                else:
                    correct_circle_location.append(1)

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
    global random_circle_index
    random_circle_index = random.randint(0, 100)
    for x, y, r in circle_list[random_circle_index]:
        pygame.draw.circle(window, (255, 255, 255), (round(x), round(y)), int(r), 1)
    pygame.display.flip()


def reset_circles():
    window.fill(black)
    reset_variables()
    draw_circles()


def highlight_screen(rect, side):
    global black, correct_circle_location, random_circle_index
    draw_rect_alpha(window, (100, 100, 100), rect)
    pygame.display.update()
    pygame.time.wait(100)
    draw_rect_alpha(window, (0, 0, 0), rect)

    if side == correct_circle_location[random_circle_index]:
        print("Correct")
    else:
        print("Wrong")

    reset_circles()


if __name__ == "__main__":
    run = True

    # Initialize pygame
    pygame.init()
    window = pygame.display.set_mode([1024, 768])
    generate_circle_lists()
    pygame.display.set_caption('SuRT Clone')
    font50 = pygame.font.SysFont(None, 50)
    window.fill(black)

    # Draw opaque rectandles for left and right sides
    leftRect = pygame.draw.rect(window, (0, 0, 0), (0, 0, 512, 768), 1)
    rightRect = pygame.draw.rect(window, (0, 0, 0), (512, 0, 512, 768), 1)

    # Render circles and set up interval
    draw_circles()
    interval = random.randint(3000, 5000)

    # Keep track of the game time
    game_start_time = time.time()
    start_time = time.time()

    while run:
        if (time.time() - start_time) * 1000 >= interval:
            print("interval: " + str(interval))
            print("time: " + str(time.time() - start_time))
            interval = random.randint(3000, 5000)
            start_time = time.time()
            reset_circles()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                pygame.event.clear()
                if event.key == pygame.K_a:
                    highlight_screen(leftRect, 0)
                if event.key == pygame.K_d:
                    highlight_screen(rightRect, 1)

                print("time taken: " + str(time.time() - start_time))

                interval = random.randint(3000, 5000)
                start_time = time.time()

        pygame.display.flip()

    pygame.quit()
    exit()



