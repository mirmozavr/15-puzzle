import pygame as pg
import sys
import random
import time


def check_solvable(board):
    PLATES = len(board)
    N = 0
    e = PLATES
    for i in range(PLATES):
        for j in range(PLATES):
            number_of_smaller_numbers = 0
            flag = False
            for p in range(PLATES - 1, -1, -1):
                if flag:
                    break
                for q in range(PLATES - 1, -1, -1):
                    if board[p][q] < board[i][j]:
                        number_of_smaller_numbers += 1
                    if p == i and q == j:
                        flag = True
                        break
            N += number_of_smaller_numbers
    # print(N, e, N + e)
    return (N + e) % 2


def check_finished(board):
    PLATES = len(board)
    plate_number_counter = 1
    for i in range(PLATES):
        for j in range(PLATES):
            if board[i][j] == 0:
                return False
            if board[i][j].n != plate_number_counter:
                return False
            plate_number_counter += 1
            if plate_number_counter == PLATES ** 2:
                return True


pg.init()
pg.display.set_caption('15 puzzle')

PLATES = 4  # number of plates on one side (cant be less than 2)
PLATE_SIZE = 80
MARGIN = 20
GAP = 2
SIDE = PLATES * PLATE_SIZE + MARGIN * 2 + GAP * (PLATES - 1)
SCREEN_SIZE = (SIDE, SIDE)
PLATE_COLOR = (180, 60, 60)
PLATE_COLOR_2 = (180, 190, 255)
FRAME_COLOR = (100, 200, 180)
TEXT_COLOR = (40, 40, 40)
GREEN = (0, 255, 140)
BLUE = (30, 45, 255)
timer = pg.time.Clock()
courier = pg.font.SysFont('courier', 48, bold=True, italic=True)

screen = pg.display.set_mode(SCREEN_SIZE)
screen.fill(FRAME_COLOR)


class Plate:
    def __init__(self, y, x, n):
        self.x, self.y, self.n = x, y, n

    def __str__(self):
        return f'{self.n}'

    def __repr__(self):
        return self.__str__()

    def draw(self):
        corner_x = self.x * PLATE_SIZE + MARGIN + GAP * self.x
        corner_y = self.y * PLATE_SIZE + MARGIN + GAP * self.y
        if self.n % 2:
            PC = PLATE_COLOR
        else:
            PC = PLATE_COLOR_2
        pg.draw.rect(screen, PC,
                     (corner_x, corner_y,
                      PLATE_SIZE, PLATE_SIZE), border_radius=5)

        text = courier.render(str(self.n), False, TEXT_COLOR)

        text_position = text.get_rect(centerx=corner_x + PLATE_SIZE // 2, centery=corner_y + PLATE_SIZE // 2)

        screen.blit(text, text_position)


# finding solvable board
while True:
    r = list(range(1, PLATES ** 2))
    random.shuffle(r)
    r = [0] + r

    board = [[0] * PLATES for z in range(PLATES)]

    for row in board:
        for col in range(len(row)):
            row[col] = r.pop()
    if check_solvable(board):
        break

# filling board with Plates
for i in range(PLATES):
    for j in range(PLATES):
        if board[i][j] != 0:
            board[i][j] = Plate(i, j, board[i][j])

# main game logic
zero_x = zero_y = PLATES - 1
while True:
    screen.fill(FRAME_COLOR)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            print('exit')
            pg.quit()
            sys.exit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and zero_x < PLATES - 1:
                board[zero_x][zero_y], board[zero_x + 1][zero_y] =\
                    board[zero_x + 1][zero_y], board[zero_x][zero_y]
            elif event.key == pg.K_DOWN and zero_x > 0:
                board[zero_x][zero_y], board[zero_x - 1][zero_y] =\
                    board[zero_x - 1][zero_y], board[zero_x][zero_y]
            elif event.key == pg.K_LEFT and zero_y < PLATES - 1:
                board[zero_x][zero_y], board[zero_x][zero_y + 1] =\
                    board[zero_x][zero_y + 1], board[zero_x][zero_y]
            elif event.key == pg.K_RIGHT and zero_y > 0:
                board[zero_x][zero_y], board[zero_x][zero_y - 1] =\
                    board[zero_x][zero_y - 1], board[zero_x][zero_y]

    for i in range(PLATES):
        for j in range(PLATES):
            if board[i][j] != 0:
                board[i][j].x, board[i][j].y = j, i
                board[i][j].draw()
            else:
                zero_x, zero_y = i, j

    pg.display.update()
    timer.tick(30)

    if check_finished(board):
        time.sleep(1)
        break
while True:
    pg.event.get()
    screen.fill(GREEN)

    text = courier.render('SOLVED!', False, BLUE)
    text_position = text.get_rect(centerx=SIDE // 2, centery=SIDE // 2)
    screen.blit(text, text_position)

    pg.display.update()
    timer.tick(30)
