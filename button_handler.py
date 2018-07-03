import turtle



class Button_Handler():

    def __init__(self):

        self.wall_button_list = []
        self.button_image_list = []
        self.active_grid = []
        self.active_row = -340
        self.active_column = -120

        self.vert_button_image = Wall_Button_Image(shape = "vertical_wall", position = (-300, 65))
        self.right_button_image = Wall_Button_Image(shape = "right_lean_wall", position = (-315, -15))
        self.left_button_image = Wall_Button_Image(shape = "left_lean_wall", position = (-285, -95))
        self.button_image_list.append(self.vert_button_image)
        self.button_image_list.append(self.right_button_image)
        self.button_image_list.append(self.left_button_image)

    def create_buttons(self):
        # wall buttons
        for image in self.button_image_list:
            image.find_center()
            wall_button = Wall_Button(button_handler = self, shape = "wall_selector", image = image)
            wall_button.setposition(image.center_x, image.center_y)
            self.wall_button_list.append(wall_button)

        # left grid buttons
        for _ in range(4):
            grid_button = Grid_Button(button_handler = self, shape = "grid_selector", button_type = "grid_button")
            grid_button.setposition(self.active_column, self.active_row)
            self.active_grid.append(grid_button)
            self.active_column += 30

        # right grid buttons
        self.active_column += 30
        for _ in range(4):
            grid_button = Grid_Button(button_handler=self, shape="grid_selector", button_type = "grid_button")
            grid_button.setposition(self.active_column, self.active_row)
            self.active_grid.append(grid_button)
            self.active_column += 30

        self.build_button = Build_Button(button_handler = self, shape = "wall_selector")
        self.build_button.setposition(-300, -150)
        self.build_button.update_build_text(self.build_button.start_color)


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
            elif self.button_type == "grid_button":
                self.button_handler.switch_grid_button_focus(self)
            elif self.button_type == "build_button":
                # self.build()
                self.glow_green()


class Grid_Button(Button):

    def __init__(self, button_handler, shape, button_type):
        super().__init__(button_handler, shape)
        self.button_type = button_type


class Wall_Button(Button):

    def __init__(self, button_handler, shape, image):
        super().__init__(button_handler, shape)
        self.image = image
        self.button_type = "wall_button"


class Build_Button(Button):

    def __init__(self, button_handler, shape):
        super().__init__(button_handler, shape)
        self.setheading(0)
        self.start_color = (200, 50, 50)
        self.pencolor(self.start_color)
        self.pencil = turtle.Turtle()
        self.pencil.speed(0)
        self.pencil.hideturtle()
        self.pencil.penup()
        self.button_type = "build_button"
        self.onrelease(self.revert_to_red)

    def update_build_text(self, color):
        self.pencil.clear()
        self.pencil.pencolor(color)
        self.pencil.setposition(self.xcor() + 1, self.ycor() - 7)
        self.pencil.write("Build", align = "center", font=("Arial", 10, "bold"))

    def glow_green(self):
        self.pencolor((100, 50, 50))
        self.update_build_text((100, 50, 50))

    def revert_to_red(self,x,y):
        self.update_build_text(self.start_color)
        self.pencolor(self.start_color)

    def build(self):
        pass


class Wall_Button_Image(turtle.Turtle):

    def __init__(self, shape, position):
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
        # self.wall_type = wall_type

        self.is_selected = False

    def find_center(self):
        self.center_y = self.ycor() + 20

        if self.shape == "right_lean_wall":
            self.center_x = self.xcor() + 15
        elif self.shape == "left_lean_wall":
            self.center_x = self.xcor() - 15
        else:
            self.center_x = self.xcor()
