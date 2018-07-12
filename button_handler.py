import turtle



class Button_Handler():

    def __init__(self):

        self.wall_button_list = []
        self.button_image_list = []
        self.active_grid = []
        self.active_row = -340
        self.active_column = -120
        self.new_wall_shape = ""
        self.new_wall_position = (0, 0)
        self.new_wall_type = ""

        self.vert_button_image = Wall_Button_Image(wall_shape = "vertical_wall", position = (-300, 65))
        self.right_button_image = Wall_Button_Image(wall_shape = "right_lean_wall", position = (-315, -15))
        self.left_button_image = Wall_Button_Image(wall_shape = "left_lean_wall", position = (-285, -95))
        self.button_image_list.append(self.vert_button_image)
        self.button_image_list.append(self.right_button_image)
        self.button_image_list.append(self.left_button_image)

    def create_buttons(self):
        # wall buttons
        for image in self.button_image_list:
            image.find_center()
            wall_button = Wall_Button(button_handler = self, shape = "large_button_border", image = image)
            wall_button.setposition(image.center_x, image.center_y)
            self.wall_button_list.append(wall_button)

        # left grid buttons
        for _ in range(4):
            grid_button = Grid_Button(button_handler = self, shape = "grid_button_border", button_type = "grid_button")
            grid_button.setposition(self.active_column, self.active_row)
            self.active_grid.append(grid_button)
            self.active_column += 30

        # right grid buttons
        self.active_column += 30
        for _ in range(4):
            grid_button = Grid_Button(button_handler=self, shape="grid_button_border", button_type = "grid_button")
            grid_button.setposition(self.active_column, self.active_row)
            self.active_grid.append(grid_button)
            self.active_column += 30

        # build button
        self.build_button = Text_Button(button_handler = self, shape = "large_button_border", button_type = "build_button", button_text = "Build")
        self.build_button.setposition(-300, -150)
        self.build_button.update_button_text(self.build_button.start_color)

        # active grid row controls
        self.advance_row_button = Text_Button(button_handler = self, shape = "large_button_border", button_type = "advance_row_button", button_text = "Up")
        self.advance_row_button.setposition(250, -150)
        self.advance_row_button.update_button_text(self.advance_row_button.start_color)

        self.retreat_row_button = Text_Button(button_handler = self, shape = "large_button_border", button_type = "retreat_row_button", button_text = "Down")
        self.retreat_row_button.setposition(250, -200)
        self.retreat_row_button.update_button_text(self.retreat_row_button.start_color)

        # enemy buttons
        self.basic_enemy_button = Text_Button(button_handler = self, shape = "large_button_border", button_type = "basic_enemy", button_text = "Basic\nEnemy")
        self.basic_enemy_button.setposition(-300, 150)
        self.basic_enemy_button.pencolor((255, 255, 255))
        self.basic_enemy_button.start_color = (255, 255, 255)
        self.basic_enemy_button.update_button_text(self.basic_enemy_button.start_color)

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

    def build_wall_section(self):

        for wall_button in self.wall_button_list:
            if wall_button.is_selected:
                self.new_wall_shape = wall_button.image.wall_shape
        for grid_button in self.active_grid:
            if grid_button.is_selected:
                self.new_wall_position = (grid_button.xcor(), grid_button.ycor())

        if self.new_wall_position[0] > 30 and self.new_wall_shape == "left_lean_wall":
            self.new_wall_type = "roof"
        elif 120 > self.new_wall_position[0] > 0 and self.new_wall_shape == "right_lean_wall":
            self.new_wall_type = "floor"
        elif self.new_wall_position[0] < -30 and self.new_wall_shape == "right_lean_wall":
            self.new_wall_type = "roof"
        elif -120 < self.new_wall_position[0] < 0 and self.new_wall_shape == "left_lean_wall":
            self.new_wall_type = "floor"
        elif self.new_wall_shape == "vertical_wall":
            self.new_wall_type = "vertical"
        else:
            print("invalid selections")
            return("no wall section built")

        wall_section = Wall_Section(self.new_wall_shape, self.new_wall_position, self.new_wall_type)

    def advance_active_grid_row(self):
        for button in self.active_grid:
            button.setposition(button.xcor(), button.ycor() + 40)

    def retreat_active_grid_row(self):
        for button in self.active_grid:
            button.setposition(button.xcor(), button.ycor() - 40)


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
        if self.button_type == "wall_button":
            self.button_handler.switch_wall_button_focus(self)
        elif self.button_type == "grid_button":
            self.button_handler.switch_grid_button_focus(self)
        elif self.button_type == "build_button":
            self.button_handler.build_wall_section()
            self.dim()
        elif self.button_type == "advance_row_button":
            self.button_handler.advance_active_grid_row()
            self.dim()
        elif self.button_type == "retreat_row_button":
            self.button_handler.retreat_active_grid_row()
            self.dim()
        elif self.button_type == "basic_enemy":
            self.dim()


class Grid_Button(Button):

    def __init__(self, button_handler, shape, button_type):
        super().__init__(button_handler, shape)
        self.button_type = button_type


class Wall_Button(Button):

    def __init__(self, button_handler, shape, image):
        super().__init__(button_handler, shape)
        self.image = image
        self.button_type = "wall_button"


class Text_Button(Button):

    def __init__(self, button_handler, shape, button_type, button_text):
        super().__init__(button_handler, shape)
        self.setheading(0)
        self.start_color = (200, 50, 50)
        self.pencolor(self.start_color)
        self.pencil = turtle.Turtle()
        self.pencil.speed(0)
        self.pencil.hideturtle()
        self.pencil.penup()
        self.button_type = button_type
        self.onrelease(self.revert_to_red)
        self.button_text = button_text

    def update_button_text(self, color):
        self.pencil.clear()
        self.pencil.pencolor(color)
        self.pencil.setposition(self.xcor() + 1, self.ycor() - 7)
        self.pencil.write(self.button_text, align = "center", font=("Arial", 10, "bold"))

    def dim(self):
        dim_color = []
        for value in self.pencolor():
            dim_color.append(int(value * 0.5))
        self.pencolor(dim_color)
        self.update_button_text(dim_color)

    def revert_to_red(self,x,y):
        self.update_button_text(self.start_color)
        self.pencolor(self.start_color)


class Wall_Button_Image(turtle.Turtle):

    def __init__(self, wall_shape, position):
        turtle.Turtle.__init__(self)
        self.speed(0)
        self.hideturtle()
        self.penup()
        self.shape(wall_shape)
        self.color("white")
        self.setheading(90)
        self.setposition(position)
        self.showturtle()
        self.wall_shape = wall_shape

        self.is_selected = False

    def find_center(self):
        self.center_y = self.ycor() + 20

        if self.wall_shape == "right_lean_wall":
            self.center_x = self.xcor() + 15
        elif self.wall_shape == "left_lean_wall":
            self.center_x = self.xcor() - 15
        else:
            self.center_x = self.xcor()


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