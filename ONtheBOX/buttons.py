import pygame
import sys
import os

# Remove pygame.init() and screen creation, as it's handled in main.py

# WIDTH, HEIGHT = 800, 600
# screen = pygame.display.set_mode((WIDTH, HEIGHT))
# pygame.display.set_caption("Game Menu Flow")

# background = pygame.image.load(os.path.join(os.path.dirname(__file__), "background.jpg.jpeg")).convert()
# background = pygame.transform.scale(background, (WIDTH, HEIGHT))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)

font = pygame.font.SysFont(None, 40)

class Button:
    def __init__(self, screen, text, x, y):
        self.screen = screen
        self.text = text
        self.font = pygame.font.SysFont(None, 40)
        self.image = self.font.render(text, True, WHITE)
        self.rect = self.image.get_rect(center=(x, y))

    def draw(self):
        pygame.draw.rect(self.screen, BLACK, self.rect.inflate(20, 10))
        self.screen.blit(self.image, self.rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)     
