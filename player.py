import pygame
from projectile import Projectile

class Player(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, screen_width):
        super().__init__()
        # load player sprite
        self.image = pygame.image.load('graphics/player.png').convert_alpha()
        # shift player to the bottom middle of the screen.
        self.rect = self.image.get_rect(midbottom=(x_pos, y_pos))
        self.max_width = screen_width
        self.ready = True
        self.projectile_time = 0
        self.projectile_cooldown = 600
        self.projectiles = pygame.sprite.Group()

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left >= 10:
            self.rect.x -= 6
        elif keys[pygame.K_RIGHT] and self.rect.right <= self.max_width - 10:
            self.rect.x += 6

    def shoot_projectile(self):
        keys = pygame.key.get_pressed()
        laser_sound = pygame.mixer.Sound('audio/laser.wav')
        laser_sound.set_volume(0.2)
        if keys[pygame.K_SPACE] and self.ready:
            self.projectiles.add(Projectile(self.rect.centerx, self.rect.top, self.rect.bottom))
            laser_sound.play()
            self.ready = False
            self.projectile_time = pygame.time.get_ticks()

    def check_cooldown(self):
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.projectile_time >= self.projectile_cooldown:
                self.ready = True

    def update(self):
        self.movement()
        self.shoot_projectile()
        self.check_cooldown()

