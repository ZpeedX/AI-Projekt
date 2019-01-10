import turtle
import math
import random
import neat
import time
import numpy as np
import pickle
import player
import treasure
import pen
import levels

#Initialize a window switch the game will run in
wn = turtle.Screen()
wn.bgcolor("black")
wn.title("A Maze Game")

#The window is 700x700 pixles
wn.setup(700,700)
wn.tracer(0)


#An array which contains every created level
levels = levels.levels

#Randomize a new position where a treasure can reside
#Returns (X,Y) coordinates
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

#A function to check if the input is either BLOCKED or FREE
def whatIsNext(num):
    if num == 1:
        return 0
    if num == 0:
        return 1
    if num == 3:
        return 1
    if num == 4:
        return 0

#Check if the input parameter is positive or negative
#If the input parameter is positive return 1
#Else return 0
def sign(num):
    if num > 0:
        return 1
    else:
        return 0


#Amount of total moves a player can make
counters = 25

#Select a level from the levels array
level_select = 5

#Reinitialize the game map with from the given level array
def update_maze(level, first_setup=False):
    #Clear everything from the user screen
    pen.clearstamps()

    for y in range(len(level)):
        for x in range(len(level[y])):
            #Get the character at each x,y coordinate
            #NOTE the order of y and x in the next line
            character = level[y][x]
            #Calculate the screen x, y coordinates
            screen_x = -288 + (x*24)
            screen_y = 288 - (y*24)

            #Check if it's an 1 (representing a wall/obstacle)
            if character == 1:
                pen.goto(screen_x, screen_y)
                pen.stamp()
            #Check if it's a 2 (representing the player)
            if character == 2:
                player.goto(screen_x, screen_y)
                player.current_pos = (x,y)

            #Check if it's a 3 (representing the player)
            if character == 3:
                treasure.goto(screen_x, screen_y)

                if first_setup == True:
                    treasure.current_pos = (x,y)


#Create new a pen object. The object is used to draw the game walls/obstacles
pen = pen.Pen()

#Create new a player object. The object tracks players current position
player = player.Player()

#Create new a treasure object. The object tracks treasures current position
treasure = treasure.Treasure()

#A function to load a new treasure when the player reaches the current treasure
def generate_treasure(fitness, level, done, closest_dist):
    (x,y) = get_treasure_pos()

    #Check if the new treasure position is not occupied by any other obstacles.
    while ((x,y) == player.current_pos or level[y][x] == 1):
        (x, y) = get_treasure_pos()

    level[y][x] = 3

    #Add 10 points to the genomes fitness (Rewarded)
    fitness += 10


    #The function is used to update the map with the new treasure position
    update_maze(level, True)
    wn.update()

    #Get the distance between the player and the new treasure
    closest_dist = player.distance(treasure.current_pos)

    return (fitness, level, done, closest_dist)


#Main function which trains the Neural network
def eval_genomes(genomes, config):
    global level_select

    #Let every genome play the game
    for genome_id, genome in genomes:
        level = np.array(levels[level_select])

        net = neat.nn.recurrent.RecurrentNetwork.create(genome, config)


        update_maze(level, True)
        wn.update()

        #Get the distance between the player and the treasure
        closest_dist = player.distance(treasure.current_pos)

        #Turn off screen updates
        wn.tracer(0)

        #Used to count amount of fitness in a game run
        fitness_current = 0

        #Used to check amount of steps the player has used
        counter = 0

        max_counter = counters

        done = False

        while not done:

            (px, py) = player.current_pos
            (tx, ty) = treasure.current_pos

            #Get 8 inputs to feed to the neural network
            #Every input contains a 1 or 0
            #1 = Yes
            #0 = No

            #Input 1 - is it clear to the left?
            left = whatIsNext(level[py][px - 1])
            #Input 2 - is it clear to the right?
            right = whatIsNext(level[py][px + 1])
            #Input 3 - is it clear up?
            up = whatIsNext(level[py + 1][px])
            #Input 4 - is it clear down?
            down = whatIsNext(level[py - 1][px])

            #Input 5 - is the treasure to the left?
            leftG = sign(px - tx)
            #Input 6 - is the treasure to the right?
            rightG = sign(tx - px)
            #Input 7 - is the treasure up?
            upG = sign(py - ty)
            #Input 8 - is the treasure down?
            downG = sign(ty - py)

            #Add the inputs into the neural network
            nnOutput = net.activate([left, up, right, down, leftG, upG, rightG, downG])

            #Get the output back from the neural network
            #The output decides is the next move which the play will take
            done = player.next_move(nnOutput.index(max(nnOutput)), level)

            if done:
                break

            #Reload the map with new values
            update_maze(level)
            wn.update()

            current_dist = player.distance(treasure.current_pos)

            #Check if the player has come closer to the treasure
            #If true then add 1 point to the the genome fitness and the reset the counter
            if closest_dist > current_dist:
                closest_dist = current_dist
                fitness_current +=1
                counter = 0

            counter +=1

            #If the pplayer reached the treasure, spawn a new treasure
            if current_dist == 0:
                (fitness_current, level, done, closest_dist) = generate_treasure(fitness_current, level, done, closest_dist)
                counter = 0

            genome.fitness = fitness_current

            #If the player has reached the maximum amount of moves then end the game for the current genome
            #Or if the genome has exceeded it's fintess goal then end the training
            if done or counter == max_counter or fitness_current > 10000:
                done = True

        genome.fitness = fitness_current



#Load the configuration on the neural network.
#The configuration is located in the 'config-feedforward' file
config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     './config-feedforward')


#Restore the population from a checkpoint where the training continues
#p = neat.checkpoint.Checkpointer.restore_checkpoint("neat-checkpoint-good-0")

#Create the population, which is the top-level object for a NEAT run
p = neat.Population(config)

#Add a stdout reporter to show progress in the terminal.
p.add_reporter(neat.StdOutReporter(True))
stats = neat.StatisticsReporter()
p.add_reporter(stats)

#Create a new checkpoint when the neural network goes to the next generation
p.add_reporter(neat.Checkpointer(1))

#Start the training phase. When the training phase is over, the function returns the winning genome
winner = p.run(eval_genomes)

#Save the winning genome in a file
with open('winner.pkl', 'wb') as output:
    pickle.dump(winner, output, 1)
