'''
~ Steps followed to create the 2048 Console Game :

STEP 1 : We set up the board using a list of lists.
STEP 2 : We create functions that will merge left, right, up and down
STEP 3 : We Set up the start of the Game, creating an empty gameboard filled with two random values
STEP 4 : We set up the Rounds of the Game, where the user will have the option to merge in any one of the four
         directions, and after they move then new board will display.
STEP 5 : We set up adding a new value each time.
STEP 6 : We set up functions to test if the user has won or lost.

'''

import copy
import random

# This function will print out the board in the way we want
def display():
    # Finding out the largest value
    largest = board[0][0]
    for row in board:
        for element in row:
            if element > largest:
                largest = element

    # Setting the maximum number of spaces needed to the length of the largest value
    numSpaces = len(str(largest))

    print()
    for row in board:
        currentRow = "|"
        for element in row:
            # If the current element is 0, add spaces
            if element == 0:
                currentRow = currentRow + " " * numSpaces + "|"
            # If not, we should add the value
            else:
                currentRow = currentRow + (" " * (numSpaces - len(str(element)))) + str(element) + "|"
        # Print the generated row
        print(currentRow)
    print()

# This function merges one row left
def mergeOneRowLeft(row):
    # Move everything as far left to the left as possible
    for j in range(boardSize - 1):
        for i in range(boardSize - 1, 0, -1):
            # Test if there is an empty space , moveover if so,
            if row[i-1]==0:
                row[i-1] = row[i]
                row[i] = 0

    # Merge everything to the left
    for i in range(boardSize - 1):
        # Test if the current value is identical to the one next to it
        if row[i] == row[i+1]:
            row[i] = row[i] * 2
            row[i+1] = 0

    # Move everything to the left again
    for i in range(boardSize - 1, 0, -1):
        if row[i-1]==0:
            row[i-1] = row[i]
            row[i] = 0
    return row

# This function merges the whole board to the left
def merge_left(currentBoard):
    # Merge every row in the board left
    for i in range(boardSize):
        currentBoard[i] = mergeOneRowLeft(currentBoard[i])

    return currentBoard

# This function reverses the order of one row
def reverse(row):
    # Add all elements of the row to a new list in reverse order
    new = []
    for i in range(boardSize - 1, -1, -1):
        new.append(row[i])
    
    return new

# This function merges the whole board right
def merge_right(currentBoard):
    # Look at every row in the board
    for i in range(boardSize):
        # Reverse the row, then merge to the left, then reverse back
        currentBoard[i] = reverse(currentBoard[i])
        currentBoard[i] = mergeOneRowLeft(currentBoard[i])
        currentBoard[i] = reverse(currentBoard[i])

    return currentBoard
 
# This function transposes the whole board
def transpose(currentBoard):
    for j in range(boardSize):
        for i in range(j, boardSize):
            if not i == j:
                temp = currentBoard[j][i]
                currentBoard[j][i] = currentBoard[i][j]
                currentBoard[i][j] = temp

    return currentBoard

# This function merges the whole board up
def merge_up(currentBoard):
    # Transposes the whole board, then merges it all left, then transposes it back
    currentBoard = transpose(currentBoard)
    currentBoard = merge_left(currentBoard)
    currentBoard = transpose(currentBoard)

    return currentBoard

# This function merges the whole board down
def merge_down(currentBoard):
    # Transposes the whole board, then merges it all right, then transposes it back
    currentBoard = transpose(currentBoard)
    currentBoard = merge_right(currentBoard)
    currentBoard = transpose(currentBoard)

    return currentBoard


# This function picks a new value for the board
def pickNewValue():
    if random.randint(1, 8) == 1:
        return 4
    else:
        return 2

# This function adds a value to the board in one of the empty spaces
def addNewValue():
    rowNum = random.randint(0, boardSize-1)
    colNum = random.randint(0, boardSize-1)

    # Pick spots until we find one that is empty
    while not board[rowNum][colNum] == 0:
        rowNum = random.randint(0, boardSize-1)
        colNum = random.randint(0, boardSize-1)

    # Filling the empty spot with a new value
    board[rowNum][colNum] = pickNewValue()

# This function tests if the user has won
def won():
    for row in board:
        if finalValue in row:
            return True
    return False

# This Function tests if the user has lost
def noMoves():
    tempBoard1 = copy.deepcopy(board)
    tempBoard2 = copy.deepcopy(board)

    # Test every possible move
    tempBoard1 = merge_down(tempBoard1)
    if tempBoard1 == tempBoard2:
        tempBoard1 = merge_up(tempBoard1)
        if tempBoard1 == tempBoard2:
            tempBoard1 = merge_left(tempBoard1)
            if tempBoard1 == tempBoard2:
                return True
    return False

'''
MAIN GAME BUILDING STARTS 

One by one we call the different functions we just created in different combinations and 
sequences and create a empty board for the game to start.

'''

# Taking the user input for board size and final value to match on the board (2048 GAME or 4096 GAME)
boardSize = int(input(" Enter the Size of the Board in which you want to play (4X4) or (8X8) : "))
finalValue = int(input(" Enter the Value for which you want to play (2048 or 4096) : "))

# Creating a blank board
board = []
for i in range(boardSize):
    row = []
    for j in range(boardSize):
        row.append(0)
    board.append(row)

# Filling up two spots with random values, to start the game

numNeeded = 2
while(numNeeded>0):
    rowNum = random.randint(0, boardSize-1)
    colNum = random.randint(0, boardSize-1)

    if board[rowNum][colNum]==0:
        board[rowNum][colNum] = pickNewValue()
        numNeeded = numNeeded - 1

print("Welcome to 2048!! Your goal is to combine values to get the number 2048, by merging the board in different directions. Everytime, you will need to type 'd' to merge right, 'w' to merge up, 'a' to merge left, and 's' to merge down.\n\nHere is the starting board : ")
display()

gameOver = False

# Repeatedly asking the user for new moves while the game isn't over
while not gameOver:
    move = input("Which way do you want to merge? ")

    # Assume they entered a valid input
    validInput = True

    # Create a copy of the board
    tempBoard = copy.deepcopy(board)

    # Figure out which way the person wants to merge and use the correct function
    if move == "d":
        board = merge_right(board)
    elif move == "w":
        board = merge_up(board)
    elif move == "a":
        board = merge_left(board)
    elif move == "s":
        board = merge_down(board)
    else:
        validInput = False

    # If the input was not valid, they need to enter a new input, so this round is over
    if not validInput:
        print("Your input was not valid!! Try Again")
    # Otherwise their input was valid
    else:
        # Test if their move was unsuccessful
        if board == tempBoard:
            # Telling them to try again
            print("Try a Different Direction!!")
        else:
            # Test if the user has won
            if won():
                display()
                print("You Won!!")
                gameOver = True
            else:
                # Add a new value
                addNewValue()

                display()

                # Figuring out if they lost
                if noMoves():
                    print("Sorry, you have no more possible moves!! You Lose!!")
                    gameOver = True

