import pygame

"""
Class to create and print
out a Sudoku board.
"""

class Board():
    """
    Takes in the parameter grid, sets
    all values of it to 0, and initializes
    the variables row, col, box, and done.
    """

    def __init__(self, grid=[]):
        grid = []
        row = []
        col = []
        box = []
        for i in range(10):
            grid.append([])
            row.append([])
            col.append([])
            box.append([])
        for i in range(10):
            for j in range(10):
                grid[i].append(0)
                row[i].append(False)
                col[i].append(False)
                box[i].append(False)
        self.grid = grid
        self.row = row
        self.col = col
        self.box = box
        self.done = False

    """
    Updates the coordinates
    to the user inputted values.
    """

    def update(self, coordinate_x, coordinate_y, value):
        self.grid[coordinate_x][coordinate_y] = value

    """
    Checks to see if the initial
    grid entered by the user is valid>
    """

    def __repr__(self):
        if (self.done == True):
            grid = self.grid
            return_grid = ''
            for i in range(9):
                for j in range(9):
                    return_grid = return_grid + str(grid[i][j]) + ' '
                return_grid = return_grid + "\n"
            return return_grid
        else:
            return "The starting board you gave was unsolvable"

    """
    Takes in the parameters self and position_hash and
    uses the bactracking algorithm to solve the board.
    """

    def solve(self, position_hash):
        if (position_hash == 81):
            self.done = True
        if (self.done == True):
            return
        # print self, position_hash
        coordinate_x = position_hash / 9
        coordinate_y = position_hash % 9
        if (self.grid[coordinate_x][coordinate_y] == 0):
            for i in range(1, 10):
                if (self.row[coordinate_x][i] == True or self.col[coordinate_y][i] == True
                    or self.box[(coordinate_x / 3) * 3 + coordinate_y / 3][i] == True):
                    continue
                else:
                    self.update(coordinate_x, coordinate_y, i)
                    self.row[coordinate_x][i] = True
                    self.col[coordinate_y][i] = True
                    self.box[(coordinate_x / 3) * 3 + coordinate_y / 3][i] = True
                    self.solve(position_hash + 1)
                    if (self.done == True):
                        return
                    self.row[coordinate_x][i] = False
                    self.col[coordinate_y][i] = False
                    self.box[(coordinate_x / 3) * 3 + coordinate_y / 3][i] = False
                    self.grid[coordinate_x][coordinate_y] = 0
        else:
            self.solve(position_hash + 1)

    """
    Creates a sudoku board and displays
    the solved board onto the screen.
    """
    def display(self):
        # Initializes the output screen
        pygame.init()
        pygame.font.init()
        WINDOW_SIZE = [360, 360]
        screen = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption("Sudoku Solver")
        screen.fill((255, 255, 255))
        clock = pygame.time.Clock()
        done = False
        while (done == False):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
            # Draws the sudoku board
            for x in range(0, 360, 40):  # Draw vertical lines
                pygame.draw.line(screen, (200, 200, 200), (x, 0), (x, 360))
            for y in range(0, 360, 40):  # Draw horizontal lines
                pygame.draw.line(screen, (200, 200, 200), (0, y), (360, y))

            for x in range(0, 360, 120):
                pygame.draw.line(screen, (0, 0, 0), (x, 0), (x, 360))
            for y in range(0, 360, 120):
                pygame.draw.line(screen, (0, 0, 0), (0, y), (360, y))

            # Displays the solved sudoku board
            myfont = pygame.font.SysFont('Comic Sans MS', 20)
            y_display = 7
            for i in range(1, 10):
                x_display = 15
                for j in range(1, 10):
                    if (self.grid[i-1][j-1] != 0):
                        textsurface = myfont.render(str(self.grid[i - 1][j - 1]), False, (0, 0, 0))
                        screen.blit(textsurface, (x_display, y_display))
                    x_display += 40
                y_display += 40
            clock.tick(60)
            pygame.display.flip()
        pygame.quit()

"""
Main fucntion loop. Asks the user to input
values for a certain coordinates and calls
the Board.solve and Board.display methods.
"""

def main():
    sudoku = Board()
    num_input = int(input("Number of coordinates to update: "))
    while (num_input > 0):
        coordinate_x, coordinate_y = (raw_input("What coordinates do you want to update: ").split())
        coordinate_x = eval(coordinate_x) - 1
        coordinate_y = eval(coordinate_y) - 1
        value = eval(raw_input("What value do you want to update it to: "))
        if (sudoku.row[coordinate_x][value] == True or sudoku.col[coordinate_y][value] == True
            or sudoku.box[(coordinate_x / 3) * 3 + coordinate_y / 3][value] == True):
            print "That is not a valid position, if you put that there, the grid is unsolvable"
            continue
        sudoku.row[coordinate_x][value] = True
        sudoku.col[coordinate_y][value] = True
        sudoku.box[(coordinate_x / 3) * 3 + coordinate_y / 3][value] = True
        sudoku.update(coordinate_x, coordinate_y, value)
        num_input -= 1
    sudoku.display()
    sudoku.solve(0)
    sudoku.display()
main()
