from general import *
import random as rand
import pygame
import time

pygame.init()
INST_FONT = pygame.font.Font('FallingSky-JKwK.otf', 18)
FONT = pygame.font.Font('FallingSky-JKwK.otf', 32)


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
    for i in range(guesses_shown):
        guess = guesses[i]
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
        s = 5
        if r > 3:
            s = r = -1
    return s, r


def check_win(word):
    if word == secret_word:
        return True
    return False


def add_letter():
    global cur_row, cur_square, guesses_shown

    color = 'blue'
    for i, char in enumerate(secret_word):
        if char == let:
            if i == cur_square:
                color = 'green'
                break
            color = 'yellow'

    board[cur_row][cur_square] = let
    temp_cols.append(color)

    # adds let to list of guesses
    if let not in guesses_col:
        color = 'blue' if color == 'blue' else 'green'
        guesses_col[let] = color
        guesses.append(let)
        guesses.sort()

    # updates location in board
    cur_square, cur_row = update_loc(cur_square, cur_row)
    if cur_square == -1 and cur_row == -1:
        for x in range(5):
            col_board[cur_row][x] = 'red'
        return False
    return True


def check_word():
    global cur_square, cur_row, temp_cols, guesses_shown, board
    word = ''.join(board[cur_row])

    # word wasn't found in the dictionary so retry line
    if word not in dictionary:
        for j in range(len(board[cur_row])):
            board[cur_row][j] = ''
        temp_cols = []
        return True

    guesses_shown = len(guesses)

    if check_win(word):
        for x in range(5):
            col_board[cur_row][x] = 'green'
        return False

    for x in range(5):
        col_board[cur_row][x] = temp_cols[x]

    temp_cols = []
    cur_square, cur_row = update_loc(cur_square, cur_row)

    if cur_square == -1 and cur_row == -1:
        return False
    cur_row += 1
    return True


def back():
    global cur_square
    if cur_square > 0:
        cur_square -= 1
        board[cur_row][cur_square] = ''
        temp_cols.pop()


if __name__ == '__main__':
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption('Wordle')
    clock = pygame.time.Clock()

    dictionary = get_dictionary()
    secret_word = dictionary[rand.randint(0, len(dictionary) - 1)]

    while playing:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # checks word
                    if cur_square == 5:
                        playing = check_word()
                        cur_square = 0
                elif event.key == pygame.K_BACKSPACE:
                    back()
                elif cur_square <= 4:
                    let = pygame.key.name(event.key)
                    playing = add_letter()
        draw()
    time.sleep(2)
    pygame.quit()
