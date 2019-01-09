import turtle
import math
import random
import neat
import time
import numpy as np
import pickle
import player
import treasure
import enemy
import pen

wn = turtle.Screen()
wn.bgcolor("black")
wn.title("A Maze Game")
wn.setup(700,700)
wn.tracer(0)


# 0 - free
# 1 - wall
# 2 - player
# 3 - treasure
# 4 - enemy
levels = []

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

levels.append([
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
])

levels.append([
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,3,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
])


levels.append([
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,1,0,0,1,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,2,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,3,0,1],
[1,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
])


levels.append([
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,3,1],
[1,0,0,0,0,1,0,2,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,1,0,0,0,0,1],
[1,0,0,1,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,1,0,0,1,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
])

counters = 10

end = len(levels)
#end = 4

#[1,0,0,0] - go_right
#[0,1,0,0] - go_down
#[0,0,1,0] - go_up
#[0,0,0,1] - go_left
def check_inputs(input):
    in0 = input[0]
    in1 = input[1]
    in2 = input[2]
    in3 = input[3]
    sum = 0

    if (in0 == 1):
        sum +=1
    if (in1 == 1):
        sum +=1
    if (in2 == 1):
        sum +=1
    if (in3 == 1):
        sum +=1

    return sum == 1

def whatIsNext(num):
    if num == 1:
        return 0
    if num == 0:
        return 1
    if num == 3:
        return 1
    if num == 4:
        return 0

def sign(num):
    if num > 0:
        return 1
    else:
        return 0


def update_maze(level, first_setup=False):
    pen.clearstamps()
    for y in range(len(level)):
        for x in range(len(level[y])):
            #Get the character at each x,y coordinate
            #NOTE the order of y and x in the next line
            character = level[y][x]
            #Calculate the screen x, y coordinates
            screen_x = -288 + (x*24)
            screen_y = 288 - (y*24)

            #Check if it's an X (representing a wall)
            if character == 1:
                pen.goto(screen_x, screen_y)
                pen.stamp()
            #Check if it's a P (representing the player)
            if character == 2:
                player.goto(screen_x, screen_y)
                player.current_pos = (x,y)

            #Check if it's a T (representing the player)
            if character == 3:
                treasure.goto(screen_x, screen_y)

                if first_setup == True:
                    treasure.current_pos = (x,y)

            #Check if it's an E (representing enemy)
            if character == 4:
                if first_setup == True:
                    enemies.append(Enemy(x,y))

                for enemy in enemies:
                    if enemy.current_pos[0] == x and enemy.current_pos[1] == y:
                        enemy.goto(screen_x, screen_y)



pen = pen.Pen()
player = player.Player()
treasure = treasure.Treasure()
enemies = []
config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     './config-feedforward')

with open('winner.pkl', 'rb') as file:
    genome = pickle.load(file)

index = 0
level = np.array(levels[index])

net = neat.nn.recurrent.RecurrentNetwork.create(genome, config)

if enemies:
    for enemy in enemies:
        enemy.destroy()

    enemies.clear()

update_maze(level, True)
wn.update()

closest_dist = player.distance(treasure.current_pos)
#Turn off screen updates
wn.tracer(0)

current_max_fitness = 0
fitness_current = 0
counter = 0
max_counter = counters
closest_dist = player.distance(treasure.current_pos)


done = False

frame = 0
while not done:

    (px, py) = player.current_pos
    (tx, ty) = treasure.current_pos
    left = whatIsNext(level[py][px - 1])
    right = whatIsNext(level[py][px + 1])
    up = whatIsNext(level[py + 1][px])
    down = whatIsNext(level[py - 1][px])


    leftG = sign(px - tx)
    rightG = sign(tx - px)
    upG = sign(py - ty)
    downG = sign(ty - py)

    (width, height) = player.dist(treasure.current_pos)

    nnOutput = net.activate([left, up, right, down, leftG, upG, rightG, downG])
    done = player.next_move(nnOutput.index(max(nnOutput)), level)


    if done:
        break

    if enemies:
        for enemy in enemies:
            done = enemy.move(level)

            if done == True:
                break

    if done:
        break

    update_maze(level)
    wn.update()

    current_dist = player.distance(treasure.current_pos)
    if closest_dist > current_dist:
        closest_dist = current_dist
        fitness_current +=1
        counter = 0

    counter +=1

    if current_dist == 0:
        (fitness_current, level, done, max_counter, index, closest_dist) = load_next_level(fitness_current, level, done, max_counter, index, closest_dist)
        counter = 0

    genome.fitness = fitness_current

    if done or counter == max_counter or fitness_current > 10000:
        done = True
        # print(genome_id, fitness_current)

genome.fitness = fitness_current
