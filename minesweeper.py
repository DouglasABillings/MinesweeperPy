def create_cell(visible=False, flagged=False, value='0'):
    """ Returns a cell
    :param visible: Whether the cell is visible or not
    :param flagged: Whether the cell is flagged or not
    :param value: The cell's value as a character, defaults to '0'
    :return: A cell Dictionary
    """
    return {"visible": visible, "flagged": flagged, "value": value}


def create_board(width, height):
    """ Get a new Board data structure
    :param width:
    :param height:
    :return: A 2D array of cells
    """
    result = []
    for y in range(height):
        row = []
        for x in range(width):
            row.append(create_cell())
        result.append(row)
    return result


def create_game(board_width, board_height, num_bombs):
    """ Get a new Game data structure
    :param board_width:
    :param board_height:
    :param num_bombs:
    :return: A game Dictionary
    """
    return {
        "board_width": board_width,
        "board_height": board_height,
        "num_bombs": num_bombs,
        "game_over": False,
        "board": create_board(board_width, board_height)
    }


if __name__ == '__main__':
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
    test_create_cell()

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
    test_create_board()

    def test_create_game():
        game1 = {
            "board_width": 3,
            "board_height": 2,
            "num_bombs": 10,
            "game_over": False,
            "board": [
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
        }
        game2 = {
            "board_width": 2,
            "board_height": 1,
            "num_bombs": 3,
            "game_over": False,
            "board": [
                [
                    {"visible": False, "flagged": False, "value": '0'},
                    {"visible": False, "flagged": False, "value": '0'}
                ]
            ]
        }
        # Can create a new game
        assert create_game(board_width=3, board_height=2, num_bombs=10) == game1
        assert create_game(board_width=2, board_height=1, num_bombs=3) == game2
    test_create_game()

    # TODO: convert a cell to a string
    # TODO: convert a board to a string

    print("All tests passed!")
