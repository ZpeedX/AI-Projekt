import turtle
import math
import random
import neat

wn = turtle.Screen()
wn.bgcolor("black")
wn.title("A Maze Game")
wn.setup(700,700)
wn.tracer(0)

#Create Pen
class Pen(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("white")
        self.penup()
        self.speed(0)

#Create Player
class Player(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("blue")
        self.penup()
        self.speed(0)
        self.gold = 0
        self.lives = 3

    def go_up(self):
        self.calc_next_move(0, 24)

    def go_down(self):
        self.calc_next_move(0, -24)

    def go_left(self):
        self.calc_next_move(-24, 0)

    def go_right(self):
        self.calc_next_move(24, 0)

    def calc_next_move(self, xcor, ycor):
        xcor = self.xcor() + xcor
        ycor = self.ycor() + ycor

        if(xcor, ycor) not in walls:
            self.goto(xcor, ycor)

    def is_collision(self, other):
        a = self.xcor()-other.xcor()
        b = self.ycor()-other.ycor()
        distance = math.sqrt((a**2)+(b**2))

        if distance < 5:
            return True
        else:
            return False

    def is_close(self, other):
        a = self.xcor()-other.xcor()
        b = self.ycor()-other.ycor()
        distance = math.sqrt((a**2)+(b**2))

        return distance

#Create Tresure
class Treasure(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape("circle")
        self.color("gold")
        self.penup()
        self.speed(0)
        self.gold = 100
        self.goto(x,y)

    def destroy(self):
        self.clear()
        self.hideturtle()

#Create Enemy
class Enemy(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("red")
        self.penup()
        self.speed(0)
        self.gold = 25
        self.goto(x,y)
        self.direction = random.choice(["up", "down", "left", "right"])

    def move(self):
        if(self.direction == "up"):
            dx = 0
            dy = 24
        elif(self.direction == "down"):
            dx = 0
            dy = -24
        elif(self.direction == "left"):
            dx = -24
            dy = 0
        elif(self.direction == "right"):
            dx = 24
            dy = 0
        else:
            dx = 0
            dy = 0

        #Check if player is close
        #If so, in that direction
        if self.is_close(player):
            if player.xcor() < self.xcor():
                self.direction = "left"
            elif player.xcor() > self.xcor():
                self.direction = "right"
            elif player.ycor() < self.ycor():
                self.direction = "down"
            elif player.ycor() > self.ycor():
                self.direction = "up"

        #Calculate the spot to move to
        move_to_x = self.xcor() + dx
        move_to_y = self.ycor() + dy

        #Check if the space has a wall
        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)
        else:
            #Choose a different direction
            self.direction = random.choice(["up", "down", "left", "right"])

        #Set timer to move next time
        turtle.ontimer(self.move, t=random.randint(100, 300))

    def is_close(self, other):
        a = self.xcor()-other.xcor()
        b = self.ycor()-other.ycor()
        distance = math.sqrt((a**2)+(b**2))

        if distance < 75:
            return True
        else:
            return False

    def destroy(self):
        self.goto(2000,2000)
        self.hideturtle()

#Create levels list
levels = [""]

#Define first level
level_1 = [
"XXXXXXXXXXXXXXXXXXXXXXXXX",
"XP                     XX",
"X                      XX",
"X                      XX",
"X                     TXX",
"XXXXXXXXXXXXXXXXXXXXXXXXX"
]
level_2 = [
"XXXXXXXXXXXXXXXXXXXXXXXXX",
"XP                      X",
"X                      XX",
"X                      XX",
"X                     TXX",
"XXXXXXXXXXXXXXXXXXXXXXXXX"
]

#add tresures
treasures = []

#add enemies
enemies = []
#Add maze to mazes list
levels.append(level_1)
levels.append(level_2)

player_startX = 0
player_startY = 0
#Create Level Setup Function
def setup_maze(level):
    global player_startX
    global player_startY
    for y in range(len(level)):
        for x in range(len(level[y])):
            #Get the character at each x,y coordinate
            #NOTE the order of y and x in the next line
            character = level[y][x]
            #Calculate the screen x, y coordinates
            screen_x = -288 + (x*24)
            screen_y = 288 - (y*24)

            #Check if it's an X (representing a wall)
            if character == "X":
                pen.goto(screen_x, screen_y)
                pen.stamp()
                walls.append((screen_x, screen_y))
            #Check if it's a P (representing the player)
            if character == "P":
                player.goto(screen_x, screen_y)
                player_startX = screen_x
                player_startY = screen_y

            #Check if it's a T (representing the player)
            if character == "T":
                treasures.append(Treasure(screen_x, screen_y))
            #Check if it's an E (representing enemy)
            #if character == "E":
                #enemies.append(Enemy(screen_x, screen_y))

def resetup_maze(level):
    pen.clearstamps()
    walls.clear()
    treasures.clear()
    enemies.clear()
    setup_maze(level)


#Create class instance
pen = Pen()
player = Player()

#Create wall
walls = []

#Setup the level

setup_maze(levels[1])

#Keyboard Binding
turtle.listen()
turtle.onkeypress(player.go_left,"a")
turtle.onkeypress(player.go_right,"d")
turtle.onkeypress(player.go_up,"w")
turtle.onkeypress(player.go_down,"s")


#Turn off screen updates
wn.tracer(0)

#Start moving enemies
for enemy in enemies:
    turtle.ontimer(enemy.move, t=250)

def eval_genomes(genomes, config):
    return True

config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     'config-feedforward')

p = neat.Population(config)

#winner = p.run(eval_genomes)

#Main Game Loop
while True:
    #Check for player collision with treasures
    #Iterate through tresure list
    for treasure in treasures:
        if player.is_collision(treasure):
            player.gold += treasure.gold
            print("Player Gold: {}".format(player.gold))
            #Destroy the treasure
            treasure.destroy()
            #Remove the treasure from the treasures list
            treasures.remove(treasure)
            resetup_maze(levels[2])


    for enemy in enemies:
        if player.is_collision(enemy):
            if player.lives == 1:
                turtle.done()
            else:
                player.lives -= 1
                print("lives: {}".format(player.lives))
                player.goto(player_startX, player_startY)

    #Update screen
    wn.update()
