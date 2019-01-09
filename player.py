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
