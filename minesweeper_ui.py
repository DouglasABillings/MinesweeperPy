import math
import random
import arcade
import minesweeper

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Minesweeper"

# Global constants that help define the UI for the board
CELL_SIZE_PX = 25

# Global constants that help define buttons in the UI
NUM_BUTTONS = 4
BUTTONS_X_OFFSET = 20
BUTTONS_Y_OFFSET = SCREEN_HEIGHT - 20
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
        bomb_x = random.randint(0, difficulty["board_width"] - 1)
        bomb_y = random.randint(0, difficulty["board_height"] - 1)
        bombs = (bomb_x, bomb_y)
        total_bombs.add(bombs)
        counter += 1
    return total_bombs


def get_ui_data(game):
    """
    Generates all of the data needed to represent a UI for a game.
    Consolidates all of the data needed to configure the UI into one maintainable and testable function.

    :param game: The game we need to generate the UI data for
    :return: A data structure that contains declarative UI data for the game
    """
    result = {
        "buttons": [{
            "x": BUTTONS_X_OFFSET,
            "y": BUTTONS_Y_OFFSET - BUTTON_SPACING * 0,
            "width": BUTTON_WIDTH,
            "height": BUTTON_HEIGHT,
            "text": "RESET",
        }, {
            "x": BUTTONS_X_OFFSET,
            "y": BUTTONS_Y_OFFSET - BUTTON_SPACING * 1,
            "width": BUTTON_WIDTH,
            "height": BUTTON_HEIGHT,
            "text": "EASY",
        }, {
            "x": BUTTONS_X_OFFSET,
            "y": BUTTONS_Y_OFFSET - BUTTON_SPACING * 2,
            "width": BUTTON_WIDTH,
            "height": BUTTON_HEIGHT,
            "text": "MEDIUM",
        }, {
            "x": BUTTONS_X_OFFSET,
            "y": BUTTONS_Y_OFFSET - BUTTON_SPACING * 3,
            "width": BUTTON_WIDTH,
            "height": BUTTON_HEIGHT,
            "text": "HARD",
        }],
        "colors": {
            "background": arcade.set_background_color((60, 60, 60)),
            "border": arcade.color.BLACK,
            "text": arcade.color.BLACK,
            "default": arcade.color.LIGHT_GRAY,
            "button_color": arcade.color.LIGHT_GRAY,
            "flag": arcade.color.RED,
            "bomb": arcade.color.BLACK,
            "empty": arcade.color.DARK_GRAY,
            "click": arcade.color.YELLOW,
            "over": arcade.color.RED,
            "one": arcade.color.BLUE,
            "two": arcade.color.DARK_GREEN,
            "three": arcade.color.RED,
            "four": arcade.color.PURPLE,
            "five": arcade.color.MAROON,
            "six": arcade.color.TURQUOISE,
            "seven": arcade.color.BLACK,
            "eight": arcade.color.GRAY
        },
        "board": {
            "x": (SCREEN_WIDTH / 2) - ((game["board_width"] / 2) * CELL_SIZE_PX),
            "y": (SCREEN_HEIGHT / 2) - ((game["board_height"] / 2) * CELL_SIZE_PX),
            "cells": []
        }
    }
    for y in range(game["board_height"]):
        row = []
        for x in range(game["board_width"]):
            colors = result["colors"]
            color = None
            cell = game["board"][y][x]
            if cell["flagged"]:
                color = colors["flag"]
            elif cell["visible"] or (game["game_over"] and not game["is_win"]):
                if cell["value"] == 'X':
                    color = colors["bomb"]
                else:
                    color = colors["empty"]
            else:
                color = colors["default"]
            row.append({
                "x": result["board"]["x"] + (x * CELL_SIZE_PX) + (CELL_SIZE_PX / 2),
                "y": SCREEN_HEIGHT - (y * CELL_SIZE_PX) - (CELL_SIZE_PX / 2) - result["board"]["y"],
                "height": CELL_SIZE_PX,
                "width": CELL_SIZE_PX,
                "color": color
            })
        result["board"]["cells"].append(row)

    return result


class App(arcade.Window):
    """
    The App class handles the implementation details of rendering our application at 60 FPS in an OS window

    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """

    # properties that are on each instance
    game = {}
    difficulty = 1

    ui_data = None

    button_shape_list = None
    board_shape_list = None

    click_text = "No click"
    offset_x = 0
    offset_y = 0

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        # Create a game to play
        difficulty = get_difficulty(self.difficulty)
        bomb_set = get_bomb_set(difficulty)
        self.game = minesweeper.create_game(difficulty["board_width"], difficulty["board_height"], bomb_set)

        arcade.set_background_color((60, 60, 60))

    def generate_button_shape_list(self):
        self.button_shape_list = arcade.ShapeElementList()

        for button in self.ui_data["buttons"]:
            # NOTE: this takes the x,y as the center, but we are storing the top left location
            button = arcade.create_rectangle_filled(
                button["x"] + (button["width"] / 2),
                button["y"] - (button["height"] / 2),
                button["width"],
                button["height"],
                self.ui_data["colors"]["button_color"]
            )
            self.button_shape_list.append(button)

    def generate_shape_list(self):
        """
        Regenerate the shape list based on the current state of the game
        """
        cells = self.ui_data["board"]["cells"]
        self.board_shape_list = arcade.ShapeElementList()
        for row in cells:
            for cell in row:
                rect = arcade.create_rectangle_filled(
                    cell["x"],
                    cell["y"],
                    cell["width"],
                    cell["height"],
                    cell["color"]
                )
                border = arcade.create_rectangle_outline(
                    cell["x"],
                    cell["y"],
                    cell["width"],
                    cell["height"],
                    self.ui_data["colors"]["border"]
                )
                self.board_shape_list.append(rect)
                self.board_shape_list.append(border)

    def setup(self):
        """
        Store all of the geometry for our scene into a shape list to optimize draw speed
        """
        # reset the game
        self.reset_game(self.difficulty)

        # generate the shape lists
        self.generate_button_shape_list()
        self.generate_shape_list()

    def reset_game(self, difficulty):
        """
        :return:
        """
        self.difficulty = difficulty
        difficulty = get_difficulty(self.difficulty)
        bomb_set = get_bomb_set(difficulty)
        self.game = minesweeper.create_game(difficulty["board_width"], difficulty["board_height"], bomb_set)
        self.ui_data = get_ui_data(self.game)

        # The top left corner of the board needs to be adjusted
        self.offset_x = (SCREEN_WIDTH / 2) - ((self.game["board_width"] / 2) * CELL_SIZE_PX)
        self.offset_y = (SCREEN_HEIGHT / 2) - ((self.game["board_height"] / 2) * CELL_SIZE_PX)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()

        # Call draw() on all your sprite lists below
        self.board_shape_list.draw()
        self.button_shape_list.draw()
        colors = self.ui_data["colors"]

        arcade.draw_text(self.click_text, 20, 20, colors["click"])

        for button in self.ui_data["buttons"]:
            # NOTE: this takes the x,y as the center, but we are storing the top left location
            x_fudge = -4 * len(button["text"])
            y_fudge = 5
            arcade.draw_text(
                button["text"],
                button["x"] + (button["width"] / 2) + x_fudge,
                button["y"] - (button["height"] / 2 + y_fudge),
                colors["text"]
            )

        if self.game["game_over"] and not self.game["is_win"]:
            x_fudge = -85
            y_fudge = -20
            arcade.draw_text("YOU LOSE", SCREEN_WIDTH / 2 + x_fudge, SCREEN_HEIGHT / 2 + y_fudge, colors["over"], 36)

        if self.game["game_over"] and self.game["is_win"]:
            x_fudge = -85
            y_fudge = -20
            arcade.draw_text("YOU WON", SCREEN_WIDTH / 2 + x_fudge, SCREEN_HEIGHT / 2 + y_fudge, colors["over"], 36)

        # Draw text for all the cells
        # TODO: investigate if this performs well (we should probably use sprites instead)
        for row in range(self.game["board_height"]):
            for col in range(self.game["board_width"]):
                cell = self.game["board"][row][col]
                not_flagged = not cell["flagged"]
                not_empty = cell["value"] != '0'
                is_visible = cell["visible"] or (self.game["game_over"] and not self.game["is_win"])
                if not_flagged and not_empty and is_visible:
                    color = colors["bomb"]
                    if cell["value"] == '1':
                        color = colors["one"]
                    elif cell["value"] == '2':
                        color = colors["two"]
                    elif cell["value"] == '3':
                        color = colors["three"]
                    elif cell["value"] == '4':
                        color = colors["four"]
                    elif cell["value"] == '5':
                        color = colors["five"]
                    elif cell["value"] == '6':
                        color = colors["six"]
                    elif cell["value"] == '7':
                        color = colors["seven"]
                    elif cell["value"] == '8':
                        color = colors["eight"]

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

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button
        """
        is_left_click = button == 1
        is_right_click = button == 4

        for button in self.ui_data["buttons"]:
            if button["x"] <= x <= button["x"] + button["width"]:
                if button["y"] - button["height"] <= y <= button["y"]:
                    if button["text"] == 'RESET':
                        self.reset_game(self.difficulty)
                    elif button["text"] == 'EASY':
                        self.reset_game(1)
                    elif button["text"] == 'MEDIUM':
                        self.reset_game(2)
                    elif button["text"] == 'HARD':
                        self.reset_game(3)

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
        self.ui_data = get_ui_data(self.game)
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
