"""Map Builder for Sky Turtle game"""

import turtle
import time
from button_handler import Button_Handler



class Game():

    def __init__(self):
        self.window = turtle.Screen()

        # border pieces
        self.window.register_shape("vertical_wall", ((0, 0), (1, 0), (1, 40), (0, 40)))
        self.window.register_shape("right_lean_wall", ((0, 0), (1, 0), (31, 40), (30, 40)))
        self.window.register_shape("left_lean_wall", ((1, 0), (0, 0), (-30, 40), (-29, 40)))

        # button borders
        self.window.register_shape("wall_selector", ((-20, -25), (20, -25), (20, 25), (-20, 25)))
        self.window.register_shape("grid_selector", ((-5, -5), (5, -5), (5, 5), (-5, 5)))

    def new_game(self):
        turtle.resetscreen()
        turtle.clearscreen()

    def draw_screen(self):
        self.window.bgcolor("black")
        self.window.setup(800, 720)
        self.window.tracer(0, 0)
        self.window.colormode(255)
        self.window_lives = True

    def end_game(self):
        self.window.bgcolor("blue")
        self.window_lives = False


class Wall_Section(turtle.Turtle):

    def __init__(self, shape, position, wall_type):
        turtle.Turtle.__init__(self)
        self.speed(0)
        self.hideturtle()
        self.penup()
        self.shape(shape)
        self.color("white")
        self.setheading(90)
        self.setposition(position)
        self.showturtle()
        # self.shape = shape
        self.wall_type = wall_type

        if self.shape == "right_lean_wall":
            self.slope = 4/3
        elif self.shape == "left_lean_wall":
            self.slope = -4/3
        else:
            self.slope = None


class Grid(turtle.Turtle):

    def __init__(self):
        turtle.Turtle.__init__(self)
        self.hideturtle()
        self.speed(0)
        self.penup()
        self.color((100, 100, 100))

    def draw_grid(self):
        self.setposition(0, -340)
        self.setheading(90)
        self.pendown()
        self.forward(660)
        self.penup()
        self.setheading(0)
        self.setposition(-122, -340)
        self.pendown()
        self.forward(244)
        self.penup()
        self.setposition(-122, -300)
        for _ in range(17):
            for _ in range(9):
                self.pendown()
                self.forward(4)
                self.penup()
                self.forward(26)
            self.setposition(-122, self.ycor() + 40)

        self.setposition(-120, -342)
        self.setheading(90)
        for _ in range(9):
            for _ in range(18):
                self.pendown()
                self.forward(4)
                self.penup()
                self.forward(36)
            self.setposition(self.xcor() + 30, -342)


def main():
    game = Game()
    game.new_game()
    game.draw_screen()
    grid = Grid()
    grid.draw_grid()

    button_handler = Button_Handler()
    button_handler.create_buttons()

    turtle.listen()
    turtle.onkey(game.end_game, "p")

    while game.window_lives:
        time.sleep(1.0/60)
        game.window.update()

if __name__ == "__main__":

    main()

    turtle.exitonclick()