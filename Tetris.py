#################################################
# hw7.py: Tetris!
#
# Your name: Aman Malik
# Your andrew id: amanm
#
# Your partner's name:Aashav
# Your partner's andrew id:ahmehta
#################################################

import cs112_f19_week7_linter
import math, copy, random

from cmu_112_graphics import *
from tkinter import *

#################################################
# Helper functions
#################################################

def almostEqual(d1, d2, epsilon=10**-7):
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)

import decimal
def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

#################################################
# Functions for you to write
#################################################
def gameDimensions():
    rows, cols, cellSize, margin = 15,10,20,25
    return (rows,cols,cellSize,margin)

def appStarted(app):
    app.gameOver = False
    app.score =0
    app.rows = gameDimensions()[0]
    app.cols = gameDimensions()[1]
    app.cellSize = gameDimensions()[2]
    app.margins = gameDimensions()[3]
    app.width = app.rows * app.cellSize
    app.height = app.cols * app.cellSize
    app.emptyColor = 'blue'
    app.board = make2dList(app) #creating a 2dList of all the emptyColor values
    #creating pieces
    # Seven "standard" pieces (tetrominoes)
    app.iPiece = [
        [  True,  True,  True,  True ]
    ]

    app.jPiece = [
        [  True, False, False ],
        [  True,  True,  True ]
    ]

    app.lPiece = [
        [ False, False,  True ],
        [  True,  True,  True ]
    ]

    app.oPiece = [
        [  True,  True ],
        [  True,  True ]
    ]

    app.sPiece = [
        [ False,  True,  True ],
        [  True,  True, False ]
    ]

    app.tPiece = [
        [ False,  True, False ],
        [  True,  True,  True ]
    ]

    app.zPiece = [
        [  True,  True, False ],
        [ False,  True,  True ]
    ]
    
    app.tetrisPieces = [ app.iPiece, app.jPiece, app.lPiece, app.oPiece,
    app.sPiece, app.tPiece, app.zPiece ]
    app.tetrisPieceColors = [ "red", "yellow", "magenta", "pink", "cyan",
    "green", "orange" ]
    newFallingPiece(app)
    
def make2dList(app):
    return [([app.emptyColor] * app.cols) for row in range(app.rows)]
    #instead of having a 2d List of zeros we need the emptyColor value stored
    #inside of the board 2dList
    #http://www.cs.cmu.edu/~112/notes/notes-2d-lists.html#creating2dLists

def drawBoard(app,canvas):
    for r in range(app.rows):
        for c in range(app.cols):
            drawCell(app,canvas,r,c,app.board[r][c])

def drawCell(app,canvas,row,col,color):
    x0,y0 = app.margins +(col*app.cellSize), app.margins+(row*app.cellSize)
    x1,y1 = (x0+app.cellSize), (y0+app.cellSize)
    canvas.create_rectangle(x0,y0,x1,y1,fill = color)

def moveFallingPiece(app,drow,dcol):
    app.fallingPieceRow += drow
    app.center += dcol
    if fallingPieceIsLegal(app):return True
    else:
        #here we undo our move if its not legal
        app.fallingPieceRow -= drow
        app.center-= dcol
        return False

def rotateFallingPiece(app):
    #creating temp variables
    oldRow = app.fallingPieceRow
    oldCol,oldPiece = app.center,app.fallingPiece
    oldNumRow,oldNumCol = len(app.fallingPiece), len(app.fallingPiece[0])
    #list comprehension to make a 2D List that will be the rotated version
    transpose = [[None]*oldNumRow for r in range(oldNumCol)]
    #creating a transposed piece
    for c in range(oldNumCol):
        for r in range(oldNumRow):
            transpose[c][r] = (oldPiece[r][c])
    #reversing our transposed piece
    transpose.reverse()
    #making the current piece to the new edit
    app.fallingPiece = transpose
    newNumRow,newNumCol= len(app.fallingPiece),len(app.fallingPiece[0])
    #mathforCentering
    newRow = oldRow + oldNumRow//2 - newNumRow//2
    newCol = oldCol + oldNumCol//2 - newNumCol//2
    app.fallingPieceRow = newRow
    app.center = newCol
    #check if the rotation is legal
    if fallingPieceIsLegal(app) == False:#if it isn't legal we undo our rotation
        app.fallingPieceRow = oldRow
        app.center = oldCol
        app.fallingPiece = oldPiece
   
def fallingPieceIsLegal(app):
    for r in range(len(app.fallingPiece)):
        for c in range(len(app.fallingPiece[0])):
            if app.fallingPiece[r][c] == True:
                newRow = app.fallingPieceRow + r
                newCol = app.center + c
                #if the peice is now out of the boundaries of our board
                if (newRow >=app.rows or newRow <0 or newCol>=app.cols or\
                newCol<0):return False
                #if the colors do not match
                elif app.board[newRow][newCol] != app.emptyColor:return False
    return True 

def keyPressed(app,event):
    if event.key=='r': #reset referenced from initSnakeandFood function in snake
    #http://www.cs.cmu.edu/~112/notes/notes-animations-part1.html#exampleSnake
        app.gameOver,app.score = False,0
        app.board = make2dList(app)
    elif app.gameOver == True: return
    elif event.key == "Right": moveFallingPiece(app,0,1)
    elif event.key == "Left": moveFallingPiece(app,0,-1)
    elif event.key == "Down": moveFallingPiece(app,1,0)
    elif event.key == "Up": rotateFallingPiece(app)
    #hard drop
    elif event.key == "d":
        while moveFallingPiece(app,1,0): pass

def newFallingPiece(app):
    randomIndex = random.randint(0, len(app.tetrisPieces) - 1)
    app.fallingPiece = app.tetrisPieces[randomIndex]
    app.fallingPieceColor = app.tetrisPieceColors[randomIndex]
    app.fallingPieceRow = 0
    app.middleCol = app.cols//2
    app.center = math.ceil(app.middleCol - 
    (len(app.fallingPiece[0]))//2)

def drawFallingPiece(app,canvas):
    for pieceRow in range(len(app.fallingPiece)):
        for pieceCol in range(len(app.fallingPiece[0])):
            if app.fallingPiece[pieceRow][pieceCol]==True:
                drawCell(app,canvas,pieceRow+app.fallingPieceRow,
                pieceCol+app.center,app.fallingPieceColor)

def placeFallingPiece(app):
    for pieceRow in range(len(app.fallingPiece)):
        for pieceCol in range(len(app.fallingPiece[0])):
            if app.fallingPiece[pieceRow][pieceCol]==True:
                app.board[pieceRow+app.fallingPieceRow][pieceCol+app.center]=\
                app.fallingPieceColor
    removeFullRows(app)

#helper function
def checkRow(app,row):
    for items in row:
        if items==app.emptyColor:return False
    return True

def removeFullRows(app):
    copy,counter=[],0
    for row in app.board:
        #checkRow is a helper functions that tells us if the row is filled
        if checkRow(app,row) == False:
            copy.append(row)
        else: counter +=1
    #adding the empty rows(replacing those that were removed)
    for c in range(counter):
        copy.insert(0,[app.emptyColor]*app.cols)
    app.board = copy   
    app.score += counter

def timerFired(app):
    if app.gameOver == False: 
        app.timerDelay = 475
        if moveFallingPiece(app,1,0) == False:
            placeFallingPiece(app)
            newFallingPiece(app)
            if not fallingPieceIsLegal(app): 
                app.gameOver=True
    
def redrawAll(app,canvas):
    canvas.create_rectangle(0,0,app.width,app.height,fill = 'orange')
    drawBoard(app,canvas)
    drawFallingPiece(app,canvas)
    #score display
    canvas.create_text(app.width/2,app.margins/2,text=f'Score: {app.score}')
    #gameOver display
    if app.gameOver == True:
        canvas.create_text(app.width/2,app.height/2,text='GAME OVER!!',\
        fill = 'black',font="Times 35 bold italic")

def playTetris():
    bWidth = gameDimensions()[1] * gameDimensions()[2] + 2*gameDimensions()[3]
    #number of columns multiplied by the cell size
    bHeight = gameDimensions()[0]*gameDimensions()[2] + 2*gameDimensions()[3]
    #number of rows multiplied by the cell size
    print('Replace this with your Tetris game!')


    runApp(width = bWidth,height = bHeight)
#################################################
# main
#################################################

def main():
    cs112_f19_week7_linter.lint()
    playTetris()

if __name__ == '__main__':
    main()
