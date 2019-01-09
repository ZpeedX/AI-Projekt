import turtle
import math
import random
import neat

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
