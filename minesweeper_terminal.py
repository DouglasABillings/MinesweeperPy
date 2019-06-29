from minesweeper import *
import random


def difficulty():
    """ User prompted for difficulty (easy, medium, or hard)
    :return: Board width, heights, and number of bombs
    """
    value = 0
    while value not in range(1, 4):
        try:
            diff_num = input("Select a level of difficulty, 1) Easy 2) Medium 3) Hard\n")
            value = int(diff_num)
        except ValueError:
            value = 0
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


def bomb_location():
    """
    :return: returns a set of bombs at random locations
    """
    counter = 1
    total_bombs = set()
    while counter in range(1, version["num_bombs"] + 1):
        bomb_x = random.randint(1, version["board_width"])
        bomb_y = random.randint(1, version["board_height"])
        bombs = (bomb_x, bomb_y)
        total_bombs.add(bombs)
        counter += 1
    return total_bombs


def user_move():
    """Takes in user input for the coord and action
    :return: returns a String and a Tuple
    """
    x, y = 0, 0
    action = ""
    while x not in range(1, game["board_width"]):
        while y not in range(1, game["board_height"]):
            try:
                # We have to handle this in a try catch block, because it may throw an exception
                x, y = map(int, input("Please enter your move in the form of x y\n").split())
                action = (input("L to reveal or R to flag\n").upper())
            except ValueError:
                # Make sure to handle a ValueError exception
                x, y = 0, 0
    coord = x, y
    if action is "L" or "l":
        return {
            "action": "LEFT_CLICK",
            "coord": coord
        }

    elif action is "R" or "r":
        return {
            "action": "RIGHT_CLICK",
            "coord": coord
        }


if __name__ == '__main__':
    version = difficulty()
    bomb_set = bomb_location()
    game = create_game(version["board_width"], version["board_height"], bomb_set)

    while not game["game_over"]:
        print(board_to_string(game["board"]))
        move = user_move()
        game = get_next_game(game, move["action"], move["coord"])
    if game["game_over"] and not game["is_win"]:
        print("You hit a bomb, try again!")
    if game["game_over"] and game["is_win"]:
        print("You won, congratulations")
