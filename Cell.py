#cell class
import pygame

class Cell:
    def __init__(self, initial_value, row, col, screen):
        self.initial_value = initial_value  # Store the initial value
        self.value = initial_value
        self.row = row
        self.col = col
        self.screen = screen
        self.width = 50
        self.height = 50
        self.selected = False
        self.sketch_value = None
        self.outline = None
        self.locked = self.initial_value != 0
        self.error = False

    def set_cell_value(self, value):
        if not self.locked:

                self.value = value
                self.draw()


    def reset_to_initial(self):
        """ Resets the cell to its initial value. """
        print(f"Resetting cell at ({self.row}, {self.col}) from {self.value} to {self.initial_value}")
        print(self.value, self.initial_value)
        self.value = self.initial_value
        self.sketch_value = None

    def set_sketched_value(self, value):
        self.sketch_value = value


    def draw(self):
        font = pygame.font.Font(None, 36)
        x = self.col * self.width
        y = self.row * self.height

        # Determine cell background color
        if self.initial_value == 0:
            bg_color = pygame.Color('white')
        else:
            bg_color = pygame.Color('cornsilk')

        # Draw cell outline
        pygame.draw.rect(self.screen, bg_color, (x, y, self.width, self.height))

        self.outline = pygame.draw.rect(self.screen, (0, 0, 0), (x, y, self.width+2, self.height+2), 1)

        # Draw cell value
        if self.value != 0:
            text = font.render(str(self.value), True, (0, 0, 0))
            text_rect = text.get_rect(center=(x + self.width // 2, y + self.height // 2))
            self.screen.blit(text, text_rect)
        else:
            # Ensure the cell is visually cleared if the value is 0
            pygame.draw.rect(self.screen, pygame.Color('white'), (x + 1, y + 1, self.width - 2, self.height - 2))

        # Draw sketched value if present
        if self.sketch_value is not None and self.value == 0:
            sketch_text = font.render(str(self.sketch_value), True, (128, 128, 128))
            sketch_rect = sketch_text.get_rect(topleft=(x + 5, y + 5))
            self.screen.blit(sketch_text, sketch_rect)

        # Draw cell outline if selected
        if self.selected:
            pygame.draw.rect(self.screen, "blue1", (x, y, self.width+2, self.height+2), 2)


# FOR TESTING PURPOSES UNCOMMENT TO TEST IT
# pygame.init()
# screen = pygame.display.set_mode((1280, 720))
# clock = pygame.time.Clock()
# running = True
#
# while running:
#     # poll for events
#     # pygame.QUIT event means the user clicked X to close your window
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#
#     # fill the screen with a color to wipe away anything from last
#
#     # RENDER YOUR GAME HERE
#     screen.fill("white")
#     cell = Cell(1, 1, 1, screen)
#     cell.draw()
#     # flip() the display to put your work on screen
#     pygame.display.flip()
#
#     clock.tick(60)  # limits FPS to 60
#
# pygame.quit()
