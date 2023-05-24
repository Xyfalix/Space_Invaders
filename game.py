import pygame
from player import Player
from aliens import Aliens

class Game:
    def __init__(self):
        player_sprite = Player()
        self.player = pygame.sprite.GroupSingle(player_sprite)

    def run(self):
        pass
        # update all sprite groups
        # draw all sprite groups
        # Groups
        self.player.draw(screen)

