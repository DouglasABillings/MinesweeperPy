from minesweeper import *


def test_create_cell():
    # Can create a default cell
    assert create_cell() == {"visible": False, "flagged": False, "value": '0'}
    # Can create a visible cell
    assert create_cell(visible=True) == {"visible": True, "flagged": False, "value": '0'}
    # Can create a flagged cell
    assert create_cell(flagged=True) == {"visible": False, "flagged": True, "value": '0'}
    # Can create a hidden cell with a value
    assert create_cell(value='1') == {"visible": False, "flagged": False, "value": '1'}
    assert create_cell(value='X') == {"visible": False, "flagged": False, "value": 'X'}
    # Can create a visible cell with a value
    assert create_cell(value='1', visible=True) == {"visible": True, "flagged": False, "value": '1'}
    assert create_cell(value='X', visible=True) == {"visible": True, "flagged": False, "value": 'X'}
    # Can create a flagged cell with a value
    assert create_cell(value='1', flagged=True) == {"visible": False, "flagged": True, "value": '1'}
    assert create_cell(value='X', flagged=True) == {"visible": False, "flagged": True, "value": 'X'}
    # The function is pure
    a_cell = create_cell()
    a_cell["value"] = "LOL"
    another_cell = create_cell()
    assert another_cell == {"visible": False, "flagged": False, "value": '0'}
    assert a_cell == {"visible": False, "flagged": False, "value": "LOL"}


def test_create_board():
    board = create_board(width=3, height=2)
    default_board = [
        [
            {"visible": False, "flagged": False, "value": '0'},
            {"visible": False, "flagged": False, "value": '0'},
            {"visible": False, "flagged": False, "value": '0'}
        ],
        [
            {"visible": False, "flagged": False, "value": '0'},
            {"visible": False, "flagged": False, "value": '0'},
            {"visible": False, "flagged": False, "value": '0'}
        ]
    ]
    modified_board = [
        [
            {"visible": False, "flagged": False, "value": '0'},
            {"visible": False, "flagged": False, "value": 'X'},
            {"visible": False, "flagged": False, "value": '0'}
        ],
        [
            {"visible": False, "flagged": False, "value": '0'},
            {"visible": False, "flagged": False, "value": '0'},
            {"visible": False, "flagged": False, "value": '0'}
        ]
    ]
    # Can create a new board
    assert board == default_board
    # The function is pure
    board[0][1]["value"] = 'X'
    assert board == modified_board
    assert create_board(1, 1) == [[{"visible": False, "flagged": False, "value": '0'}]]


def test_cell_to_char():
    # Can convert a hidden cell to a char correctly
    assert cell_to_char(create_cell()) == '#'
    assert cell_to_char(create_cell(value='X')) == '#'
    assert cell_to_char(create_cell(value='1')) == '#'

    # Can convert a flagged cell to a char correctly
    assert cell_to_char(create_cell(flagged=True)) == 'F'
    assert cell_to_char(create_cell(value='X', flagged=True)) == 'F'
    assert cell_to_char(create_cell(value='3', flagged=True)) == 'F'

    # Can convert a visible cell to a char correctly
    assert cell_to_char(create_cell(visible=True)) == '0'
    assert cell_to_char(create_cell(visible=True, flagged=True)) == '0'
    assert cell_to_char(create_cell(visible=True, value='X')) == 'X'
    assert cell_to_char(create_cell(visible=True, value='1')) == '1'
    assert cell_to_char(create_cell(visible=True, value='2')) == '2'
    assert cell_to_char(create_cell(visible=True, value='3')) == '3'


def test_board_to_string():
    test_board = [
        [
            {"visible": True, "flagged": False, "value": '0'},
            {"visible": True, "flagged": False, "value": '0'},
            {"visible": True, "flagged": False, "value": '1'},
            {"visible": False, "flagged": True, "value": 'X'},
            {"visible": True, "flagged": False, "value": '1'}
        ],
        [
            {"visible": True, "flagged": False, "value": '1'},
            {"visible": True, "flagged": False, "value": '1'},
            {"visible": True, "flagged": False, "value": '1'},
            {"visible": True, "flagged": False, "value": '1'},
            {"visible": True, "flagged": False, "value": '1'}
        ],
        [
            {"visible": True, "flagged": False, "value": 'X'},
            {"visible": True, "flagged": False, "value": '1'},
            {"visible": True, "flagged": False, "value": '0'},
            {"visible": True, "flagged": False, "value": '0'},
            {"visible": True, "flagged": False, "value": '0'}
        ]
    ]

    # Can convert a board to a string correctly
    assert board_to_string(create_board(5, 5)) == "#####\n#####\n#####\n#####\n#####"
    assert board_to_string(create_board(3, 2)) == "###\n###"
    assert board_to_string(create_board(5, 2)) == "#####\n#####"
    assert board_to_string(test_board) == "001F1\n11111\nX1000"


def test_place_bombs_on_board():
    test_board = create_board(10, 10)

    # Can place a set of bombs on the board
    bomb_set = {(0, 1), (2, 3), (3, 4)}
    board_with_bombs = place_bombs_on_board(test_board, bomb_set)
    for y, row in enumerate(board_with_bombs):
        for x, cell in enumerate(row):
            if (x, y) in bomb_set:
                assert cell == create_cell(value='X')
            else:
                assert cell == create_cell(value='0')

    # Function does not throw exception and is pure
    bomb_set = {(-1, 10000)}
    place_bombs_on_board(test_board, bomb_set)
    assert test_board == create_board(10, 10)


def test_place_nums_on_board():
    test_board = create_board(3, 3)
    test_board[1][1] = create_cell(value='X')

    # Can place numbers correctly around a single bomb
    #  111
    #  1X1
    #  111
    board_with_nums = place_nums_on_board(test_board)
    for y, row in enumerate(board_with_nums):
        for x, cell in enumerate(row):
            if (x, y) == (1, 1):
                assert cell["value"] == 'X'
            else:
                assert cell["value"] == '1'

    # Can place numbers correctly around a few bombs
    #  X12X2
    #  112X2
    #  00111
    #  01232
    #  01XXX
    bombs = {(0, 0), (3, 0), (3, 1), (2, 4), (3, 4), (4, 4)}
    board_with_nums = place_nums_on_board(place_bombs_on_board(create_board(5, 5), bombs))
    for y, row in enumerate(board_with_nums):
        for x, cell in enumerate(row):
            cell["visible"] = True
    assert board_to_string(board_with_nums) == "X12X2\n112X2\n00111\n01232\n01XXX"

    # Can place numbers around a TON of bombs
    # XXX
    # X8X
    # XXX
    bombs = {(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)}
    board_with_nums = place_nums_on_board(place_bombs_on_board(create_board(3, 3), bombs))
    for y, row in enumerate(board_with_nums):
        for x, cell in enumerate(row):
            cell["visible"] = True
    assert board_to_string(board_with_nums) == "XXX\nX8X\nXXX"

    # Function is pure
    original_board = create_board(3, 3)
    original_board[1][1] = create_cell(value='X')
    assert test_board == original_board


def test_get_next_board():
    # 000000
    # 011100
    # 01X210
    # 012X10
    # 001110
    bombs = {(2, 2), (3, 3)}
    test_board = place_nums_on_board(place_bombs_on_board(create_board(6, 5), bombs))

    # Can left click to reveal a hidden bomb or number greater than zero
    next_board = get_next_board(board=test_board, action="LEFT_CLICK", coord=(3, 3))
    assert board_to_string(next_board) == "######\n######\n######\n###X##\n######"
    next_board = get_next_board(board=next_board, action="LEFT_CLICK", coord=(3, 4))
    assert board_to_string(next_board) == "######\n######\n######\n###X##\n###1##"

    # Left and right click does nothing to an already visible cell
    next_board = get_next_board(next_board, "LEFT_CLICK", (3, 3))
    next_board = get_next_board(next_board, "RIGHT_CLICK", (3, 4))
    assert board_to_string(next_board) == "######\n######\n######\n###X##\n###1##"

    # Can right click a hidden cell to flag it and again to unflag it
    next_board = get_next_board(next_board, "RIGHT_CLICK", (0, 0))
    assert board_to_string(next_board) == "F#####\n######\n######\n###X##\n###1##"
    next_board = get_next_board(next_board, "RIGHT_CLICK", (0, 0))
    assert board_to_string(next_board) == "######\n######\n######\n###X##\n###1##"
    next_board = get_next_board(next_board, "RIGHT_CLICK", (0, 0))
    assert board_to_string(next_board) == "F#####\n######\n######\n###X##\n###1##"

    # Left click does nothing to a flagged cell
    next_board = get_next_board(next_board, "LEFT_CLICK", (0, 0))
    assert next_board[0][0] == create_cell(flagged=True)
    assert board_to_string(next_board) == "F#####\n######\n######\n###X##\n###1##"

    # Function does not crash and is pure
    assert next_board == get_next_board(next_board, "LOL", (5, 5))
    assert next_board == get_next_board(next_board, "LEFT_CLICK", (23, -5))
    assert board_to_string(next_board) == "F#####\n######\n######\n###X##\n###1##"
    assert test_board == place_nums_on_board(place_bombs_on_board(create_board(6, 5), bombs))

    # Left clicking a hidden 0 cell flood fills in every possible direction recursively
    # until non zero cells are revealed
    next_board = get_next_board(next_board, "LEFT_CLICK", (1, 4))
    assert board_to_string(next_board) == "F00000\n011100\n01#210\n012X10\n001110"


def test_is_board_over():
    # 000000
    # 011100
    # 01X210
    # 012X10
    # 001110
    bombs = {(2, 2), (3, 3)}
    test_board = place_nums_on_board(place_bombs_on_board(create_board(6, 5), bombs))
    original_board = place_nums_on_board(place_bombs_on_board(create_board(6, 5), bombs))

    # Can verify a game is unsolved
    is_over, is_win = is_board_over(board=original_board)
    assert not is_over and not is_win

    # Can verify a game is lost when a bomb is click
    is_over, is_win = is_board_over(get_next_board(original_board, 'LEFT_CLICK', (2, 2)))
    assert is_over and not is_win

    # Can verify a game is unsolved after a couple moves have been made
    test_board = get_next_board(get_next_board(test_board, 'LEFT_CLICK', (1, 1)), 'LEFT_CLICK', (3, 4))
    is_over, is_win = is_board_over(test_board)
    assert not is_over and not is_win

    # Can verify a game is solved and won after all non bomb cells are made visible
    test_board = get_next_board(test_board, 'LEFT_CLICK', (0, 0))
    is_over, is_win = is_board_over(test_board)
    assert is_over and is_win
    test_board = get_next_board(test_board, 'RIGHT_CLICK', (2, 2))
    is_over, is_win = is_board_over(test_board)
    assert is_over and is_win

    # Function is pure
    assert original_board == place_nums_on_board(place_bombs_on_board(create_board(6, 5), bombs))


def test_create_game():
    bombs1 = {(0, 0)}
    game1 = {
        "board_width": 3,
        "board_height": 2,
        "bombs": bombs1,
        "game_over": False,
        "is_win": False,
        "board": [
            [
                {"visible": False, "flagged": False, "value": 'X'},
                {"visible": False, "flagged": False, "value": '1'},
                {"visible": False, "flagged": False, "value": '0'}
            ],
            [
                {"visible": False, "flagged": False, "value": '1'},
                {"visible": False, "flagged": False, "value": '1'},
                {"visible": False, "flagged": False, "value": '0'}
            ]
        ]
    }
    bombs2 = {(1, 0)}
    game2 = {
        "board_width": 2,
        "board_height": 1,
        "bombs": bombs2,
        "game_over": False,
        "is_win": False,
        "board": [
            [
                {"visible": False, "flagged": False, "value": '1'},
                {"visible": False, "flagged": False, "value": 'X'}
            ]
        ]
    }

    # Can create a new game
    assert create_game(board_width=3, board_height=2, bomb_set=bombs1) == game1
    assert create_game(2, 1, bombs2) == game2


def test_get_next_game():
    bombs = {(2, 2), (3, 3)}
    test_game = create_game(6, 5, bombs)

    # Can advance the game to its next state with a left click
    next_game = get_next_game(test_game, 'LEFT_CLICK', (3, 4))
    assert next_game == {
        "board_width": 6,
        "board_height": 5,
        "bombs": bombs,
        "game_over": False,
        "is_win": False,
        "board": get_next_board(test_game["board"], 'LEFT_CLICK', (3, 4))
    }

    # Function is pure
    assert test_game == create_game(6, 5, bombs)

    # The game is won when every non bomb cell is revealed
    next_game2 = get_next_game(next_game, 'LEFT_CLICK', (0, 0))
    assert next_game2 == {
        "board_width": 6,
        "board_height": 5,
        "bombs": bombs,
        "game_over": True,
        "is_win": True,
        "board": get_next_board(next_game["board"], 'LEFT_CLICK', (0, 0))
    }
    next_game3 = get_next_game(next_game2, 'RIGHT_CLICK', (2, 2))
    assert next_game3 == {
        "board_width": 6,
        "board_height": 5,
        "bombs": bombs,
        "game_over": True,
        "is_win": True,
        "board": get_next_board(next_game2["board"], 'RIGHT_CLICK', (2, 2))
    }

    # The game is lost when a bomb is revealed
    next_game4 = get_next_game(next_game3, 'LEFT_CLICK', (3, 3))
    assert next_game4 == {
        "board_width": 6,
        "board_height": 5,
        "bombs": bombs,
        "game_over": True,
        "is_win": False,
        "board": get_next_board(next_game3["board"], 'LEFT_CLICK', (3, 3))
    }


def run_tests():
    """Run all the tests in this module"""
    # Can create a cell
    test_create_cell()
    # Can create a board
    test_create_board()

    # Can convert a cell to a char
    test_cell_to_char()
    # Can convert a board to a string
    test_board_to_string()

    # Can place bombs on a board
    test_place_bombs_on_board()
    # Can place the numbers on a board
    test_place_nums_on_board()

    # Can advance the board to its next state
    test_get_next_board()
    # Check check to see if a board is solved, and if it was a win or loss
    test_is_board_over()

    # Can create a game
    test_create_game()
    # Can advance the game to its next state
    test_get_next_game()

    print("All tests passed!")


if __name__ == '__main__':
    run_tests()
