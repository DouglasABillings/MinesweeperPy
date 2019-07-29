import math
import random
import arcade
import minesweeper


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Minesweeper"

CELL_SIZE_PX = 25
NUM_BUTTONS = 4
BUTTON_WIDTH = CELL_SIZE_PX * 4
BUTTON_HEIGHT = CELL_SIZE_PX * 1.25
BUTTON_SPACING = 50


def get_difficulty(value):
    """ User prompted for difficulty (easy, medium, or hard)
    :return: Board width, heights, and number of bombs
    """
    if value is 1:
        return {
            "board_width": 10,
            "board_height": 10,
            "num_bombs": 10
        }
    if value is 2:
        return {
            "board_width": 15,
            "board_height": 15,
            "num_bombs": 20
        }
    if value is 3:
        return {
            "board_width": 20,
            "board_height": 20,
            "num_bombs": 40
        }


def get_bomb_set(difficulty):
    """
    :return: returns a set of bombs at random locations
    """
    counter = 1
    total_bombs = set()
    while counter in range(1, difficulty["num_bombs"] + 1):
        bomb_x = random.randint(0, difficulty["board_width"]-1)
        bomb_y = random.randint(0, difficulty["board_height"]-1)
        bombs = (bomb_x, bomb_y)
        total_bombs.add(bombs)
        counter += 1
    return total_bombs


class App(arcade.Window):
    """
    Main application class.

    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """

    # properties that are on each instance
    game = {}
    offset_x = 0
    offset_y = 0
    difficulty = 1
    buttons = None
    shape_list = None
    click_text = None
    easy_text = None
    medium_text = None
    hard_text = None
    reset_text = None

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        arcade.set_background_color((60, 60, 60))

        # Create a game to play
        difficulty = get_difficulty(self.difficulty)
        bomb_set = get_bomb_set(difficulty)
        self.game = minesweeper.create_game(difficulty["board_width"], difficulty["board_height"], bomb_set)

    def generate_buttons(self):
        self.buttons = arcade.ShapeElementList()

        x = self.button_dict()["button_x"]
        for i in range(NUM_BUTTONS):
            y = self.button_dict()["button_y"] - (BUTTON_SPACING * i)
            button = arcade.create_rectangle_filled(x, y, BUTTON_WIDTH, BUTTON_HEIGHT, self.button_dict()["button_color"])
            self.buttons.append(button)

    def button_text(self):
        self.click_text = "No click"
        self.easy_text = "EASY"
        self.medium_text = "MEDIUM"
        self.hard_text = "HARD"
        self.reset_text = "RESET"

    def button_dict(self):
        return{
            "button_offset_x": 20,
            "button_offset_y": SCREEN_HEIGHT - 65,
            "button_x": 20 + BUTTON_WIDTH/2,
            "button_y": (SCREEN_HEIGHT - 65) - BUTTON_HEIGHT/2,
            "button_color": arcade.color.LIGHT_GRAY,
            "button_text": self.button_text(),
            }

    def generate_shape_list(self):
        """
        Regenerate the shape list based on the current state of the game
        """
        self.shape_list = arcade.ShapeElementList()
        for row in range(self.game["board_height"]):
            for col in range(self.game["board_width"]):
                cell = self.game["board"][row][col]
                x_px = self.offset_x + (col * CELL_SIZE_PX) + (CELL_SIZE_PX / 2)
                y_px = SCREEN_HEIGHT - (row * CELL_SIZE_PX) - (CELL_SIZE_PX / 2) - self.offset_y

                if cell["flagged"]:
                    color = arcade.color.RED
                elif cell["visible"] or (self.game["game_over"] and not self.game["is_win"]):
                    if cell["value"] == 'X':
                        color = arcade.color.BLACK
                    else:
                        color = arcade.color.DARK_GRAY
                else:
                    color = arcade.color.LIGHT_GRAY

                rect = arcade.create_rectangle_filled(x_px, y_px, CELL_SIZE_PX, CELL_SIZE_PX, color)
                border = arcade.create_rectangle_outline(x_px, y_px, CELL_SIZE_PX, CELL_SIZE_PX, arcade.color.BLACK)
                self.shape_list.append(rect)
                self.shape_list.append(border)

    def setup(self):
        """
        Store all of the geometry for our scene into a shape list to optimize draw speed
        """
        self.offset_x = (SCREEN_WIDTH / 2) - ((self.game["board_width"] / 2) * CELL_SIZE_PX)
        self.offset_y = (SCREEN_HEIGHT / 2) - ((self.game["board_height"] / 2) * CELL_SIZE_PX)
        # generate the shape list
        self.generate_buttons()
        self.generate_shape_list()
        self.button_text()

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()

        # Call draw() on all your sprite lists below
        self.shape_list.draw()
        self.buttons.draw()

        arcade.draw_text(self.click_text, 25, SCREEN_HEIGHT - 26, arcade.color.WHITE)
        arcade.draw_text(self.easy_text, 55, SCREEN_HEIGHT - 138, arcade.color.BLACK)
        arcade.draw_text(self.medium_text, 45, SCREEN_HEIGHT - 186, arcade.color.BLACK)
        arcade.draw_text(self.hard_text, 55, SCREEN_HEIGHT - 235, arcade.color.BLACK)
        arcade.draw_text(self.reset_text, 52, SCREEN_HEIGHT - 85, arcade.color.BLACK)

        if self.game["game_over"] and not self.game["is_win"]:
            arcade.draw_text("YOU LOSE", SCREEN_WIDTH/2 - 85, SCREEN_HEIGHT/2 - 20, arcade.color.RED, 36)

        # Draw all the required text
        # TODO: investigate if this performs well (we should probably use sprites instead)
        for row in range(self.game["board_height"]):
            for col in range(self.game["board_width"]):
                cell = self.game["board"][row][col]
                not_flagged = not cell["flagged"]
                not_empty = cell["value"] != '0'
                is_visible = cell["visible"] or (self.game["game_over"] and not self.game["is_win"])
                if not_flagged and not_empty and is_visible:
                    color = arcade.color.BLACK
                    if cell["value"] == '1':
                        color = arcade.color.BLUE
                    elif cell["value"] == '2':
                        color = arcade.color.DARK_GREEN
                    elif cell["value"] == '3':
                        color = arcade.color.DARK_RED
                    elif cell["value"] == '4':
                        color = arcade.color.PURPLE
                    elif cell["value"] == '5':
                        color = arcade.color.MAROON
                    elif cell["value"] == '6':
                        color = arcade.color.TURQUOISE
                    elif cell["value"] == '7':
                        color = arcade.color.BLACK
                    elif cell["value"] == '8':
                        color = arcade.color.GRAY

                    num_offset = 7
                    x_px = self.offset_x + (col * CELL_SIZE_PX) + num_offset
                    y_px = self.offset_y + (row * CELL_SIZE_PX) - num_offset
                    arcade.draw_text(cell["value"], x_px, SCREEN_HEIGHT - y_px - CELL_SIZE_PX, color)

    def update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        pass

    def reset_game(self, difficulty):
        """
        :return:
        """
        self.difficulty = difficulty
        difficulty = get_difficulty(self.difficulty)
        bomb_set = get_bomb_set(difficulty)
        self.game = minesweeper.create_game(difficulty["board_width"], difficulty["board_height"], bomb_set)

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button
        """
        is_left_click = button == 1
        is_right_click = button == 4

        for i in range(NUM_BUTTONS):
            if self.button_dict()["button_offset_x"] <= x <= self.button_dict()["button_offset_x"] + BUTTON_WIDTH:
                button_y = self.button_dict()["button_offset_y"] - (BUTTON_SPACING * i)
                if button_y - BUTTON_HEIGHT <= y <= button_y:
                    if i == 0:
                        self.reset_game(self.difficulty)
                    else:
                        self.reset_game(i)

        # Use math.floor to truncate down to an integer
        x_click = math.floor((x - self.offset_x) / CELL_SIZE_PX)
        y_click = math.floor(((SCREEN_HEIGHT - y) - self.offset_y) / CELL_SIZE_PX)

        # Advance the game
        if is_left_click:
            self.click_text = "left click     x: " + str(x) + " y: " + str(y)
            self.game = minesweeper.get_next_game(self.game, "LEFT_CLICK", (x_click, y_click))
        elif is_right_click:
            self.click_text = "right click     x: " + str(x_click) + " y: " + str(y_click)
            self.game = minesweeper.get_next_game(self.game, "RIGHT_CLICK", (x_click, y_click))
        else:
            return
        # Update the shape list
        self.generate_shape_list()


def main():
    """ Main method """
    # initialize an app object and call its setup method
    app = App(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    app.setup()

    # run the app
    arcade.run()


if __name__ == "__main__":
    main()
