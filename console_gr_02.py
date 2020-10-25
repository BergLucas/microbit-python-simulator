import math
import random

import radio
import microbit


# definition of functions
def get_message():
    """Waits and return a message from another micro:bit.

    Return
    ------
    message: message sent by another micro:bit (str)
    """
    message = None
    while message == None:
        microbit.sleep(250)
        message = radio.receive()

    return message


def create_board():
    """Creates an empty board.

    Return
    -------
    board : A dictionary with the coordinates of the board (dict)
    """
    board = {}

    # add all possible coordinates and set them to 0
    for x in range(5):
        for y in range(5):
            board[(x, y)] = 0
    return board


def create_all_pieces():
    """Creates every pieces available.

    Return
    ------
    pieces : every pieces available (list)
    """
    pieces = (
        # Lines
        [(0, 0), (0, 1), (0, 2), (0, 3)],
        [(0, 0), (0, 1), (0, 2)],
        [(0, 0), (0, 1)],
        [(0, 0)],

        # Columns
        [(0, 0), (1, 0), (2, 0), (3, 0)],
        [(0, 0), (1, 0), (2, 0)],
        [(0, 0), (1, 0)],
        [(0, 0)],

        # Zigzag
        [(0, 0), (0, 1), (1, 1), (1, 2)],
        [(0, 1), (1, 1), (1, 0), (2, 0)],

        # Corners
        [(0, 0), (0, 1), (1, 0)],
        [(0, 0), (0, 1), (0, 2), (1, 0), (2, 0)],

        # Square
        [(0, 0), (0, 1), (1, 0), (1, 1)]
    )

    return pieces


def encode(board, piece):
    """Sets the moving piece in the board and transforms the information of the board to str in order to transfer
    them to the gamepad.

    Parameters
    ----------
    board : board game (dictionary)
    piece : coordinates of the moving piece (list of tuples)
    """
    mess = ''

    for y in range(5):
        for x in range(5):
            if (x, y) in piece:
                # if the coordinates are part of the coordinates of the moving piece, add 8 to the string
                # (representing the value of the light of a moving piece).
                mess += '8'
            else:
                # else, take the value from the board dictionary.
                mess += str(board[(x, y)])
    return mess


def collides_piece(board, new_piece):
    """Checks if the new piece collides with an already dropped piece

    Parameters
    ----------
    board : board game (dictionary)
    new_piece : piece which is dropped by the player (list)

    Return
    ------
    True : if the new piece collides with an already dropped piece
    False : if the new piece doesn't collide with any already dropped piece
    """
    # if the coordinates of the new piece are set in the dict, it means another piece is already in that place.
    for coord in new_piece:
        if board[coord] != 0:
            return True
    return False


def clear_five(board):
    """Clears a line or a column if it is filled

    Parameters
    ----------
    board : game board (dictionary)

    Return
    ------
    board : new game board
    """
    for x in range(5):
        i = 0
        j = 0
        # checking if a line or a column is filled
        for y in range(5):
            if board[(x, y)] == 5:
                i += 1
            if board[(y, x)] == 5:
                j += 1
        # setting the light of the corresponding coordinates to 0 if a line or a column is found filled
        if i == 5:
            for y in range(5):
                board[(x, y)] = 0
        if j == 5:
            for y in range(5):
                board[(y, x)] = 0
    return board


def move_piece(board, piece, direction):
    """Moves a piece if it does not collide with board sides or other pieces

    Parameters
    ----------
    board : game board (dictionary)
    piece : piece to move (list)
    direction : direction in which the piece will be moved (tuple)

    Returns
    -------
    new_piece : new piece position (list)
    piece : initial piece position (list)
    """
    # take and split the directions from the parameter
    dx = int(direction[0])
    dy = int(direction[1])

    for (dx, dy) in ((dx, dy), (dx, 0), (0, dy)):
        # moving the piece by adding the directions to the old coordinates of the piece
        new_piece = []
        for coordinate in piece:
            x = coordinate[0]
            y = coordinate[1]
            new_piece.append((x + dx, y + dy))

        # split the new coordinates and return them
        for coordinate in new_piece:
            new_x = coordinate[0]
            new_y = coordinate[1]

            if new_x > 4 or new_y > 4 or new_x < 0 or new_y < 0:
                break
            elif board[coordinate] != 0:
                break
        else:
            return new_piece
    return piece


def drop_piece(piece, board):
    """Drops the piece in the board

    Parameters
    ----------
    piece : piece to drop (list)
    board : board game (dictionary)

    Return
    ------
    board : board game with the new piece added (dict)
    """
    for coord in piece:
        board[coord] = 5
    return board


# settings
group_id = 2

# setup radio to receive orders
radio.on()
radio.config(group=group_id)
print('configured')
# create empty board + available pieces
board = create_board()
pieces = create_all_pieces()

# loop until game is over
nb_dropped_pieces = 0
game_is_over = False

while not game_is_over:
    # show score (number of pieces dropped)
    print('show')
    microbit.display.show(nb_dropped_pieces)
    print('show done')

    # create a new piece in the top left corner
    piece = pieces[random.randint(0, len(pieces) - 1)]

    # check if the new piece collides with dropped pieces
    game_is_over = collides_piece(board, piece)

    if not game_is_over:
        # ask orders until the current piece is dropped
        piece_dropped = False
        while not piece_dropped:
            # send state of the board to gamepad (as a string)
            radio.send(encode(board, piece))
            print('GAME: Send message')
            # wait until gamepad sends an order
            order = get_message()
            print('GAME: Receive message', order)
            # execute order (drop or move piece)
            if order == 'Drop':
                board = drop_piece(piece, board)
                nb_dropped_pieces += 1
                piece_dropped = True

                # check if a line/column is filled
                board = clear_five(board)
            else:
                piece = move_piece(board, piece, order.split(','))

        # wait a few milliseconds and clear screen
        microbit.sleep(500)
        microbit.display.clear()

# tell that the game is over
microbit.display.scroll('Game is over', delay=100)
