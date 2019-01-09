import random
import math
def get_treasure_pos():
    q = random.randint(1,6)

    if (q > 3):
        offset = 7*(q-4)
        yoffset = 4
    else:
        offset = 7*(q-1)
        yoffset = 0

    pos = random.randint(0,31)

    xpos = pos % 8

    ypos = math.floor((pos - xpos)/8)

    return (1 + offset + xpos, 1 + yoffset + ypos)


def load_next_level(fitness, level, done, counter, index, closest_dist):

    (x,y) = get_treasure_pos()
    while ((x,y) == player.current_pos or level[y][x] == 1):
        (x, y) = get_treasure_pos()

    level[y][x] = 3

    fitness += 10
    counter = counters

    if enemies:
        for enemy in enemies:
            enemy.destroy()

        enemies.clear()

    update_maze(level, True)
    wn.update()

    closest_dist = player.distance(treasure.current_pos)

    return (fitness, level, done, counter, index, closest_dist)
