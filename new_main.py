import turtle
import math
import random
import neat
import time
import numpy as np
import pickle

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


levels.append([
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,1],
[1,0,0,0,2,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,3,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
])

levels.append([
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,1,0,3,1],
[1,0,0,1,0,0,1,0,1,0,0,1,0,0,1,0,0,1,0,1,0,1,1,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1],
[1,2,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,1,0,0,1,0,1,0,0,1,0,0,1,0,0,1,0,1,0,1,1,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,1,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
])

levels.append([
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,1,1,1,1,0,0,1,1,0,0,0,1,1,0,0,1,1,1,1,1,0,0,1],
[1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1],
[1,2,0,0,0,0,1,1,1,1,1,0,0,0,1,1,1,1,1,1,0,0,0,3,0,1],
[1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1],
[1,0,0,1,1,1,1,0,0,1,1,0,0,0,1,1,0,0,1,1,1,1,1,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
])

levels.append([
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1],
[1,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,1],
[1,0,0,0,0,0,0,0,1,0,0,0,0,3,0,0,0,1,0,0,0,0,0,0,0,1],
[1,0,0,2,0,0,0,0,1,0,0,0,1,1,0,0,0,1,0,0,0,0,0,0,0,1],
[1,0,0,1,1,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,1,1,0,0,1],
[1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
])

counters = 25

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


class Player(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("blue")
        self.penup()
        self.speed(0)
        self.lives = 3
        self.current_pos = (1,1)
        self.points = 0

    def next_move(self, input, level):
        self_x = self.current_pos[0]
        self_y = self.current_pos[1]
        end = False


        if input == 2:
            end = self.is_blocked((self_x+1, self_y), level)
        elif input == 3:
            end = self.is_blocked((self_x, self_y+1), level)
        elif input == 1:
            end = self.is_blocked((self_x, self_y-1), level)
        elif input == 0:
            end = self.is_blocked((self_x-1, self_y), level)

        return end


    def is_blocked(self, next_pos, level):
        if level[next_pos[1]][next_pos[0]] == 0:
            level[self.current_pos[1]][self.current_pos[0]] = 0
            level[next_pos[1]][next_pos[0]] = 2
            self.current_pos = next_pos

        elif level[next_pos[1]][next_pos[0]] == 3:
            level[self.current_pos[1]][self.current_pos[0]] = 0
            level[next_pos[1]][next_pos[0]] = 2
            self.current_pos = next_pos

        elif level[next_pos[1]][next_pos[0]] == 1:
            return True

        elif level[next_pos[1]][next_pos[0]] == 4:
            return True

        return False

    def distance(self, other):
        a = self.current_pos[0]-other[0]
        b = self.current_pos[1]-other[1]
        distance = math.sqrt((a**2)+(b**2))

        return distance

    def dist(self, other):
        width = self.current_pos[0]-other[0]
        height = self.current_pos[1]-other[1]

        return (width, height)
#Create Tresure
class Treasure(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("circle")
        self.color("gold")
        self.penup()
        self.speed(0)
        self.current_pos = (0,0)

    def destroy(self):
        self.clear()
        self.hideturtle()

class Enemy(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("red")
        self.penup()
        self.speed(0)
        self.current_pos = (x,y)
        self.next = "down"

    def move(self, level):
        self_x = self.current_pos[0]
        self_y = self.current_pos[1]
        end = False
        if self.next == "down":
            end = self.next_move((self_x, self_y+1), level)
        elif self.next == "up":
            end = self.next_move((self_x, self_y-1), level)

        return end

    def next_move(self, next_pos, level):
        if level[next_pos[1]][next_pos[0]] == 0:
            level[self.current_pos[1]][self.current_pos[0]] = 0
            level[next_pos[1]][next_pos[0]] = 4
            self.current_pos = next_pos
        elif level[next_pos[1]][next_pos[0]] == 2:
            return True

        elif level[next_pos[1]][next_pos[0]] == 1:
            if self.next == "down":
                self.next = "up"
            else:
                self.next = "down"


        return False

    def destroy(self):
        self.clear()
        self.hideturtle()


#Create Pen
class Pen(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("white")
        self.penup()
        self.speed(0)

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



pen = Pen()
player = Player()
treasure = Treasure()
enemies = []

def load_next_level(fitness, level, done, counter, index, closest_dist):
    #q = random.randint(1,100)
    #if (q == 42):
    #    s = index
    #    while (s == index):
    #        s = random.randint(0, len(levels)-1)
        #index = 2
    #    level = np.array(levels[index])

    #else:
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



def eval_genomes(genomes, config):
    global enemies
    for genome_id, genome in genomes:
        index = 3
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
            #time.sleep(0.1)
            #print(map)

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

            #print([left, up, right, down, leftG, upG, rightG, downG])
            nnOutput = net.activate([left, up, right, down, leftG, upG, rightG, downG])

            #print(level.flatten())
            #print(genome_id, nnOutput)
            #print(nnOutput)

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
                #index += 1
                (fitness_current, level, done, max_counter, index, closest_dist) = load_next_level(fitness_current, level, done, max_counter, index, closest_dist)
                counter = 0

            genome.fitness = fitness_current

            if done or counter == max_counter or fitness_current > 10000:
                done = True
                # print(genome_id, fitness_current)

        genome.fitness = fitness_current




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

config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     './config-feedforward')

p = neat.checkpoint.Checkpointer.restore_checkpoint("neat-checkpoint-good-1")
#p = neat.Population(config)

p.add_reporter(neat.StdOutReporter(True))
stats = neat.StatisticsReporter()
p.add_reporter(stats)
p.add_reporter(neat.Checkpointer(1))

winner = p.run(eval_genomes)

with open('winner.pkl', 'wb') as output:
    pickle.dump(winner, output, 1)
