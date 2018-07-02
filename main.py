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


class Button(turtle.Turtle):

    def __init__(self, button_handler, shape):
        turtle.Turtle.__init__(self)
        self.speed(0)
        self.color("white")
        self.fillcolor("")
        self.penup()
        self.shape(shape)
        self.setheading(90)
        self.onclick(self.get_clicked)
        self.is_selected = False
        self.button_handler = button_handler
        self.button_type = "test"

    def get_clicked(self, x, y):
            print(x, y)
            if self.button_type == "wall_button":
                self.button_handler.switch_wall_button_focus(self)
            elif self.button_type =="grid_button":
                self.button_handler.switch_grid_button_focus(self)


class Grid_Button(Button):

    def __init__(self, button_handler, shape, button_type):
        super().__init__(button_handler, shape)
        self.button_type = button_type


class Wall_Button(Button):

    def __init__(self, button_handler, shape, image):
        super().__init__(button_handler, shape)
        self.image = image
        self.button_type = "wall_button"


class Button_Handler():

    def __init__(self):

        self.wall_button_list = []
        self.button_image_list = []
        self.active_grid = []
        self.active_row = -340
        self.active_column = -120

        self.vert_button_image = Wall_Button_Image("vertical_wall", (-300, 65), "vert")
        self.right_button_image = Wall_Button_Image("right_lean_wall", (-315, -15), "roof")
        self.left_button_image = Wall_Button_Image("left_lean_wall", (-285, -95), "floor")
        self.button_image_list.append(self.vert_button_image)
        self.button_image_list.append(self.right_button_image)
        self.button_image_list.append(self.left_button_image)

    def create_buttons(self):
        # wall buttons
        for image in self.button_image_list:
            image.find_center()
            wall_button = Wall_Button(self, "wall_selector", image)
            wall_button.setposition(image.center_x, image.center_y)
            self.wall_button_list.append(wall_button)

        # left grid buttons
        for _ in range(4):
            grid_button = Grid_Button(self, "grid_selector", button_type="grid_button")
            grid_button.setposition(self.active_column, self.active_row)
            self.active_grid.append(grid_button)
            self.active_column += 30

    def switch_wall_button_focus(self, selected_button):
        for button in self.wall_button_list:
            if button == selected_button:
                button.image.color("green")
                button.pencolor("green")
                button.is_selected = True
            else:
                button.image.color("white")
                button.pencolor("white")
                button.is_selected = False

    def switch_grid_button_focus(self, selected_button):

        for button in self.active_grid:
            if button == selected_button:
                button.pencolor("green")
                button.is_selected = True
            else:
                button.pencolor("white")
                button.is_selected = False


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
        self.shape = shape
        self.wall_type = wall_type

        if self.shape == "right_lean_wall":
            self.slope = 4/3
        elif self.shape == "left_lean_wall":
            self.slope = -4/3
        else:
            self.slope = None


class Wall_Button_Image(Wall_Section):

    def __init__(self, shape, position, wall_type):
        super().__init__(shape, position, wall_type)
        self.is_selected = False

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

    test_click_radius = Button(button_handler, "wall_selector")

    turtle.listen()
    turtle.onkey(game.end_game, "p")

    while game.window_lives:
        time.sleep(1.0/60)
        game.window.update()

if __name__ == "__main__":

    main()

    turtle.exitonclick()