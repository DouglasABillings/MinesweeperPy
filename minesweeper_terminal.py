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


if __name__ == '__main__':
    # TODO: Create game using the appropriate width and height, and the bomb locations
    version = difficulty()
    bomb_set = bomb_location()
    game = create_game(version["board_width"], version["board_height"], bomb_set)

    # TODO: get a move from the player (an action and a coordinate)
    # TODO: update the game state one move
    # TODO: print the game's board
    # TODO: repeat until the game ends
    print(board_to_string(game["board"]))
    game = get_next_game(game, "LEFT_CLICK", (5, 2))

