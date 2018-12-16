import turtle
import math
import random
import neat
import time
import numpy as np

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

level_1 = [
[1,1,1,1,1,1,1,1,1,1,1,1],
[1,2,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,3,1],
[1,1,1,1,1,1,1,1,1,1,1,1]
]

#(0,0) - go_left
#(0,1) - go_right
#(1,0) - go_up
#(1,1) - go_down

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

        if input[0] == 1:
            self.is_blocked((self_x-1, self_y), level)
        elif input[1] == 1:
            self.is_blocked((self_x+1, self_y), level)
        elif input[2] == 1:
            self.is_blocked((self_x, self_y+1), level)
        elif input[3] == 1:
            self.is_blocked((self_x, self_y-1), level)


    def is_blocked(self, next_pos, level):
        if level[next_pos[1]][next_pos[0]] == 0:
            level[self.current_pos[1]][self.current_pos[0]] = 0
            level[next_pos[1]][next_pos[0]] = 2
            self.current_pos = next_pos
        elif level[next_pos[1]][next_pos[0]] == 3:
            level[self.current_pos[1]][self.current_pos[0]] = 0
            level[next_pos[1]][next_pos[0]] = 2
            self.current_pos = next_pos

    def distance(self, other):
        a = self.current_pos[0]-other[0]
        b = self.current_pos[1]-other[1]
        distance = math.sqrt((a**2)+(b**2))

        return distance

#Create Tresure
class Treasure(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("circle")
        self.color("gold")
        self.penup()
        self.speed(0)
        self.gold = 100
        self.current_pos = (0,0)

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

def setup_maze(level):
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
                treasure.current_pos = (x,y)
            #Check if it's an E (representing enemy)
            #if character == "E":
                #enemies.append(Enemy(screen_x, screen_y))


def resetup_maze(level):
    pen.clearstamps()
    setup_maze(level)

pen = Pen()
player = Player()
treasure = Treasure()

def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        level = np.array(level_1)
        net = neat.nn.recurrent.RecurrentNetwork.create(genome, config)

        setup_maze(level)
        closest_dist = player.distance(treasure.current_pos)
        #Turn off screen updates
        wn.tracer(0)

        current_max_fitness = 0
        fitness_current = 0
        frame = 0
        counter = 0
        closest_dist = player.distance(treasure.current_pos)

        done = False

        while not done:
            frame += 1
            nnOutput = net.activate(level.flat)
            player.next_move(nnOutput, level)
            resetup_maze(level)
            wn.update()

            current_dist = player.distance(treasure.current_pos)
            if closest_dist > current_dist:
                closest_dist = current_dist
                fitness_current +=1

            if current_dist == 0:
                done = True
                fitness_current +=10000

            if fitness_current > current_max_fitness:
                current_max_fitness = fitness_current
                counter = 0
            else:
                counter += 1

            if done or counter == 20:
                done = True
                print(genome_id, fitness_current)

            genome.fitness = fitness_current
            #print(nnOutput)



config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     './config-feedforward')
p = neat.Population(config)

winner = p.run(eval_genomes)
