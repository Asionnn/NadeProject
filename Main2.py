import math
import pygame
import time
import random
from datetime import datetime
import csv

# structure for data = (trial #, side, correct?, reaction time, unix time)
data = []
circle_list = []
correct_circle_location = []
fields = ['Trial #', 'Side', 'Correct?', 'Reaction Time', 'UNIX Time Stamp']
black = [160, 160, 160]

date = datetime.today().strftime('%y%m%d%H%M%S')
filename = 'Data' + date + '.csv'

circles = 0
trial_count = 1
random_circle_index = 0

started_trials = False
runOnce = True
button_pressed = False


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
        num_generated += 1
        circles = 0
        runOnce = True


def euclidean_distance(x1, y1, x2, y2):
    return math.hypot((x1 - x2), (y1 - y2))


def draw_rect_alpha(surface, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)


def draw_selected_circles():
    for x, y, r in circle_list[random_circle_index]:
        pygame.draw.circle(window, (0, 0, 0), (round(x), round(y)), int(r), 2)


def draw_circles():
    global random_circle_index
    random_circle_index = random.randint(0, 100)
    for x, y, r in circle_list[random_circle_index]:
        pygame.draw.circle(window, (0, 0, 0), (round(x), round(y)), int(r), 2)
    pygame.display.flip()


def reset_circles():
    window.fill(black)
    draw_circles()


def highlight_screen(rect):
    global correct_circle_location, random_circle_index
    draw_rect_alpha(window, (100, 100, 100), rect)
    pygame.display.update()
    pygame.time.wait(100)
    draw_rect_alpha(window, (160, 160, 160), rect)
    draw_selected_circles()


def record_data(side, duration):
    global correct_circle_location, random_circle_index, interval, trial_count
    print("correct") if correct_circle_location[random_circle_index] == side else print("wrong")

    str_side = "Left" if side == 0 else "Right"
    correct = correct_circle_location[random_circle_index] == side

    data.append((trial_count, str_side, correct, duration, time.time()))
    trial_count += 1
    # print(data)


if __name__ == "__main__":
    run = True

    # Initialize pygame
    pygame.init()
    window = pygame.display.set_mode([1024, 768])
    generate_circle_lists()
    pygame.display.set_caption('SuRT Clone')
    font50 = pygame.font.SysFont(None, 50)
    window.fill(black)

    # Draw opaque rectangles for left and right sides
    leftRect = pygame.draw.rect(window, (160, 160, 160), (0, 0, 512, 768), 1)
    rightRect = pygame.draw.rect(window, (160, 160, 160), (512, 0, 512, 768), 1)

    # Render circles and set up interval
    if started_trials:
        draw_circles()
    interval = random.randint(10000, 15000)

    # Keep track of the game time
    game_start_time = time.time()
    start_time = time.time()

    # start button
    start_button = pygame.Rect(462, 359, 100, 50)
    pygame.draw.rect(window, [0, 255, 0], start_button)

    while run:
        if (time.time() - start_time) * 1000 >= interval and started_trials:

            print("interval: " + str(interval))
            print("time: " + str(time.time() - start_time))

            data.append((trial_count, "N/A", False, "N/A", time.time()))
            trial_count += 1
            interval = random.randint(10000, 15000)
            start_time = time.time()
            reset_circles()
            button_pressed = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                with open('./' + filename, 'w') as csvfile:
                    csvwriter = csv.writer(csvfile)
                    csvwriter.writerow(fields)
                    csvwriter.writerows(data)
                    csvfile.close()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not started_trials:
                window.fill(black)
                pygame.display.flip()
                started_trials = True
                start_time = time.time()
                draw_circles()

            if event.type == pygame.KEYDOWN and not button_pressed and started_trials:
                pygame.event.clear()
                if event.key == pygame.K_a:
                    button_pressed = True
                    record_data(0, time.time() - start_time)
                    highlight_screen(leftRect)
                if event.key == pygame.K_d:
                    button_pressed = True
                    record_data(1, time.time() - start_time)
                    highlight_screen(rightRect)

                interval = random.randint(10000, 15000)
                start_time = time.time()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if start_button.collidepoint(mouse_pos) and not started_trials:
                    window.fill(black)
                    pygame.display.flip()
                    started_trials = True
                    start_time = time.time()
                    draw_circles()

        pygame.display.flip()

    pygame.quit()
    exit()



