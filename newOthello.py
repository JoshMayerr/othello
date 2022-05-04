import turtle
import random
import math

from numpy import Infinity

t = turtle.Turtle()
s = turtle.Screen()

computer = 'white'

start = (-256, 256)
squareLength = 64
sideLength = 512

s.tracer(0,0)

def baseBoard():
    t.clear()
    t.speed(10)
    t.penup()
    t.fillcolor('green')
    t.goto(start)
    t.begin_fill()
    t.pendown()
    t.goto(256, 256)
    t.goto(256, -256)
    t.goto(-256, -256)
    t.end_fill()
    t.penup()

def drawBoard():
    for j in range(8):
        t.pendown()
        t.left(90)
        t.forward(sideLength)
        t.right(90)
        t.forward(squareLength)
        t.right(90)
        t.forward(sideLength)
        t.right(90)
        t.forward(squareLength)
        t.right(90)
        for l in range(8):
            for i in range(4):
                t.forward(squareLength)
                t.right(90)
                i+=1
            t.forward(squareLength)
            l += 1
        t.right(90)
        t.forward(squareLength)
        t.right(90)
        t.forward(sideLength)
        t.left(90)
        j+=1

def whichRow(y):
    if 256>y>192:
        return 0
    elif 192>y>128:
        return 1
    elif 128>y>64:
        return 2
    elif 64>y>0:
        return 3
    elif 0>y>-64:
        return 4
    elif -64>y>-128:
        return 5
    elif -128>y>-192:
        return 6
    elif -192>y>-256:
        return 7

def whichColumn(x):
    if 256>x>192:
        return 7
    elif 192>x>128:
        return 6
    elif 128>x>64:
        return 5
    elif 64>x>0:
        return 4
    elif 0>x>-64:
        return 3
    elif -64>x>-128:
        return 2
    elif -128>x>-192:
        return 1
    elif -192>x>-256:
        return 0

def yFromRow(r):
    if r == 0:
        return (256+192)/2
    elif r == 1:
        return (192+128)/2
    elif r == 2:
        return (128+64)/2
    elif r == 3:
        return (64+0)/2
    elif r == 4:
        return (0-64)/2
    elif r == 5:
        return (-64-128)/2
    elif r == 6:
        return (-128-192)/2
    elif r == 7:
        return (-192-256)/2

def xFromColumn(c):
    if c == 7:
        return (256+192)/2
    elif c == 6:
        return (192+128)/2
    elif c == 5:
        return (128+64)/2
    elif c == 4:
        return (64+0)/2
    elif c == 3:
        return (0-64)/2
    elif c == 2:
        return (-64-128)/2
    elif c == 1:
        return (-128-192)/2
    elif c == 0:
        return (-192-256)/2

def stampPlayer(row, column, player):
    t.penup()
    t.goto(xFromColumn(column), yFromRow(row))
    t.color(player)
    t.shape("circle")
    t.shapesize(1.5,1.5,1.5)
    t.stamp()

baseBoard()
drawBoard()


def updateBoard(board, player, row, col):
    board[row][col] = player
    return board

def calculateScore(board, player):
    count = 0
    for row in board:
        for col in row:
            if col == player:
                count += 1
    return count

def updateScore(board):
    t.penup()
    b = calculateScore(board, 'black')
    w = calculateScore(board, 'white')
    t.goto(-256, 300)
    t.color('black')
    t.write('Black Score: ' + str(b))
    t.forward(75)
    t.write('White Score: ' + str(w))
    t.forward(75)

# reset the canvas and draw board given game state
def updateCanvas(board):
    baseBoard()
    drawBoard()
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == 'black' or board[row][col] == 'white':
                stampPlayer(row, col, board[row][col])
    return


def isOnBoard(row, col):
    return col >= 0 and col <= 7 and row >= 0 and row <= 7

def notOutOfBounds(x, y):
    return x >= -256 and x <= 256 and y >= -256 and y <= 256

directions = [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]

def validMove(board, player, row, col):
    if board[row][col] != 0 or not isOnBoard(col, row):
        return False
    board[row][col] = player
    tilesToFlip = []
    for xdirection, ydirection in directions:
        x, y = row, col
        x += xdirection
        y += ydirection
        if isOnBoard(x, y) and board[x][y] == opp(player):
            x += xdirection
            y += ydirection
            if not isOnBoard(x, y):
                continue
            while board[x][y] == opp(player): # go until u find the same piece
                x += xdirection
                y += ydirection
                if not isOnBoard(x, y):
                    break
            if not isOnBoard(x, y):
                continue
            if board[x][y] == player: # go get the tiles to flip
                while True:
                    x -= xdirection
                    y -= ydirection
                    if x == row and y == col:
                        break
                    tilesToFlip.append([x, y])
    board[row][col] = 0
    if len(tilesToFlip) == 0:
        return False
    return tilesToFlip

def allMoves(board, player):
    # return [[row, col] for row in board for col in board[row] if validMove(board, player, row, col)]
    list = [[[row,col] for col in range(len(board[row])-1) if validMove(board, player, row, col)] for row in range(len(board)-1)]
    temp = []
    for x in range(len(list)):
        if len(list[x]) > 0:
            temp += list[x]
    return temp


def flipPieces(board, flipList):
    for tile in flipList:
        board[tile[0]][tile[1]] = opp(board[tile[0]][tile[1]])
    return board

def nextBoard(board, player, move):
    flipList = validMove(board, player, move[0], move[1])
    newBoard = updateBoard(board, player, move[0], move[1])
    return flipPieces(newBoard, flipList)

def randomMove(board, player):
    if allMoves(board, player):
        moves = allMoves(board, player)
        return random.choice(moves)
    return

def playerPieces(board, player):
    pieces = []
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == player:
                pieces.append([row, col])
    return pieces

def emptyDirections():
    # return how many of the directions are open
    # for xdirection, ydirection in directions:
    return

def opp(player):
    if player == 'black':
        return 'white'
    else:
        return 'black'

SQUARE_WEIGHTS2 = [
    [120, -20,  20,   5,   5,  20, -20, 120],
    [-20, -40,  -5,  -5,  -5,  -5, -40, -20],
    [20,  -5,  15,   3,   3,  15,  -5,  20],
    [5,  -5,   3,   3,   3,   3,  -5,   5],
    [5,  -5,   3,   3,   3,   3,  -5,   5],
    [20,  -5,  15,   3,   3,  15,  -5,  20],
    [-20, -40,  -5,  -5,  -5,  -5, -40, -20],
    [120, -20,  20,   5,   5,  20, -20, 120]
]

SQUARE_WEIGHTS = [
    [20, -3, 11, 8, 8, 11, -3, 20],
    [-3, -7, -4, 1, 1, -4, -7, -3],
    [11, -4, 2, 2, 2, 2, -4, 11],
    [8, 1, 2, -3, -3, 2, 1, 8],
    [8, 1, 2, -3, -3, 2, 1, 8],
    [11, -4, 2, 2, 2, 2, -4, 11],
    [-3, -7, -4, 1, 1, -4, -7, -3],
    [20, -3, 11, 8, 8, 11, -3, 20]
]

def evaluate2(board, player):
    playerTotal = 0
    for row,col in playerPieces(board, player):
        playerTotal += SQUARE_WEIGHTS[row][col]
    # frontier disksmultiplier
    return playerTotal

def evaluate(board, player):
    oppo = opp(player)
    p = 0
    c = 0
    l = 0
    m = 0
    f = 0
    d = 0
    playerTiles = 0
    oppTiles = 0
    x1 = [-1, -1, 0, 1, 1, 1, 0, -1]
    y1 = [0, 1, 1, 1, 0, -1, -1, -1]
    playerFrontTiles = 0
    oppFrontTiles = 0
    for i in range(8):
        for j in range(8):
            if board[i][j] == player:
                d += SQUARE_WEIGHTS[i][j]
                playerTiles += 1
            elif board[i][j] == oppo:
                d -= SQUARE_WEIGHTS[i][j]
                oppTiles += 1
            if board[i][j] != 0:
                for k in range(8):
                    x = i + x1[k]
                    y = j + y1[k]
                    if x >= 0 and x < 8 and y >= 0 and y < 8 and board[x][y] == 0:
                        if board[i][j] == player:
                            playerFrontTiles += 1
                        else:
                            oppFrontTiles += 1
                            break
    print(playerTiles, oppTiles)
    if playerTiles > oppTiles:
            p = (100.0 * playerTiles)/(playerTiles + oppTiles)
    elif playerTiles < oppTiles:
        p = -(100.0 * oppTiles)/(playerTiles + oppTiles)
    else:
        p = 0

    if playerFrontTiles > oppFrontTiles:
        f = -(100.0 * playerFrontTiles)/(playerFrontTiles + oppFrontTiles)
    elif playerFrontTiles < oppFrontTiles:
        f = (100.0 * oppFrontTiles)/(playerFrontTiles + oppFrontTiles)
    else:
        f = 0

    # corner occupancy
    playerTiles = 0
    oppTiles = 0
    if board[0][0] == player:
        playerTiles+=1
    elif board[0][0] == oppo:
        oppTiles+=1
    if board[0][7] == player:
        playerTiles+=1
    elif board[0][7] == oppo:
        oppTiles+=1
    if board[7][0] == player:
        playerTiles+=1
    elif board[7][0] == oppo:
        oppTiles+=1
    if board[7][7] == player:
        playerTiles+=1
    elif board[7][7] == oppo:
        oppTiles+=1
    c = 25 *  playerTiles - oppTiles

    # corner closeeness
    playerTiles = 0
    oppTiles = 0
    if board[0][0] == '0':
        if(board[0][1] == player): playerTiles+=1
        elif(board[0][1] == oppo): oppTiles+=1
        if(board[1][1] == player): playerTiles+=1
        elif(board[1][1] == oppo): oppTiles+=1
        if(board[1][0] == player): playerTiles+=1
        elif(board[1][0] == oppo): oppTiles+=1
    if(board[0][7] == '0'):
        if(board[0][6] == player): playerTiles+=1
        elif(board[0][6] == oppo): oppTiles+=1
        if(board[1][6] == player): playerTiles+=1
        elif(board[1][6] == oppo): oppTiles+=1
        if(board[1][7] == player): playerTiles+=1
        elif(board[1][7] == oppo): oppTiles+=1
    if(board[7][0] == '0'):
        if(board[7][1] == player): playerTiles+=1
        elif(board[7][1] == oppo): oppTiles+=1
        if(board[6][1] == player): playerTiles+=1
        elif(board[6][1] == oppo): oppTiles+=1
        if(board[6][0] == player): playerTiles+=1
        elif(board[6][0] == oppo): oppTiles+=1
    if(board[7][7] == '-'):
        if(board[6][7] == player): playerTiles+=1
        elif(board[6][7] == oppo): oppTiles+=1
        if(board[6][6] == player): playerTiles+=1
        elif(board[6][6] == oppo): oppTiles+=1
        if(board[7][6] == player): playerTiles+=1
        elif(board[7][6] == oppo): oppTiles+=1
    l = -12.5 * (playerTiles - oppTiles)

    playerTiles = len(allMoves(board, player))
    oppTiles = len(allMoves(board, oppo))
    if playerTiles > oppTiles:
        m = (100.0 * playerTiles)/(playerTiles + oppTiles)
    elif playerTiles < oppTiles:
        m = -(100.0 * oppTiles)/(playerTiles + oppTiles)
    else:
        m = 0

    print('p:', p, c, l, m, f, d)
    score = (10 * p) + (801.724 * c) + (382.026 * l) + (78.922 * m) + (74.396 * f) + (10 * d)
    return score

def checkWinner(board):
    # check for filled board
    # check for no valid moves
    if not allMoves(board, 'white') or not allMoves(board, 'black'):
        if calculateScore(board, 'white') > calculateScore(board, 'black'):
            return 'white'
        else:
            return 'black'
    return None

scores = {
    'black': -Infinity,
    'white': Infinity,
    'tie': 0
}

def minimax(board, depth, player, isMaximizing, alpha, beta):
    result = checkWinner(board)
    moves = allMoves(board, player)
    # print(result)
    if depth == 0 or not moves:
        if result:
            return scores[result]
        # print(evaluate(board, player), 'player')
        # print(evaluate(board, 'black'), 'blakc')
        # print(evaluate(board, 'white'), 'white')
        return evaluate(board, 'white')
    if isMaximizing:
        bestScore = -Infinity
        for row, col in moves:
            board[row][col] = player
            score = minimax(board, depth - 1, opp(player), False, alpha, beta)
            board[row][col] = 0
            bestScore = max(score, bestScore)
            alpha = max(alpha, bestScore)
            if beta <= alpha:
                break
        return bestScore
    else:
        bestScore = Infinity
        for row, col in moves:
            board[row][col] = player
            score = minimax(board, depth - 1, opp(player), True, alpha, beta)
            board[row][col] = 0
            bestScore = min(score, bestScore)
            beta = min(beta, bestScore)
            if beta <= alpha:
                break
        return bestScore

def bestMove(board, depth, player):
    moves = allMoves(board, player)
    move = moves[0]
    bestScore = -Infinity
    for row, col in moves:
        board[row][col] = player
        score = minimax(board, depth-1, opp(player), True, -Infinity, Infinity)
        board[row][col] = 0
        if score > bestScore:
            bestScore = score
            move = [row, col]
    return move

# print(bestMove(gameBoard, 5, 'white'))

def initialize():
    gameBoard = [[0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 'black', 'white', 0, 0, 0],
             [0, 0, 0, 'white', 'black', 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],]
    baseBoard()
    drawBoard()
    # updateBoard(gameBoard)
    updateCanvas(gameBoard)
    return gameBoard

gameBoard = initialize()

def onMove(x, y):
    if notOutOfBounds(x, y):
        row = whichRow(y)
        col = whichColumn(x)
        if validMove(gameBoard, "black", row, col):
            # PLAYER MOVE
            nextBoard(gameBoard, "black", [row, col])
            updateCanvas(gameBoard)
            updateScore(gameBoard)
            # AI MOVE
            AImove = bestMove(gameBoard, 4, computer)
            print(AImove)
            nextBoard(gameBoard, computer, [AImove[0], AImove[1]])
            updateCanvas(gameBoard)
            updateScore(gameBoard)
            # else:
            #     print(checkWinner(gameBoard))
            #     initialize()
            #     return

            # CPU MOVE RANDOM
            # random = randomMove(gameBoard, 'white')
            # if random:
            #     nextBoard(gameBoard, "white", [random[0], random[1]])
            #     updateCanvas(gameBoard)
            #     updateScore(gameBoard)

# onclick action
s.onclick(onMove)
s.mainloop()
