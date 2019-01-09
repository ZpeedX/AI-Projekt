import turtle
import math
import random
import neat

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
