import pygame
from Cell import Cell
class Board:


    def __init__(self, width, height, screen, difficulty, board):
        self.width = width
        self.height = height
        self.screen = screen
        self.difficulty = difficulty
        self.font = pygame.font.SysFont('Arial', 20)
        # self.cells = [[Cell(0, row, col, screen) for col in range(9)] for row in range(9)]
        self.cells = [[Cell(board[row][col], row, col, screen) for col in range(9)] for row in range(9)]
        self.board = board
        self.initial_state = board  # Store the initial state for reset purposes
        self.selected_cell = None

    def draw(self):
        for i in range(1, 9):
            if i % 3 == 0:
                pygame.draw.line(
                    self.screen,
                    "darkorange",
                    (0, i * 50),
                    (450, i * 50),
                    4
                )
            else:
                pygame.draw.line(
                    self.screen,
                    "black",
                    (0, i*50),
                    (450, i*50),
                    2
                )

        for i in range(1, 9):
            if i % 3 == 0:
                pygame.draw.line(
                    self.screen,
                    "darkorange",
                    (i*50, 0),
                    (i*50, 450),
                    4
                )
            else:
                pygame.draw.line(
                    self.screen,
                    "black",
                    (i * 50, 0),
                    (i * 50, 450),
                    2
                )

        pygame.draw.rect(self.screen, "black",
                         pygame.Rect(self.width / 2 - 450 / 2, self.height / 2 - 450 / 2, 450, 451), 4)

    def select(self, row, col):
        if self.selected_cell:
            self.selected_cell.selected = False

        self.selected_cell = self.cells[row][col]
        self.selected_cell.selected = True
        self.selected_cell.draw()

    def move_selection(self, dx, dy):
        if self.selected_cell:
            new_row, new_col = self.selected_cell.row + dy, self.selected_cell.col + dx
            if 0 <= new_row < 9 and 0 <= new_col < 9:  # Ensure new position is within the grid
                self.select(new_row, new_col)
    def click(self, x, y):
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return None
        cell_size = self.width // 9
        row = y // cell_size
        col = x // cell_size
        if 0 <= row < 9 and 0 <= col < 9:
            self.select(row, col)
            return (row, col)
        return None

    def clear(self):
        if self.selected_cell:
            self.selected_cell.set_cell_value(0)
            self.selected_cell.set_sketched_value(0)

    def sketch(self, value):
        if self.selected_cell:
            self.selected_cell.set_sketched_value(value)
            self.selected_cell.draw()


    def place_number(self, value):
        if self.selected_cell:
            self.selected_cell.set_cell_value(value)

    # def reset_to_original(self):
    #     for row in range(9):
    #         for col in range(9):
    #             self.cells[row][col].reset()
    def reset_to_original(self):
        """ Resets all cells to their initial state, ignoring cells that have not been changed by the user. """
        for i, row in enumerate(self.cells):
            for j, cell in enumerate(row):
                # x = cell.col * cell.width
                # y = cell.row * cell.height

                if cell.value != cell.initial_value:
                    cell.reset_to_initial()  # Reset each cell to its initial state

                self.board[i][j] = cell.value



    def clear_user_inputs(self):
        """ Clears all user inputs (values and sketches) from editable cells. """
        for row in self.cells:
            for cell in row:
                if cell.initial_value == 0:  # Check if the cell is editable
                    cell.value = 0
                    cell.sketch_value = None
                    cell.draw()  # Redraw cell to update its visual state


    def is_full(self):
        for row in range(9):
            for col in range(9):
                if self.cells[row][col].value == 0:
                    return False
        return True

    def update_board(self):
        for row in range(9):
            for col in range(9):
                self.board[row][col] = self.cells[row][col].value
    def find_empty(self):
        for row in range(9):
            for col in range(9):
                if self.cells[row][col].value == 0:
                    return (row, col)
        return None

    def check_board(self):
        for i in range(9):
            existing = set()
            for j in range(9):
                num = self.cells[i][j].value
                if num != 0:
                    if num in existing:
                        return False
                    existing.add(num)

        for j in range(9):
            existing = set()
            for i in range(9):
                num = self.cells[i][j].value
                if num != 0:
                    if num in existing:
                        return False
                    existing.add(num)

        for row in range(0,9,3):
            for col in range(0,9,3):
                existing = set()
                for i in range(row, row + 3):
                    for j in range(col, col + 3):
                        num = self.cells[i][j].value
                        if num != 0:
                            if num in existing:
                                return False
                            existing.add(num)
        return True


# FOR TESTING PURPOSES, UNCOMMENT TO TEST IT
# pygame.init()
# pygame.display.set_caption('Sudoku')
# screen = pygame.display.set_mode((450, 550))
# clock = pygame.time.Clock()
# running = True
#
# while running:
#     # poll for events
#     mouse = pygame.mouse.get_pos()
#     # pygame.QUIT event means the user clicked X to close your window
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#
#         if event.type == pygame.MOUSEBUTTONDOWN:
#
#             if 350 <= mouse[0] <= 400 and 500 <= mouse[1] <= 525:
#                 pygame.quit()
#                 break
#
#     # fill the screen with a color to wipe away anything from last
#
#     # RENDER YOUR GAME HERE
#     screen.fill("cornsilk")
#     board = Board(450, 450, screen, 'easy')
#     board.draw()
#     # flip() the display to put your work on screen
#     pygame.display.flip()
#
#     clock.tick(60)  # limits FPS to 60
#
# pygame.quit()
