from cgitb import text
import tkinter as tk
import colors as c
import random

class Game(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.grid()
        self.master.title("2048")

        # Making the Outline of the GUI
        self.main_grid = tk.Frame(self, bg=c.GRID_COLOR, bd=2.2, width=500, height=500) # Border of 3 pixels

        self.main_grid.grid(pady=(90, 0))

        self.make_GUI()

        self.start_Game()

        self.master.bind("<Left>", self.left)
        self.master.bind("<Right>", self.right)
        self.master.bind("<Up>", self.up)
        self.master.bind("<Down>", self.down)


        self.mainloop()

    def make_GUI(self):
        # Making a 4X4 Grid
        self.cells = []
        for i in range(grid_num):
            row = []
            for j in range(grid_num):
                cell_frame = tk.Frame(      # For each Cell in the grid, we create a cell frame
                    self.main_grid,
                    bg=c.EMPTY_CELL_COLOR,
                    width=150,
                    height=150
                )

                cell_frame.grid(row=i, column=j, padx=5, pady=5) # Calling grid on each Cell Frame
                cell_number = tk.Label(self.main_grid, bg=c.EMPTY_CELL_COLOR) # Used to display the number values on each cell
                cell_number.grid(row=i, column=j)
                cell_data = {"frame": cell_frame, "number": cell_number} # Creating a dictonary to store the data for the widgets
                row.append(cell_data)
            self.cells.append(row)

        # Making Score Header
        score_frame = tk.Frame(self)
        score_frame.place(relx=0.5, y=40, anchor="center")
        tk.Label(
            score_frame,
            text = "Score",
            font = c.SCORE_LABEL_FONT  
        ).grid(row=0)
        self.score_label = tk.Label(score_frame, text="0", font=c.SCORE_FONT) # Displaying the score
        self.score_label.grid(row=1)

    def start_Game(self):
        # Creating a Matrix of Zeroes
        self.matrix = [[0] * grid_num for _ in range(grid_num)]

        # Filling two random cells with 2s

        row = random.randint(0, 3)
        col = random.randint(0, 3)

        self.matrix[row][col] = 2

        self.cells[row][col]["frame"].configure(bg=c.CELL_COLORS[2])
        self.cells[row][col]["number"].configure(
             bg=c.CELL_COLORS[2],
             fg=c.CELL_NUMBER_COLORS[2],
             font=c.CELL_NUMBER_FONTS[2],
             text="2"
            )
        while(self.matrix[row][col] != 0):
            row = random.randint(0, 3)
            col = random.randint(0, 3)

        self.matrix[row][col] = 2
        self.cells[row][col]["frame"].configure(bg=c.CELL_COLORS[2])
        self.cells[row][col]["number"].configure(
            bg=c.CELL_COLORS[2],
            fg=c.CELL_NUMBER_COLORS[2],
            font=c.CELL_NUMBER_FONTS[2],
            text="2"
            )

        self.score = 0

    # Matrix Manipulation Functions

    # There are 4 Matrix functions which will be manipulating the Four by Four matrix we created in Start Game function
    # They will be called in different combinations and sequences based on the move by the player.
    # Each function will use a nested for loop to change the values and/or positions of the values in the matrix.


    # First function is stack - Stack will compress all non-zero numbers in the matrix towards one side of the board
    # eliminating all the gaps of empty cells between them.

    #Stack Function to compress to the left side 
    def stack(self):
        new_matrix = [[0] * grid_num for _ in range(grid_num)]
        for i in range(grid_num):
            fill_position = 0
            for j in range(grid_num):
                if self.matrix[i][j] != 0:
                    new_matrix[i][fill_position] = self.matrix[i][j]
                    fill_position = fill_position + 1

        self.matrix = new_matrix

    # Combine Function -  It adds together all horizontally adjacent non-zero numbers of the same value in the matrix
    # and merges them to the left position.

    def combine(self):
        for i in range(grid_num):
            for j in range(grid_num-1):
                if self.matrix[i][j] != 0 and self.matrix[i][j] == self.matrix[i][j+1]:
                    self.matrix[i][j] = self.matrix[i][j] * 2
                    self.matrix[i][j+1] = 0
                    self.score = self.score + self.matrix[i][j]


    # Reverse Function or Method - It will reverse the order of each row in the matrix

    def reverse(self):
        new_matrix = []
        for i in range(grid_num):
            new_matrix.append([])
            for j in range(grid_num):
                new_matrix[i].append(self.matrix[i][3-j])

        self.matrix = new_matrix

    # Last Function is the Transpose Method - It will flip the matrix over it's diagonal.

    def transpose(self):
        new_matrix = [[0] * grid_num for _ in range(grid_num)]
        for i in range(grid_num):
            for j in range(grid_num):
                new_matrix[i][j] = self.matrix[j][i]

        self.matrix = new_matrix

    # A function to randomly add a new tile to the matrix after each move - Add a new 2 or 4 title randomly to an empty cell

    def add_new_tile(self):
        row = random.randint(0, 3)
        col = random.randint(0, 3)

        while(self.matrix[row][col] != 0):
            row = random.randint(0, 3)
            col = random.randint(0, 3)
        self.matrix[row][col] = random.choice([2, 4])


    # Update the GUI to match the Matrix
    def update_GUI(self):
        for i in range(grid_num):
            for j in range(grid_num):
                cell_value = self.matrix[i][j]
                if cell_value == 0:
                    self.cells[i][j]["frame"].configure(bg=c.EMPTY_CELL_COLOR)
                    self.cells[i][j]["number"].configure(bg=c.EMPTY_CELL_COLOR, text="")
                else:
                    self.cells[i][j]["frame"].configure(bg=c.CELL_COLORS[cell_value])
                    self.cells[i][j]["number"].configure(
                        bg=c.CELL_COLORS[cell_value],
                        fg=c.CELL_NUMBER_COLORS[cell_value],
                        font=c.CELL_NUMBER_FONTS[cell_value],
                        text=str(cell_value)
                        )

        self.score_label.configure(text=self.score) # Updating the Score display
        self.update_idletasks() 


    # Visualizing how each of these moves will be played out

    # Arrow-Press Functions

    def left(self, event):
        self.stack()
        self.combine()
        self.stack()
        self.add_new_tile()
        self.update_GUI()
        self.game_over()

    def right(self, event):
        self.reverse()
        self.stack()
        self.combine()
        self.stack()
        self.reverse()
        self.add_new_tile()
        self.update_GUI()
        self.game_over()

    def up(self, event):
        self.transpose()
        self.stack()
        self.combine()
        self.stack()
        self.transpose()
        self.add_new_tile()
        self.update_GUI()
        self.game_over()

    def down(self, event):
        self.transpose()
        self.reverse()
        self.stack()
        self.combine()
        self.stack()
        self.reverse()
        self.transpose()
        self.add_new_tile()
        self.update_GUI()
        self.game_over()


    # Check if any moves are possible

    def horizontal_move_exists(self):
        for i in range(grid_num):
            for j in range(grid_num-1):
                if self.matrix[i][j] == self.matrix[i][j+1]:
                    return True
        return False
    
    def vertical_move_exists(self):
        for i in range(grid_num-1):
            for j in range(grid_num):
                if self.matrix[i][j] == self.matrix[i+1][j]:
                    return True
        return False
    
    # Check if Game is over (Win/Lose)

    def game_over(self):
        if any(final_num in row for row in self.matrix):  # If the player won, which means 2048 is on the board
            game_over_frame = tk.Frame(self.main_grid, borderwidth=2)
            game_over_frame.place(relx=0.5, rely=0.5, anchor="center")
            tk.Label( game_over_frame, text="You Win!!", bg=c.WINNER_BG,
                fg=c.GAME_OVER_FONT_COLOR,
                font=c.GAME_OVER_FONT).pack()

        elif not any(0 in row for row in self.matrix) and not self.horizontal_move_exists() and not self.vertical_move_exists(): # If the board is occupied and no legal moves remain for the player
            game_over_frame = tk.Frame(self.main_grid, borderwidth=2)
            game_over_frame.place(relx=0.5, rely=0.5, anchor="center")
            tk.Label(
                game_over_frame,
                text="Game Over!!",
                bg=c.LOSER_BG,
                fg=c.GAME_OVER_FONT_COLOR,
                font=c.GAME_OVER_FONT
            ).pack()

final_num = int(input("Enter the winning number (2048 or 4096) : "))
grid_num = int(input("Enter the number for the dimensions of the grid (4X4) or (8X8) : "))

def main():
    Game()

if __name__ == "__main__":
    main()

                    








