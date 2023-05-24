import pygame

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, screen_height, speed=-8):
        super().__init__()
        self.image = pygame.Surface((5, 15))  # Set the size of the projectile
        self.image.fill((255, 255, 255))  # Set the color of the projectile (white in this case)
        self.rect = self.image.get_rect(center=(x_pos, y_pos))
        self.speed = speed
        self.height_constraint = screen_height

    def destroy(self):
        if self.rect.y <= -50 or self.rect.y >= self.height_constraint + 50:
            self.kill()

    def update(self):
        self.rect.y += self.speed
        self.destroy()