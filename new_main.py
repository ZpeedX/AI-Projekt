import turtle
import math
import random
import neat

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
        self.gold = 0
        self.lives = 3
        current_pos = (1,3)

        def next_move(input, level):
            if input == (0,0):
            elif



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
