import numpy as np
import pygame
import sys
import math
import random

rowcount = 6
colcount = 7

emptySlot = 0
playerPiece = 1
botPiece = 2

# GAME LOGIC METHODS
def createBoard():
    board = np.zeros((rowcount,colcount))
    return board

def dropPiece(board, row, col, piece):
    board[row][col] = piece

def isValidLocation(board, col):
    if board[rowcount-1][col] == 0 and col in range(0, colcount):
        return True

def getNextOpenRow(board, col):
    for r in range(rowcount):
        if board[r][col] == 0:
            return r

def winValidator(board, piece):
    # HORIZONTAL WIN
    for r in range(rowcount):
        for c in range(colcount-3):
            if board[r][c] == board[r][c+1] == board[r][c+2] == board[r][c+3] and board[r][c] == piece:
                return True
    # VERTICAL WIN
    for c in range(colcount):
        for r in range(rowcount-3):
            if board[r][c] == board[r+1][c] == board[r+2][c] == board[r+3][c] and board[r][c] == piece:
                return True

    # NEGATIVELY SLOPED DIAGONAL WIN
    for r in range(3, rowcount):
        for c in range(colcount-3):
            if board[r][c] == board[r-1][c+1] == board[r-2][c+2] == board[r-3][c+3] and board[r][c] == piece:
                return True

    # POSITIVELY SLOPED DIAGONAL WIN

    for r in range(rowcount-3):
        for c in range(colcount-3):
            if board[r][c] == board[r+1][c+1] == board[r+2][c+2] == board[r+3][c+3] and board[r][c] == piece:
                return True

################################################################################

# GUI MODELING
pygame.init()
pygame.display.set_caption('Connect4 game')

def drawBoard(board):
    for c in range(colcount):
        for r in range(rowcount):
            pygame.draw.rect(screen, (0, 0, 255), ((c*100), (r*100+100), 100, 100) )
            pygame.draw.circle(screen, color=(0, 0, 0), center=((c*100+50), (r*100+150)), radius=40)
    for c in range(colcount):
        for r in range(rowcount):
            if board[r][c] == playerPiece:
                pygame.draw.circle(screen, color=(255, 0, 0), center=((c*100+50), 800-(r*100+150)), radius=40)
                pygame.draw.circle(screen, color=(0,0,0), center=((c*100+50), 800-(r*100+150)), radius=36, width=2)
            elif board[r][c] == botPiece:
                pygame.draw.circle(screen, color=(255, 255, 0), center=((c*100+50), 800-(r*100+150)), radius=40)
                pygame.draw.circle(screen, color=(0,0,0), center=((c*100+50), 800-(r*100+150)), radius=36, width=2)
            pygame.display.update()

def animate1(row, col):
    for i in range(1, rowcount-row+1):
        pygame.draw.rect(screen, color=(0, 0, 0), rect=(0, 0, 700, 100) )
        pygame.display.update()
        pygame.draw.circle(screen, color=(255,0,0), center=(col*100+50,i*100-50), radius=40)
        pygame.display.update()
        pygame.draw.circle(screen, color=(0,0,0), center=(col*100+50,i*100-50), radius=36, width=2)
        pygame.display.update()
        pygame.draw.circle(screen, color=(0,0,0), center=(col*100+50,i*100-50), radius=40)
        pygame.time.wait(50)
        pygame.display.update()

def animate2(row, col):
    for i in range(1, rowcount-row+1):
        pygame.draw.rect(screen, color=(0, 0, 0), rect=(0, 0, 700, 100) )
        pygame.display.update()
        pygame.draw.circle(screen, color=(255,255,0), center=(col*100+50,i*100-50), radius=40)
        pygame.display.update()
        pygame.draw.circle(screen, color=(0,0,0), center=(col*100+50,i*100-50), radius=36, width=2)
        pygame.display.update()
        pygame.draw.circle(screen, color=(0,0,0), center=(col*100+50,i*100-50), radius=40)
        pygame.time.wait(50)
        pygame.display.update()

width = colcount * 100
height = (rowcount+1) * 100
size = (width, height)
screen = pygame.display.set_mode(size)
winLength = 4

################################################################################

# MINIMAX ALGORITHM
def evalWindow(window, piece):
    score = 0
    opp = playerPiece
    if piece == playerPiece:
        opp = botPiece

    if window.count(piece) == 4:
        score += 10000
    elif window.count(piece) == 3 and window.count(emptySlot) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(emptySlot) == 2:
        score += 2

    if window.count(opp) == 3 and window.count(emptySlot) == 1:
        score -= 4


    return score

def scorePosition(board, piece):
    score = 0
    # favor center column over other columns
    centerList = [int(i) for i in list(board[:, colcount//2])]
    centerCount = centerList.count(piece)
    score += centerCount * 3

    for r in range(rowcount):
        rowList = [int(i) for i in list(board[r,:])]
        for c in range(colcount-3):
            window = rowList[c:c+winLength]
            score += evalWindow(window, piece)

    for c in range(colcount):
        colList = [int(i) for i in list(board[:,c])]
        for r in range(rowcount-3):
            window = colList[r:r+winLength]
            score += evalWindow(window, piece)

    for r in range(rowcount-3):
        for c in range(colcount-3):
            window = [board[r+i][c+i] for i in range(winLength)]
            score += evalWindow(window, piece)

    for r in range(rowcount-3):
        for c in range(colcount-3):
            window = [board[r+i][c-i] for i in range(winLength)]
            score += evalWindow(window, piece)

    return score

def getValidLocs(board):
    validLocs = []
    for col in range(colcount):
        if isValidLocation(board, col):
            validLocs.append(col)
    return validLocs

def pickBestMove(board, piece):
    validLocs = getValidLocs(board)
    bestScore = -1000000
    bestCol = random.choice(validLocs)

    for col in validLocs:
        row = getNextOpenRow(board, col)
        temp = board.copy()
        dropPiece(temp, row, col, piece)
        score = scorePosition(temp, piece)

        if score > bestScore:
            bestScore = score
            bestCol = col

    return bestCol

def isTerminalNode(board):
    if winValidator(board, playerPiece) or winValidator(board, botPiece) or (len(getValidLocs(board)) == 0) == True:
        return True

def minimax(board, depth, alpha, beta, maximizingPlayer):
    validLocs = getValidLocs(board)
    terminalNode = isTerminalNode(board)
    if depth == 0 or terminalNode:
        if terminalNode:
            if winValidator(board, botPiece):
                return (None, 100000000)
            elif winValidator(board, playerPiece):
                return (None, -100000000)
        else:
            return None, scorePosition(board, botPiece)

    if maximizingPlayer:
        score = -math.inf
        column = random.choice(validLocs)
        for col in validLocs:
            row = getNextOpenRow(board, col)
            temp = board.copy()
            dropPiece(temp, row, col, botPiece)
            newScore = minimax(temp, depth-1, alpha, beta, False)[1]
            if newScore > score:
                score = newScore
                column = col
            alpha = max(alpha, score)
            if alpha >= beta:
                break
        return column, score

    else:
        score = math.inf
        column = random.choice(validLocs)
        for col in validLocs:
            row = getNextOpenRow(board, col)
            temp = board.copy()
            dropPiece(temp, row, col, playerPiece)
            newScore = minimax(temp, depth-1, alpha, beta, True)[1]
            if newScore < score:
                score = newScore
                column = col
            beta = min(beta, score)
            if alpha >= beta:
                break
        return column, score

################################################################################

# MAIN FUNCTION
def main():
    board = createBoard()
    game_over = False
    turn = random.randint(0,1)

    drawBoard(board)
    pygame.display.update()

    while not game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # WHEN HOVERING
            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, color=(0,0,0), rect=(0, 0, width, 100))
                posx = event.pos[0]
                if turn == 0:
                    pygame.draw.circle(screen, color=(255,0,0), center=(posx,50), radius=40)
                    pygame.draw.circle(screen, color=(0,0,0), center=(posx,50), radius=36, width=2)

                pygame.display.update()

            # WHEN CLICKING
            if event.type == pygame.MOUSEBUTTONDOWN:
        # MOVES
                if turn == 0:
                    col = int(math.floor(posx/100))

                    if isValidLocation(board, col) == True:
                        row = getNextOpenRow(board, col)
                        animate1(row, col)
                        dropPiece(board, row, col, playerPiece)
                        turn += 1
                        drawBoard(board)

                    if winValidator(board, playerPiece) == True:
                        pygame.draw.rect(screen, color=(0, 0, 0), rect=(0, 0, 700, 100) )
                        pygame.display.update()
                        xfont = pygame.font.Font('freesansbold.ttf', 32)
                        winner = xfont.render(f'Game over! Player wins.', True, (255,255,255))
                        screen.blit(winner, (150, 40))
                        pygame.display.update()
                        pygame.time.wait(3500)
                        game_over = True

        if turn == 1 and not game_over:
            col, minimaxScore = minimax(board, 5, -math.inf, math.inf, True)

            if isValidLocation(board, col) == True:
                pygame.time.wait(random.randint(250, 750))
                row = getNextOpenRow(board, col)
                animate2(row, col)
                dropPiece(board, row, col, botPiece)
                turn -= 1
                drawBoard(board)

            if winValidator(board, botPiece) == True:
                pygame.draw.rect(screen, color=(0, 0, 0), rect=(0, 0, 700, 100) )
                pygame.display.update()
                xfont = pygame.font.Font('freesansbold.ttf', 32)
                winner = xfont.render(f'Game over! Bot wins.', True, (255,255,255))
                screen.blit(winner, (200, 40))
                pygame.display.update()
                pygame.time.wait(3500)
                game_over = True

main()
