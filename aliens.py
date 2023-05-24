import pygame

class Aliens(pygame.sprite.Sprite):
    def __init__(self, row, x_pos, y_pos):
        super().__init__()
        if row == 0:
            self.image = pygame.image.load('graphics/green.png').convert_alpha()
            self.value = 300
        elif 1 <= row <= 2:
            self.image = pygame.image.load('graphics/yellow.png').convert_alpha()
            self.value = 200
        else:
            self.image = pygame.image.load('graphics/red.png').convert_alpha()
            self.value = 100
        self.rect = self.image.get_rect(topleft=(x_pos, y_pos))

    def update(self, direction):
        self.rect.x += direction

class BonusAlien(pygame.sprite.Sprite):
    def __init__(self, side, screen_width):
        super().__init__()
        self.image = pygame.image.load('graphics/extra.png').convert_alpha()
        self.screen_width = screen_width
        self.side = side
        # alien moves from right to left if it spawns on the right side
        if side == 'right':
            x = screen_width + 50
            self.speed = -3
        # alien moves from left to right if it spawns on the left side
        else:
            x = -50
            self.speed = 3
        self.rect = self.image.get_rect(topleft=(x, 50))

    def destroy(self):
        if (self.rect.x <= -50 and self.side == 'right') or\
                (self.rect.x >= self.screen_width + 50 and self.side == 'left'):
            self.kill()

    def update(self):
        self.rect.x += self.speed
        self.destroy()
