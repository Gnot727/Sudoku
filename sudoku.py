import pygame
import sudoku_generator
from Cell import Cell
from Board import Board
from constants import *


def WelcomeScreen(screen, font):
    screen.fill('cornsilk')
    welcome = (font.render('Welcome to Sudoku', True, "black", ))
    large_font = pygame.font.SysFont('Times New Roman', 42)
    welcome_text_large = large_font.render('Welcome to Sudoku', True, "black")
    screen.blit(welcome_text_large, (50, 160))

    easy_button = pygame.draw.rect(screen, 'orange', (45, 300, 60, 30))
    medium_button = pygame.draw.rect(screen, 'orange', (196, 300, 80, 30))
    hard_button = pygame.draw.rect(screen, 'orange', (350, 300, 60, 30))

    screen.blit(font.render('easy', True, "white"), (52, 300))
    screen.blit(font.render('medium', True, "white"), (198, 300))
    screen.blit(font.render('hard', True, "white"), (359, 300))

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if easy_button.collidepoint(mouse_pos):
                return 'easy'
            if medium_button.collidepoint(mouse_pos):
                return 'medium'
            if hard_button.collidepoint(mouse_pos):
                return 'hard'


def draw_text(text, font, color, x, y, screen):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)


def WinLoseScreen(font, screen, board):
    screen.fill('cornsilk')
    if board.check_board() is True:
        pygame.display.set_caption('You Win!')
        draw_text("You Win!", font, 'orange', 225, 275, screen)
    else:
        pygame.display.set_caption('You Lose!')
        draw_text("You Lose!", font, 'orange', 225, 275, screen)

    restart_btn = pygame.Rect(175, 300, 100, 40)
    pygame.draw.rect(screen, 'orange', restart_btn)
    draw_text("Restart", font, 'white', restart_btn.centerx, restart_btn.centery, screen)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if restart_btn.collidepoint(mouse_pos):
                    return True
            if event.type == pygame.QUIT:
                return False


def update_board(sudoku, board, screen):
    screen.fill(PRIMARY_COLOR)
    for i, row in enumerate(sudoku):
        for j, col in enumerate(row):
            cell = Cell(col, i, j, screen)
            cell.draw()

    board.draw()
    pygame.display.flip()  # Update the entire screen to reflect changes


def main():
    pygame.init()
    font = pygame.font.SysFont(FONT, FONT_SIZE)
    pygame.display.set_caption('Sudoku')
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()
    running = True
    current_number = None

    screen.fill(PRIMARY_COLOR)

    difficulty = WelcomeScreen(screen, font)

    while not difficulty:
        difficulty = WelcomeScreen(screen, font)
        pygame.display.flip()

    removed = 0

    if difficulty == "easy":
        removed = 30
    elif difficulty == "medium":
        removed = 40
    elif difficulty == "hard":
        removed = 50

    sudoku = sudoku_generator.generate_sudoku(9, removed)
    board = Board(450, 450, screen, difficulty, sudoku)

    '''
    for i, row in enumerate(sudoku):
        for j, col in enumerate(row):
            if col != 0:
                cell = Cell(col, i, j, screen)
                cell.draw()

    board.draw()
    '''
    update_board(sudoku, board, screen)
    while running:
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

        resetBtn = pygame.Rect(45, 500, 60, 25)
        restartBtn = pygame.Rect(192.5, 500, 70, 25)
        exitBtn = pygame.Rect(350, 500, 50, 25)

        pygame.draw.rect(screen, SECONDARY_COLOR, resetBtn)
        pygame.draw.rect(screen, SECONDARY_COLOR, restartBtn)
        pygame.draw.rect(screen, SECONDARY_COLOR, exitBtn)

        screen.blit(font.render('reset', True, FONT_COLOR), (52, 500))
        screen.blit(font.render('restart', True, FONT_COLOR), (198, 500))
        screen.blit(font.render('exit', True, FONT_COLOR), (359, 500))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                clicked = board.click(mouse_pos[0], mouse_pos[1])
                update_board(sudoku, board, screen)
                if clicked:
                    board.select(*clicked)
                if resetBtn.collidepoint(mouse_pos):
                    board.reset_to_original()
                    sudoku = board.board
                    update_board(sudoku, board, screen)

                elif restartBtn.collidepoint(mouse_pos):
                    difficulty = WelcomeScreen(screen, font)
                    while not difficulty:
                        difficulty = WelcomeScreen(screen, font)
                        pygame.display.flip()
                    removed = 0
                    if difficulty == "easy":
                        removed = 30
                    elif difficulty == "medium":
                        removed = 40
                    elif difficulty == "hard":
                        removed = 50
                    sudoku = sudoku_generator.generate_sudoku(9, removed)
                    board = Board(450, 450, screen, difficulty, sudoku)
                    update_board(sudoku, board, screen)
                elif exitBtn.collidepoint(mouse_pos):
                    running = False
            elif event.type == pygame.KEYDOWN:
                update_board(sudoku, board, screen)
                if event.key == pygame.K_UP:
                    board.move_selection(0, -1)
                elif event.key == pygame.K_DOWN:
                    board.move_selection(0, 1)
                elif event.key == pygame.K_LEFT:
                    board.move_selection(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    board.move_selection(1, 0)

                if event.key == pygame.K_1:
                    current_number = 1
                    board.sketch(1)
                elif event.key == pygame.K_2:
                    current_number = 2
                    board.sketch(2)
                elif event.key == pygame.K_3:
                    current_number = 3
                    board.sketch(3)
                elif event.key == pygame.K_4:
                    current_number = 4
                    board.sketch(4)
                elif event.key == pygame.K_5:
                    current_number = 5
                    board.sketch(5)
                elif event.key == pygame.K_6:
                    current_number = 6
                    board.sketch(6)
                elif event.key == pygame.K_7:
                    current_number = 7
                    board.sketch(7)
                elif event.key == pygame.K_8:
                    current_number = 8
                    board.sketch(8)
                elif event.key == pygame.K_9:
                    current_number = 9
                    board.sketch(9)
                elif event.key == pygame.K_RETURN and not board.selected_cell.locked:
                    if current_number:
                        row, col = board.selected_cell.row, board.selected_cell.col
                        board.place_number(current_number)
                        # row, col = clicked[0],
                        # clicked[1]
                        sudoku[row][col] = current_number
                        update_board(sudoku, board, screen)
                        pygame.display.flip()
                        current_number = None

                if board.is_full():

                    WinLoseScreen(font, screen, board)

                    if WinLoseScreen(font, screen, board):
                        difficulty = WelcomeScreen(screen, font)
                        while not difficulty:
                            difficulty = WelcomeScreen(screen, font)
                            pygame.display.flip()
                        removed = 0
                        if difficulty == "easy":
                            removed = 30
                        elif difficulty == "medium":
                            removed = 40
                        elif difficulty == "hard":
                            removed = 50

                        sudoku = sudoku_generator.generate_sudoku(9, removed)
                        board = Board(450, 450, screen, difficulty, sudoku)
                        update_board(sudoku, board, screen)

        # flip() the display to put your work on screen
        #pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

    pygame.quit()


if __name__ == '__main__':
    main()
