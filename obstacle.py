import pygame

class Obstacle(pygame.sprite.Sprite):
    block_size = 10

    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.block_size = 10
        self.image = pygame.Surface((self.block_size, self.block_size))  # Set the size of an individual block
        self.image.fill('pink')  # Set the color of the block
        self.rect = self.image.get_rect(topleft=(x_pos, y_pos))

    shape = [
                '  xxxxxxx  ',
                ' xxxxxxxxx ',
                'xxxxx xxxxx',
                'xxxx   xxxx',
                'xxx     xxx',]


    def destroy(self):
        pass

    def update(self):
        pass



