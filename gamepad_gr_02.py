import radio
import microbit


# definition of functions

def get_message():
    """Waits and returns a message from another micro:bit.

    Return
    ------
    message: message sent by another micro:bit (str)
    """
    message = None
    while message == None:
        microbit.sleep(250)
        message = radio.receive()

    return message


def show_board(board):
    """Shows the board game on the micro:bit that we use as a controller

    Parameters
    ----------
    board : boars game (dictionary)
    """
    # show the board led by led from the decoded dictionary
    for coordinates in board:
        x = coordinates[0]
        y = coordinates[1]
        microbit.display.set_pixel(x, y, board[coordinates])


def decode(message):
    """Decodes message and puts it in the game board

    Parameters
    ----------
    message : message sent by the console that has to be decoded and put in the dictionary (str)

    Return
    ------
    board : state of the board game after adding the instructions (dict)
    """
    board = {}
    turn = 0

    # read the received message char by char and adding them to the dictionary
    for y in range(5):
        for x in range(5):
            board[x, y] = int(message[turn])
            turn += 1

    return board


# settings
group_id = 2

# setup radio to receive/send messages
radio.on()
radio.config(group=group_id)

# loop forever (until micro:bit is switched off)
while True:
    # get view of the board
    view = get_message()

    # clear screen
    microbit.display.clear()

    # show view of the board
    show_board(decode(view))

    # wait for button A or B to be pressed
    while not (microbit.button_a.is_pressed() or microbit.button_b.is_pressed()):
        microbit.sleep(50)

    if microbit.button_a.is_pressed():
        # send current direction
        if microbit.accelerometer.get_y() > 300:
            direction = '0,1'
        elif microbit.accelerometer.get_y() < -300:
            direction = '0,-1'
        elif microbit.accelerometer.get_x() > 300:
            direction = '1,0'
        elif microbit.accelerometer.get_x() < -300:
            direction = '-1,0'
        else:
            direction = '0,0'

        radio.send(direction)
    elif microbit.button_b.is_pressed():
        # notify that the piece should be dropped
        radio.send('Drop')
