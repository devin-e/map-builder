"""Map Builder for Sky Turtle game"""

import turtle
import time



class Game():

    def __init__(self):
        self.window = turtle.Screen()

        # border pieces
        self.window.register_shape("vertical_wall", ((0, 0), (1, 0), (1, 40), (0, 40)))
        self.window.register_shape("right_lean_wall", ((0, 0), (1, 0), (31, 40), (30, 40)))
        self.window.register_shape("left_lean_wall", ((1, 0), (0, 0), (-30, 40), (-29, 40)))

    def new_game(self):
        turtle.resetscreen()
        turtle.clearscreen()

    def draw_screen(self):
        self.window.bgcolor("black")
        self.window.setup(800, 700)
        self.window.tracer(0, 0)
        self.window.colormode(255)
        self.window_lives = True

    def end_game(self):
        self.window.bgcolor("blue")
        self.window_lives = False


class Button_Handler():

    def __init__(self):
        self.button_list = []
        self.border_pen = turtle.Turtle()
        self.border_pen.speed(0)
        self.border_pen.hideturtle()
        self.border_pen.penup()
        self.border_pen.color((100, 100, 100))

    def create_buttons(self):
        self.vert_button = Wall_Section("vertical_wall", (-300, 65), "vert")
        self.right_button = Wall_Section("right_lean_wall", (-315, -15), "roof")
        self.left_button = Wall_Section("left_lean_wall", (-285, -95), "floor")
        self.button_list.append(self.vert_button)
        self.button_list.append(self.right_button)
        self.button_list.append(self.left_button)

        for button in self.button_list:
            button.find_center()
            self.draw_button_border(button)

    def draw_button_border(self, button):
        self.border_pen.setposition(button.center_x - 20, button.center_y - 25)
        self.border_pen.pendown()
        for _ in range(2):
            self.border_pen.forward(40)
            self.border_pen.left(90)
            self.border_pen.forward(50)
            self.border_pen.left(90)
        self.border_pen.penup()


class Wall_Section(turtle.Turtle):

    def __init__(self, shape, position, type):
        turtle.Turtle.__init__(self)
        self.speed(0)
        self.hideturtle()
        self.penup()
        self.shape(shape)
        self.color("white")
        self.setheading(90)
        self.setposition(position)
        self.showturtle()
        self.shape = shape
        self.type = type

        if self.shape == "right_lean_wall":
            self.slope = 4/3
        elif self.shape == "left_lean_wall":
            self.slope = -4/3
        else:
            self.slope = None

    def find_center(self):
        self.center_y = self.ycor() + 20

        if self.shape == "right_lean_wall":
            self.center_x = self.xcor() + 15
        elif self.shape == "left_lean_wall":
            self.center_x = self.xcor() - 15
        else:
            self.center_x = self.xcor()


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