import pygame
from random import choice
import sys
from pygame.locals import *
from img import NewImage

BANDWIDTH = 4
BOARDHEIGHT = 4
TILESIZE = 80
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
FPS = 30
BLANK = None

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BRIGHTBLUE = (0, 50, 255)
DARKTURQUOISE = (3, 54, 73)
GREEN = (0, 204, 0)

BGCOLOR = DARKTURQUOISE
TILECOLOR = GREEN
TEXTCOLOR = WHITE
BORDERCOLOR = BRIGHTBLUE
BASICFONTSIZE = 20

BUTTONCOLOR = WHITE
BUTTONTEXTCOLOR = BLACK
MESSAGECOLOR = WHITE

XMARGIN = int((WINDOWWIDTH - (TILESIZE * BANDWIDTH + (BANDWIDTH - 1))) / 2)
YMARGIN = int((WINDOWHEIGHT - (TILESIZE * BOARDHEIGHT + (BOARDHEIGHT - 1))) / 2)

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'


class Tile(object):
    """
    Класс игровой плитки.
    Атрибуты:
    - координаты плитки (tilex, tiley)
    - порядковый номер плитки (number)
    - опциональные параметры adjx и adjy,
        которые позволяют сместить отображение плитки на игровом поле по горизонтали и вертикали соответственно.
    """
    def __init__(self, tilex, tiley, number, adjx=0, adjy=0):
        self.tilex = tilex
        self.tiley = tiley
        self.number = number
        self.adjx = adjx
        self.adjy = adjy
        self.drawTile()

    def drawTile(self):
        """
        Метод, отображающий плитку на игровом поле.

        Вычисляет положение левого верхнего угла плитки с помощью метода getLeftTopOfTile класса SlidingPuzzle.
        Затем загружает изображение для плитки с помощью pygame.image.load, используя имя файла,
        и создает поверхность rect_surface, на которую загружается изображение плитки.
        Далее используется метод blit, чтобы нарисовать изображение плитки на rect_surface.
        Отображает rect_surface на экране с помощью метода blit объекта DISPLAYSURF,
        применяя смещение adjx и adjy, если они указаны.
        """
        left, top = SlidingPuzzle.getLeftTopOfTile(self.tilex, self.tiley)
        image = pygame.image.load(f'images/{str(self.number)}.jpeg')
        rect_surface = pygame.Surface((80, 80))
        rect_surface.blit(image, (0, 0))
        DISPLAYSURF.blit(rect_surface, (left + self.adjx, top + self.adjy))


class SlidingPuzzle(object):
    """Основной класс игры."""
    def __init__(self):
        """
        Этот метод инициализирует игру, устанавливает окно игры, создает текстовые элементы для кнопок,
        генерирует начальное и решенное состояние игрового поля, а также создает пустой список для хранения всех ходов.
        Обрабатывает события (мышь и клавиатура).
        """
        global FPSCLOCK, DISPLAYSURF, BASICFONT, RESET_SURF, RESET_RECT, NEW_SURF, NEW_RECT, SOLVE_SURF, SOLVE_RECT, images

        images = []
        for i in range(15):
            images.append(pygame.image.load(f'images/{str(i + 1)}.jpeg'))

        pygame.init()
        FPSCLOCK = pygame.time.Clock()
        DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
        pygame.display.set_caption('Slide Puzzle')
        BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)

        RESET_SURF, RESET_RECT = self.makeText('Reset', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 90)
        NEW_SURF, NEW_RECT = self.makeText('New Game', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 60)
        SOLVE_SURF, SOLVE_RECT = self.makeText('Solve', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 30)

        mainBoard, solutionSeq = self.generateNewPuzzle(80)
        SOLVEDBOARD = self.getStartingBoard()
        allMoves = []

        while True:
            slideTo = None
            msg = 'Click tile or press arrow keys to slide.'
            if mainBoard == SOLVEDBOARD:
                """
                Если игровое поле (mainBoard) совпадает с решенным полем (SOLVEDBOARD),
                то сообщение обновляется на "Solved!"
                """
                msg = 'Solved!'

            self.drawBoard(mainBoard, msg)

            self.checkForQuit()
            for event in pygame.event.get():
                """Обработчик событий клика мыши."""
                if event.type == MOUSEBUTTONUP:
                    spotx, spoty = self.getSpotClicked(mainBoard, event.pos[0], event.pos[1])

                    if (spotx, spoty) == (None, None):
                        if RESET_RECT.collidepoint(event.pos):
                            self.resetAnimation(mainBoard, allMoves)
                            allMoves = []
                        elif NEW_RECT.collidepoint(event.pos):
                            mainBoard, solutionSeq = self.generateNewPuzzle(80)
                            allMoves = []
                        elif SOLVE_RECT.collidepoint(event.pos):
                            self.resetAnimation(mainBoard, solutionSeq + allMoves)
                            allMoves = []
                    else:
                        blankx, blanky = self.getBlankPosition(mainBoard)
                        if spotx == blankx + 1 and spoty == blanky:
                            slideTo = LEFT
                        elif spotx == blankx - 1 and spoty == blanky:
                            slideTo = RIGHT
                        elif spotx == blankx and spoty == blanky + 1:
                            slideTo = UP
                        elif spotx == blankx and spoty == blanky - 1:
                            slideTo = DOWN

                elif event.type == KEYUP:
                    """Обработчик событий нажатия кнопки на клавиатуре."""
                    if event.key in (K_LEFT, K_a) and self.isValidMove(mainBoard, LEFT):
                        slideTo = LEFT
                    elif event.key in (K_RIGHT, K_d) and self.isValidMove(mainBoard, RIGHT):
                        slideTo = RIGHT
                    elif event.key in (K_UP, K_w) and self.isValidMove(mainBoard, UP):
                        slideTo = UP
                    elif event.key in (K_DOWN, K_s) and self.isValidMove(mainBoard, DOWN):
                        slideTo = DOWN

            if slideTo:
                self.slideAnimation(mainBoard, slideTo, 'Click tile or press arrow keys to slide.', 8)
                self.makeMove(mainBoard, slideTo)
                allMoves.append(slideTo)
            pygame.display.update()
            FPSCLOCK.tick(FPS)

    @staticmethod
    def terminate():
        """Метод для выхода из приложения."""
        pygame.quit()
        sys.exit()

    def checkForQuit(self):
        """Метод, проверяющий закрытие окна (или нажатие клавиши ESCAPE)."""
        for event in pygame.event.get(QUIT):
            self.terminate()
        for event in pygame.event.get(KEYUP):
            if event.key == K_ESCAPE:
                self.terminate()
            pygame.event.post(event)

    @staticmethod
    def getStartingBoard():
        """Метод для отображения начального состояния игрового поля."""
        counter = 1
        board = []
        for x in range(BANDWIDTH):
            column = []
            for y in range(BOARDHEIGHT):
                column.append(counter)
                counter += BANDWIDTH
            board.append(column)
            counter -= BANDWIDTH * (BOARDHEIGHT - 1) + BANDWIDTH - 1

        board[BANDWIDTH - 1][BOARDHEIGHT - 1] = BLANK
        return board

    @staticmethod
    def getBlankPosition(board):
        """Метод, определяющий пустую ячейку на игровом поле. Возвращает ее позицию в виде кортежа (x, y)"""
        for x in range(BANDWIDTH):
            for y in range(BOARDHEIGHT):
                if board[x][y] == BLANK:
                    return x, y

    def makeMove(self, board, move):
        """Метод, чтобы сделать ход: переместить выбранный блок в пустую ячейку."""
        blankx, blanky = self.getBlankPosition(board)

        if move == UP:
            board[blankx][blanky], board[blankx][blanky + 1] = board[blankx][blanky + 1], board[blankx][blanky]
        elif move == DOWN:
            board[blankx][blanky], board[blankx][blanky - 1] = board[blankx][blanky - 1], board[blankx][blanky]
        elif move == LEFT:
            board[blankx][blanky], board[blankx + 1][blanky] = board[blankx + 1][blanky], board[blankx][blanky]
        elif move == RIGHT:
            board[blankx][blanky], board[blankx - 1][blanky] = board[blankx - 1][blanky], board[blankx][blanky]

    def isValidMove(self, board, move):
        """
        Метод, проверяющий является ли указанное направление движения допустимым,
        с учетом текущего положения пустой клетки.
        """
        blankx, blanky = self.getBlankPosition(board)
        return (move == UP and blanky != len(board[0]) - 1) or \
            (move == DOWN and blanky != 0) or \
            (move == LEFT and blankx != len(board) - 1) or \
            (move == RIGHT and blankx != 0)

    def getRandomMove(self, board, lastMove=None):
        """
        Метод, получающий текущее состояние игровой доски и последнее выполненное движение,
        а затем возвращающий случайное действие (UP, DOWN, LEFT, RIGHT),
        которое может быть сделано на доске, учитывая последнее выполненное движение и валидность хода.
        """
        validMoves = [UP, DOWN, LEFT, RIGHT]

        if lastMove == UP or not self.isValidMove(board, DOWN):
            validMoves.remove(DOWN)
        if lastMove == DOWN or not self.isValidMove(board, UP):
            validMoves.remove(UP)
        if lastMove == LEFT or not self.isValidMove(board, RIGHT):
            validMoves.remove(RIGHT)
        if lastMove == RIGHT or not self.isValidMove(board, LEFT):
            validMoves.remove(LEFT)

        return choice(validMoves)

    @staticmethod
    def getLeftTopOfTile(tileX, tileY):
        """
        Метод вычисляет координаты верхнего левого угла плитки игрового поля
        на основе заданных индексов плитки (tileX, tileY) и размера ячейки (TILESIZE).
        Затем возвращает кортеж с вычисленными координатами (left, top).
        """
        left = XMARGIN + (tileX * TILESIZE) + (tileX - 1)
        top = YMARGIN + (tileY * TILESIZE) + (tileY - 1)
        return left, top

    def getSpotClicked(self, board, x, y):
        """
        Метод принимает текущее состояние игрового поля (board) и координаты x, y.
        Затем перебирает все плитки на игровом поле и проверяет,
        на какую было произведено нажатие мышью (по координатам x, y).
        Если плитка найдена - функция возвращает ее индексы (tileX, tileY),
        если плитка не найдена - функция возвращает (None, None).
        """
        for tileX in range(len(board)):
            for tileY in range(len(board[0])):
                left, top = self.getLeftTopOfTile(tileX, tileY)
                tileRect = pygame.Rect(left, top, TILESIZE, TILESIZE)
                if tileRect.collidepoint(x, y):
                    return (tileX, tileY)
        return None, None

    @staticmethod
    def makeText(text, color, bgcolor, top, left):
        """Метод, отображающий текст (цвет текста, цвет фона, расположение)."""
        textSurf = BASICFONT.render(text, True, color, bgcolor)
        textRect = textSurf.get_rect()
        textRect.topleft = (top, left)
        return textSurf, textRect

    def drawBoard(self, board, message):
        """
        Метод, отрисовывающий игровое поле на основе переданной ей доски (board) и информационного сообщения (message).
        Заполняет экран цветом фона (BGCOLOR), отображает переданное сообщение (если оно есть).
        Отрисовывает плитки во всех клетках доски.
        Рисует рамку вокруг всего поля и отображает кнопки "reset", "new" и "solve" на экране.
        """
        DISPLAYSURF.fill(BGCOLOR)
        if message:
            textSurf, textRect = self.makeText(message, MESSAGECOLOR, BGCOLOR, 5, 5)
            DISPLAYSURF.blit(textSurf, textRect)

        for tilex in range(len(board)):
            for tiley in range(len(board[0])):
                if board[tilex][tiley]:
                    Tile(tilex, tiley, board[tilex][tiley])

        left, top = self.getLeftTopOfTile(0, 0)
        width = BANDWIDTH * TILESIZE
        height = BOARDHEIGHT * TILESIZE
        pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (left - 5, top - 5, width + 11, height + 11), 4)

        DISPLAYSURF.blit(RESET_SURF, RESET_RECT)
        DISPLAYSURF.blit(NEW_SURF, NEW_RECT)
        DISPLAYSURF.blit(SOLVE_SURF, SOLVE_RECT)

    def slideAnimation(self, board, direction, message, animationSpeed):
        """
        Метод для анимации перемещения плиток в игре.
        Принимает позицию плитки, направление и сообщение о перемещении.

        Цикл for проходит от 0 до TILESIZE с шагом animationSpeed
        и используется для пошагового изменения позиции плитки.
        На каждой итерации цикла происходит отрисовка игрового поля с учетом новой позиции плитки,
        затем вызывается pygame.display.update() для обновления экрана с учетом новых изменений,
        чтобы пользователь видел пошаговую анимацию перемещения.

        После каждой итерации также вызывается FPSCLOCK.tick(FPS) для контроля частоты обновления экрана
        с учетом фреймов в секунду (FPS) игры.
        Класс Tile используется для отрисовки плитки в новой позиции в соответствии с направлением перемещения.
        """
        blankx, blanky = self.getBlankPosition(board)
        if direction == UP:
            movex = blankx
            movey = blanky + 1
        elif direction == DOWN:
            movex = blankx
            movey = blanky - 1
        elif direction == LEFT:
            movex = blankx + 1
            movey = blanky
        elif direction == RIGHT:
            movex = blankx - 1
            movey = blanky

        self.drawBoard(board, message)
        baseSurf = DISPLAYSURF.copy()
        moveLeft, moveTop = self.getLeftTopOfTile(movex, movey)
        pygame.draw.rect(baseSurf, BGCOLOR, (moveLeft, moveTop, TILESIZE, TILESIZE))

        for i in range(0, TILESIZE, animationSpeed):
            self.checkForQuit()
            DISPLAYSURF.blit(baseSurf, (0, 0))
            if direction == UP:
                Tile(movex, movey, board[movex][movey], 0, -i)
            if direction == DOWN:
                Tile(movex, movey, board[movex][movey], 0, i)
            if direction == LEFT:
                Tile(movex, movey, board[movex][movey], -i, 0)
            if direction == RIGHT:
                Tile(movex, movey, board[movex][movey], i, 0)

            pygame.display.update()
            FPSCLOCK.tick(FPS)

    def generateNewPuzzle(self, numSlides):
        """
        Метод, генерирующая новую игру.
        Создает последовательность перемещений плиток на игровом поле, чтобы перемешать их и создать новый пазл.
        Метод возвращает состояние игрового поля после перемешивания и последовательность перемещений,
        которая была сделана для перемешивания.
        """
        sequence = []
        board = self.getStartingBoard()
        self.drawBoard(board, '')
        pygame.display.update()
        pygame.time.wait(500)
        lastMove = None
        for i in range(numSlides):
            move = self.getRandomMove(board, lastMove)
            self.slideAnimation(board, move, 'Generating new puzzle...', animationSpeed=int(TILESIZE / 3))
            self.makeMove(board, move)
            sequence.append(move)
            lastMove = move
        return board, sequence

    def resetAnimation(self, board, allMoves):
        """
        Анимация решения. Метод принимает два аргумента: игровое поле (board) и список всех ходов (allMoves).
        Создает инвентированную копию списка всех ходов. Для каждого хода вычисляется противоположное направление
        (операции UP/DOWN/RIGHT/LEFT). Проигрывается анимация перемещения в противоположном направлении
        с использованием функции slideAnimation с параметрами oppositeMove и заданной скоростью анимации.
        Выполняется ход в противоположном направлении с использованием функции makeMove.
        """
        revAllMoves = allMoves[:]
        revAllMoves.reverse()

        for move in revAllMoves:
            if move == UP:
                oppositeMove = DOWN
            elif move == DOWN:
                oppositeMove = UP
            elif move == RIGHT:
                oppositeMove = LEFT
            elif move == LEFT:
                oppositeMove = RIGHT
            self.slideAnimation(board, oppositeMove, '', animationSpeed=int(TILESIZE / 2))
            self.makeMove(board, oppositeMove)


if __name__ == '__main__':
    NewImage()
    SlidingPuzzle()
