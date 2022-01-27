import random as rand
import pygame
import time

pygame.init()
INSTRUCTIONS = [
    "Blue isn't in the word",
    "Yellow is in the word but not the right spot",
    "Green is in the word and the right spot"
]
INST_FONT = pygame.font.Font('FallingSky-JKwK.otf', 18)
FONT = pygame.font.Font('FallingSky-JKwK.otf', 32)
WIDTH = 900
HEIGHT = 600
WINDOW_SIZE = [WIDTH, HEIGHT]
BOARD_OFFSET = 600
BOARDER = 50
FPS = 60


# returns list of 5 letter words from txt file
def get_dictionary():
    f = open('5letterwords.txt')
    words = f.readlines()
    f.close()
    return [word[:-1] for word in words]


def draw():
    screen.fill('grey')
    # prints the game board
    for x in range(5):
        for y in range(5):
            pygame.draw.rect(screen, col_board[x][y],
                             [(y * 100) + BOARDER,
                              (x * 100) + BOARDER,
                              90, 90], 1)
            rend = FONT.render(board[x][y], True, 'black')
            screen.blit(rend, [(y * 100) + BOARDER + 35, (x * 100) + BOARDER + 20])

    # prints the game information
    vert_offset = 0
    colors = ['blue', 'yellow', 'green']
    for i, text in enumerate(INSTRUCTIONS):
        rend = INST_FONT.render(text, True, colors[i])
        screen.blit(rend, [BOARD_OFFSET - 50, BOARDER + vert_offset])
        vert_offset += 25

    pygame.draw.line(screen, 'black',
                     [BOARD_OFFSET - 50, BOARDER + 80],
                     [WIDTH - 10, BOARDER + 80])

    pygame.draw.rect(screen, 'black',
                     [BOARD_OFFSET, BOARDER + 100,
                      WIDTH - 10 - BOARDER - BOARD_OFFSET,
                      HEIGHT - (BOARDER * 2) - 110], 1)

    vert_offset = 100
    ifix = 0
    for i, guess in enumerate(guesses):
        # letter color
        l, c = guess, guesses_col[guess]
        rend = FONT.render(l, True, c)
        i -= ifix
        screen.blit(rend, [BOARD_OFFSET + (i * 20) + 10, BOARDER + vert_offset])
        if i % 10 == 0 and i != 0:
            vert_offset += 25
            ifix += 10
    pygame.display.update()


def update_loc(s, r):
    s += 1
    if s > 4:
        s = 0
        r += 1
        if r > 4:
            s = r = -1
    return s, r


def check_word(word):
    if word == secret_word:
        return True
    return False


def add_letter():
    global cur_row, cur_square
    color = 'blue'
    for i, char in enumerate(secret_word):
        if char == let:
            if i == cur_square:
                color = 'green'
                break
            color = 'yellow'
    board[cur_row][cur_square] = let
    col_board[cur_row][cur_square] = color
    # adds let to list of guesses
    if let not in guesses_col:
        color = 'blue' if color == 'blue' else 'green'
        guesses_col[let] = color
        guesses.append(let)

    # checks if you filled current attempt
    if cur_square == 4:
        word = ''.join(board[cur_row])
        # word wasn't found in the dictionary so retry line
        if word not in dictionary:
            cur_square = 0
            for j in range(len(board[cur_row])):
                board[cur_row][j] = ''
                col_board[cur_row][j] = 'black'
            return True
        # word guessed
        if check_word(word):
            return False

    # updates location in board
    cur_square, cur_row = update_loc(cur_square, cur_row)
    if cur_square == -1 and cur_row == -1:
        return False
    return True


if __name__ == '__main__':
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption('Wordle')
    clock = pygame.time.Clock()

    dictionary = get_dictionary()
    secret_word = dictionary[rand.randint(0, len(dictionary) - 1)]
    board = [['', '', '', '', ''] for x in range(5)]
    col_board = [['black', 'black', 'black', 'black', 'black'] for x in range(5)]
    cur_square, cur_row = 0, 0
    playing = True
    guesses_col = {}
    guesses = []

    while playing:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
            if event.type == pygame.KEYDOWN:
                let = pygame.key.name(event.key)
                playing = add_letter()
        draw()
    time.sleep(2)
    pygame.quit()
