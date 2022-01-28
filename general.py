INSTRUCTIONS = [
    "Blue isn't in the word",
    "Yellow is in the word but not the right spot",
    "Green is in the word and the right spot"
]
WIDTH = 900
HEIGHT = 600
WINDOW_SIZE = [WIDTH, HEIGHT]
BOARD_OFFSET = 600
BOARDER = 50
FPS = 60

board = [['', '', '', '', ''] for x in range(5)]
col_board = [['black', 'black', 'black', 'black', 'black'] for x in range(5)]
temp_cols = []
cur_square, cur_row = 0, 0
playing = True
guesses_col = {}
guesses = []
guesses_shown = 0
