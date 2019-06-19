import copy


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


def create_game(board_width, board_height, bomb_set):
    """ Get a new Game data structure
    :param board_width:
    :param board_height:
    :param bomb_set:
    :return: A game Dictionary
    """
    return {
        "board_width": board_width,
        "board_height": board_height,
        "bombs": bomb_set,
        "game_over": False,
        "is_win": False,
        "board": place_nums_on_board(place_bombs_on_board(create_board(board_width, board_height), bomb_set))
    }


def cell_to_char(cell):
    """ Generate a Char from a given Cell
    :param cell:
    :return: A Char representing the given cell
    """
    if cell["visible"]:
        return cell["value"]
    else:
        return 'F' if cell["flagged"] else '#'


def board_to_string(board):
    """ Generates a string from a given board
    :param board:
    :return: A String representing the given board
    """
    result = ""
    for y in range(len(board)):
        row_string = ""
        for x in range(len(board[0])):
            row_string += cell_to_char(board[y][x])
        result += row_string
        if y in range(len(board) - 1):
            result += '\n'
    return result


def place_bombs_on_board(board, bomb_set):
    """ Generates a board with bombs placed
    :param board:
    :param bomb_set:
    :return: a new board
    """
    result = copy.deepcopy(board)
    for y in range(len(board)):
        for x in range(len(board[0])):
            if (x, y) in bomb_set:
                result[y][x]["value"] = 'X'
    return result


def place_nums_on_board(board):
    """ Generates a board with numbers placed
    :param board: 2D array of dictionaries
    :return: Returns a board with numbers
    """
    result = copy.deepcopy(board)
    direction = [(-1, -1), (-1, 0), (-1, 1),
                 (0, -1), (0, 1),
                 (1, -1), (1, 0), (1, 1)]
    for y in range(len(result)):
        for x in range(len(result[0])):
            if result[y][x]["value"] == 'X':
                continue
            for (delta_x, delta_y) in direction:
                new_y = y + delta_y
                new_x = x + delta_x
                in_bounds = 0 <= new_y < len(result) and 0 <= new_x < len(result[0])
                if in_bounds and result[new_y][new_x]["value"] == 'X':
                    result[y][x]["value"] = chr(ord(result[y][x]["value"]) + 1)
    return result


def get_next_board(board, action, coord):
    """ Generates the next state of board with an action taken
    :param board: 2D Array of Dictionaries
    :param action: Reveal or Flag (Left or Right Click)
    :param coord: A tuple where the action is being taken place
    :return: A new board
    """
    result = copy.deepcopy(board)
    (x, y) = coord
    in_bounds = 0 <= y < len(result) and 0 <= x < len(result[0])
    if not in_bounds:
        return result

    cell = result[y][x]
    directions = [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1), (0, 1),
                  (1, -1), (1, 0), (1, 1)]

    if action == "LEFT_CLICK":
        if not cell["visible"] and not cell["flagged"]:
            cell["visible"] = True
            if cell["value"] == '0':
                for (delta_x, delta_y) in directions:
                    result = get_next_board(result, action, (x + delta_x, y + delta_y))
    elif action == "RIGHT_CLICK":
        cell["flagged"] = not cell["flagged"]

    return result


def is_board_over(board):
    """ Checks the board to see if the game is over and if it's a win
    :param board: 2D Array of Dictionaries
    :return: Tuple of two Booleans
    """
    result = copy.deepcopy(board)

    total_cells = len(result) * len(result[0])
    total_bombs = 0
    visible_bombs = 0
    visible_non_bombs = 0
    for y in range(len(result)):
        for x in range(len(result[0])):
            cell = result[y][x]
            if cell["value"] == 'X':
                total_bombs += 1
                if cell["visible"]:
                    visible_bombs += 1
            elif cell["visible"]:
                visible_non_bombs += 1

    if visible_bombs > 0:
        return True, False
    elif visible_non_bombs == total_cells - total_bombs:
        return True, True
    else:
        return False, False


def get_next_game(game, action, coord):
    """ Generate and return the next state of game
    :param game: A game dictionary
    :param action: An action to perform (either the string "LEFT_CLICK" or "RIGHT_CLICK")
    :param coord: A location to perform the action
    :return: A new game dictionary
    """
    result = copy.deepcopy(game)
    result["board"] = get_next_board(result["board"], action, coord)
    is_over, is_win = is_board_over(result["board"])
    result["game_over"] = is_over
    result["is_win"] = is_win
    return result
