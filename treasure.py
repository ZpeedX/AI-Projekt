import turtle
import math
import random
import neat

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
