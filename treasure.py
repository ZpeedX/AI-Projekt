import turtle
import math
import random
import neat

#Treasure class representing a treasure in the game map
class Treasure(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("circle")
        self.color("gold")
        self.penup()
        self.speed(0)
        self.current_pos = (0,0)

    #Remove the treasure from the game map
    def destroy(self):
        self.clear()
        self.hideturtle()
