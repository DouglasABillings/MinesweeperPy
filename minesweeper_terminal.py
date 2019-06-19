from minesweeper import *


if __name__ == '__main__':
    # TODO: Prompt user for difficulty (easy, medium, or hard)
    # TODO: Generate a random list of bomb locations
    # TODO: Create game using the appropriate width and height, and the bomb locations

    game = create_game(10, 10, {(0, 1), (1, 1), (2, 2)})

    # TODO: get a move from the player (an action and a coordinate)
    # TODO: update the game state one move
    # TODO: print the game's board
    # TODO: repeat until the game ends

    game = get_next_game(game, "LEFT_CLICK", (5, 2))
    print(board_to_string(game["board"]))
