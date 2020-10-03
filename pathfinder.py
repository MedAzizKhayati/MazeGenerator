import pygame
import random
import time

pygame.init()
width = 1900
height = 1000
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Sorting")
size = 20
array = []
started = False
start = []
finish = []
grid = []
paths = []
startmaze = False
sleeptime = 0.01
pathfound = False


def initialise():
    global started, startmaze, pathfound, start, array, finish, grid, paths
    array = []
    started = False
    start = []
    finish = []
    grid = []
    paths = []
    startmaze = False
    pathfound = False


def array_maker():
    for i in range(width // size):
        for j in range(height // size):
            array.append([])
            grid.append([])
            array[i].append([255, 255, 255])
            grid[i].append([1])


def setup(click, click2, mx, my):
    global start, finish, started, grid
    if click:
        if not len(start):
            array[mx // size][my // size] = [255, 0, 0]
            start = [mx // size, my // size]
            paths.append(start)
        elif not len(finish) and not ([mx // size, my // size] in [start]):
            array[mx // size][my // size] = [0, 255, 0]
            finish = [mx // size, my // size]
        elif start and finish and not ([mx // size, my // size] in [start, finish]):
            array[mx // size][my // size] = [0, 0, 0]
            grid[mx // size][my // size][0] = 0
    if click2:
        array[mx // size][my // size] = [255, 255, 255]
        grid[mx // size][my // size][0] = 1

    keys = pygame.key.get_pressed()
    if keys[pygame.K_s] and len(start) and len(finish):
        started = True


def QuickSort(arr):
    elements = len(arr)

    if elements < 2:
        return arr

    current_position = 0  # Position of the partitioning element

    for i in range(1, elements):  # Partitioning loop
        if grid[arr[i][0]][arr[i][1]][2] <= grid[arr[0][0]][arr[0][1]][2]:
            current_position += 1
            temp = arr[i]
            arr[i] = arr[current_position]
            arr[current_position] = temp

    temp = arr[0]
    arr[0] = arr[current_position]
    arr[current_position] = temp  # Brings pivot to it's appropriate position

    left = QuickSort(arr[0:current_position])  # Sorts the elements to the left of pivot
    right = QuickSort(arr[current_position + 1:elements])  # sorts the elements to the right of pivot

    arr = left + [arr[current_position]] + right  # Merging everything together

    return arr


def dijkstras_algorithm():
    global array, grid, paths, pathfound, limitsx, limitsy, step

    def give_neighbours(x, y):
        return [[x, y - 1], [x, y + 1], [x + 1, y], [x - 1, y]]

    if len(paths):
        if paths[0] == start:
            step = False
            limitsx = [-1, width // size]
            limitsy = [-1, height // size]
            pathfound = False
            paths = []
            neighbours = give_neighbours(start[0], start[1])
            for i in neighbours:
                x, y = i[0], i[1]
                if not x in limitsx and not y in limitsy:
                    if grid[x][y][0]:
                        paths.append(i)
                        grid[x][y].append(start)
                        grid[x][y].append(1)
                        array[x][y] = (0, 200, 255)
        neighbours = give_neighbours(paths[0][0], paths[0][1])
        if not pathfound:
            for i in neighbours:
                x, y = i[0], i[1]
                if not x in limitsx and not y in limitsy and grid[x][y][0] and i != grid[paths[0][0]][paths[0][1]][1]:
                    if len(grid[x][y]) > 1:
                        if paths[0][1] == y == grid[paths[0][0]][paths[0][1]][1][1] or paths[0][0] == x == \
                                grid[paths[0][0]][paths[0][1]][1][0]:
                            d = grid[paths[0][0]][paths[0][1]][2] + 1
                        else:
                            d = grid[paths[0][0]][paths[0][1]][2] + 1.1
                        if grid[x][y][2] > d:
                            grid[x][y][2] = d
                            grid[x][y][1] = [paths[0][0], paths[0][1]]
                    elif not i in paths:
                        paths.append(i)
                        grid[x][y].append(paths[0])
                        if paths[0][1] == y == grid[paths[0][0]][paths[0][1]][1][1] or paths[0][0] == x == \
                                grid[paths[0][0]][paths[0][1]][1][0]:
                            grid[x][y].append(grid[paths[0][0]][paths[0][1]][2] + 1)
                        else:
                            grid[x][y].append(grid[paths[0][0]][paths[0][1]][2] + 1.1)
                        array[x][y] = (0, 200, 255)
                    if i == finish:
                        array[x][y] = (0, 255, 0)
                        pathfound = True
            paths.pop(0)
            QuickSort(paths)
    if pathfound:
        if not step:
            paths = []
            current = grid[finish[0]][finish[1]][1]
            while current != start:
                paths.append(current)
                current = grid[current[0]][current[1]][1]
            step = True
            limitsx = len(paths)
        else:
            if limitsx > 0:
                limitsx -= 1
                array[paths[limitsx][0]][paths[limitsx][1]] = [255, 255, 40]


def greedy_best_first():
    global array, grid, paths, pathfound, limitsx, limitsy

    def give_neighbours(x, y):
        return [[x, y - 1], [x, y + 1], [x + 1, y], [x - 1, y]]
    if len(paths):
        if paths[0] == start:
            limitsx = [-1, width // size]
            limitsy = [-1, height // size]
            pathfound = False
            grid[start[0]][start[1]].append([-1, -1])
            grid[start[0]][start[1]].append(abs(finish[0] - start[0]) + abs(finish[1] - start[1]))
        neighbours = give_neighbours(paths[0][0], paths[0][1])
        current = paths[0]
        if not pathfound:
            for i in neighbours:
                x, y = i[0], i[1]
                if not x in limitsx and not y in limitsy and grid[x][y][0] and i != grid[current[0]][current[1]][1]:
                    if len(grid[x][y]) == 1:
                        d = abs(finish[0] - x) + abs(finish[1] - y)
                        put = False
                        for j in paths:
                            if d <= grid[j[0]][j[1]][2]:
                                paths.insert(paths.index(j), i)
                                put = True
                                break
                        if not put:
                            paths.append(i)
                        grid[x][y].append(current)
                        grid[x][y].append(d)
                        array[x][y] = (0, 200, 255)
                    if i == finish:
                        array[x][y] = (0, 255, 0)
                        pathfound = True
            paths.pop(paths.index(current))
        if pathfound:
            current = grid[finish[0]][finish[1]][1]
            while current != start:
                array[current[0]][current[1]] = [255, 255, 40]
                current = grid[current[0]][current[1]][1]


def recursive_division():
    global startmaze

    def algorithme(startx, endx, starty, endy):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        if endx - startx >= endy - starty:
            holes = 0
            for i in range(startx + 1, endx):
                if grid[i][starty - 1][0]:
                    holes += 1
                if grid[i][endy + 1][0]:
                    holes += 1
            if (not holes and endx - startx > 1) or (holes == 1 and endx - startx > 2) or (
                    holes > 1 and endx - startx > 3):
                while True:
                    vertical = random.randint(startx + 1, endx - 1)
                    if not grid[vertical][starty - 1][0] and not grid[vertical][endy + 1][0]:
                        break
            else:
                vertical = 0
            holesy = random.randint(starty, endy)
            if vertical > 0:
                for i in range(starty, endy + 1):
                    if i != holesy:
                        time.sleep(sleeptime)
                        array[vertical][i] = [0, 0, 0]
                        grid[vertical][i][0] = 0
                        pygame.draw.rect(win, array[vertical][i], [vertical * size, i * size, size, size])
                        pygame.display.update()
                if vertical - startx > 1:
                    algorithme(startx, vertical - 1, starty, endy)
                if endx - vertical > 1:
                    algorithme(vertical + 1, endx, starty, endy)
        else:
            holes = 0
            for i in range(starty + 1, endy):
                if grid[startx - 1][i][0]:
                    holes += 1
                if grid[endx + 1][i][0]:
                    holes += 1
            blocks = endy - starty
            if (not holes and blocks > 1) or (holes == 1 and blocks > 2) or (holes > 1 and blocks > 3):
                while True:
                    horizontal = random.randint(starty + 1, endy - 1)
                    if not grid[startx - 1][horizontal][0] and not grid[endx + 1][horizontal][0]:
                        break
            else:
                horizontal = 0
            if horizontal:
                holesx = random.randint(startx, endx)
                for i in range(startx, endx + 1):
                    if i != holesx:
                        time.sleep(sleeptime)
                        array[i][horizontal] = [0, 0, 0]
                        grid[i][horizontal][0] = 0
                        pygame.draw.rect(win, array[i][horizontal], [i * size, horizontal * size, size, size])
                        pygame.display.update()
                if horizontal - starty > 1:
                    algorithme(startx, endx, starty, horizontal - 1)
                if endy - horizontal > 1:
                    algorithme(startx, endx, horizontal + 1, endy)

    if not startmaze:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_m]:
            startmaze = 1
    elif startmaze == 1:
        for i in range(width // size):
            time.sleep(sleeptime)
            array[i][0] = [0, 0, 0]
            array[i][height // size - 1] = [0, 0, 0]
            grid[i][0][0] = 0
            grid[i][height // size - 1][0] = 0
            pygame.draw.rect(win, [0, 0, 0], [i * size, 0, size, size])
            pygame.draw.rect(win, [0, 0, 0], [i * size, (height // size - 1) * size, size, size])
            pygame.display.update()
        for i in range(height // size):
            time.sleep(sleeptime)
            array[0][i] = [0, 0, 0]
            array[width // size - 1][i] = [0, 0, 0]
            grid[0][i][0] = 0
            grid[width // size - 1][i][0] = 0
            pygame.draw.rect(win, [0, 0, 0], [0, i * size, size, size])
            pygame.draw.rect(win, [0, 0, 0], [(width // size - 1) * size, i * size, size, size])
            pygame.display.update()
        algorithme(1, width // size - 2, 1, height // size - 2)
        startmaze = 2


def main():
    global started, array, pathfound
    run = True
    clock = pygame.time.Clock()
    t1 = time.time()
    array_maker()
    mx, my = 0, 0
    click = False
    click2 = False
    while run:
        win.fill((255, 255, 255))
        # clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        if not started:
            setup(click, click2, mx, my)
        else:
            # dijkstras_algorithm()
            greedy_best_first()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            initialise()
            array_maker()
        click = click2 = False
        if pygame.mouse.get_pressed()[0]:
            click = True
        if pygame.mouse.get_pressed()[2]:
            click2 = True
        mx, my = pygame.mouse.get_pos()
        for i in range(0, width, size):
            pygame.draw.line(win, (200, 200, 255), [i, 0], [i, height], 1)
        for i in range(0, height, size):
            pygame.draw.line(win, (200, 200, 255), [0, i], [width, i], 1)
        for i in range(len(array)):
            for j in range(len(array[i])):
                if array[i][j] != [255, 255, 255]:
                    pygame.draw.rect(win, array[i][j], [i * size, j * size, size, size])
                    if array[i][j] != [0, 0, 0]:
                        pygame.draw.rect(win, (200, 200, 255), [i * size, j * size, size, size], 1)
        recursive_division()
        t2 = time.time()
        print(int(1 / (t2 - t1)))
        t1 = t2
        pygame.display.update()


main()
pygame.quit()
