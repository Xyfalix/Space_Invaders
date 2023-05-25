import pygame
from sys import exit
from player import Player
from aliens import Aliens, BonusAlien
from obstacle import Obstacle
from projectile import Projectile
import random

def create_aliens(rows, cols, start_x_pos, start_y_pos):
    spacing = 50
    for row_index, row in enumerate(range(rows)):
        for col_index, col in enumerate(range(cols)):
            x_pos = start_x_pos + col_index * spacing
            y_pos = start_y_pos + row_index * spacing
            aliens.add(Aliens(row, x_pos, y_pos))

def create_shelter(x_start, y_start):
    for row_index, row in enumerate(Obstacle.shape):
        for col_index, col in enumerate(row):
            if col == 'x':
                x = x_start + col_index * Obstacle.block_size
                y = y_start + row_index * Obstacle.block_size
                shelter.add(Obstacle(x, y))

def alien_border_check():
    global alien_direction
    all_aliens = aliens.sprites()
    for alien in all_aliens:
        if alien.rect.right >= screen_width:
            alien_direction = -1
            alien_downward_movement(2)
        elif alien.rect.left <= 0:
            alien_direction = 1
            alien_downward_movement(2)

def alien_invaded_check():
    global game_active
    all_aliens = aliens.sprites()
    for alien in all_aliens:
        if alien.rect.bottom >= 550:
            game_active = False

def alien_downward_movement(distance):
    all_aliens = aliens.sprites()
    if all_aliens:
        for alien in all_aliens:
            alien.rect.y += distance

def alien_shooter():
    if aliens:
        # Get the lowest y-coordinate among all sprites in the group
        min_y = min(alien.rect.y for alien in aliens.sprites())

        # Find all sprites with the lowest y-coordinate
        highest_aliens = [alien for alien in aliens.sprites() if alien.rect.y == min_y]

        # Select a random sprite from the sprites with the lowest x-coordinate
        selected_sprite = random.choice(highest_aliens)

        return selected_sprite

def spawn_bonus_alien():
    side = random.choice(bonus_alien_spawn_side)
    bonus_alien.add(BonusAlien(side=side, screen_width=screen_width))

def collision_checker():
    global lives
    global score
    global game_active
    global alien_direction
    # player lasers
    if player.sprite.projectiles:
        for projectile in player.sprite.projectiles:
            # obstacle collision
            if pygame.sprite.spritecollide(projectile, shelter, True):
                projectile.kill()
            # alien collision
            aliens_hit = pygame.sprite.spritecollide(projectile, aliens, True)
            if aliens_hit:
                explosion_sound.play()
                for alien in aliens_hit:
                    score += alien.value
                projectile.kill()
                # if all aliens in the group have been killed, generate a fresh set of aliens
                if not aliens:
                    create_aliens(rows=5, cols=8, start_x_pos=60, start_y_pos=80)
                    alien_direction = 1

            # bonus alien collision
            if pygame.sprite.spritecollide(projectile, bonus_alien, True):
                explosion_sound.play()
                projectile.kill()
                score += random.choice([500, 600, 700, 800, 900, 1000])

    # alien lasers
    if alien_projectile:
        for projectile in alien_projectile:
            # obstacle collision
            if pygame.sprite.spritecollide(projectile, shelter, True):
                projectile.kill()
            # player collision
            if pygame.sprite.spritecollide(projectile, player, False):
                explosion_sound.play()
                projectile.kill()
                lives -= 1
                if lives <= 0:
                    game_active = False

    # aliens
    if aliens:
        for alien in aliens:
            # check for collision between alien and shelter. Destroy shelter.
            pygame.sprite.spritecollide(alien, shelter, True)

def display_lives():
    for life in range(lives):
        x = lives_x_start_pos + (life * (live_surf.get_size()[0] + 10))
        screen.blit(live_surf, (x, 8))
        screen.blit(life_text, life_text_rect)

def display_score():
    score_text = test_font.render(f'Score: {score}', False, (255, 255, 255))
    score_text_rect = score_text.get_rect(midleft=(10, 20))
    screen.blit(score_text, score_text_rect)


pygame.init()
screen_width = 600
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Space Invaders')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeled.ttf', 20)
bonus_alien_spawn_side = ['right', 'left']
game_active = False
start_time = 0

ALIENPROJECTILE = pygame.USEREVENT + 1
# alien to shoot 1 laser every 800 ms
pygame.time.set_timer(ALIENPROJECTILE, 800)

BONUSALIEN = pygame.USEREVENT + 2
# spawn bonus alien randomly from 2 to 5s
pygame.time.set_timer(BONUSALIEN, random.randint(10000, 15000))

# groups
# player group
player = pygame.sprite.GroupSingle()
player.add(Player(screen_width/2, screen_height-10, screen_width))

# alien group
aliens = pygame.sprite.Group()
alien_direction = 1

# bonus alien group
bonus_alien = pygame.sprite.GroupSingle()

# shelter group
shelter = pygame.sprite.Group()

# alien projectile group
alien_projectile = pygame.sprite.Group()

# score and life setup
lives = 3
live_surf = pygame.image.load('graphics/player.png').convert_alpha()
lives_x_start_pos = screen_width - live_surf.get_size()[0] * lives - 30
life_text = test_font.render('Lives:', False, (64, 224, 240))
life_text_rect = life_text.get_rect(midright=(lives_x_start_pos-10, 25))
score = 0

# music setup
music = pygame.mixer.Sound('audio/music.wav')
music.set_volume(0.2)
music.play(loops=-1)

laser_sound = pygame.mixer.Sound('audio/laser.wav')
laser_sound.set_volume(0.2)

explosion_sound = pygame.mixer.Sound('audio/explosion.wav')
explosion_sound.set_volume(0.5)

background_surface = pygame.image.load('graphics/tv.png').convert()

# draw alien objects
create_aliens(rows=5, cols=8, start_x_pos=60, start_y_pos=60)

# generate shelter from obstacle blocks
create_shelter(50, 450)
create_shelter(250, 450)
create_shelter(450, 450)

# Intro Screen
intro_font = pygame.font.Font('font/Pixeled.ttf', 50)
space_text = intro_font.render('SPACE', False, (255, 255, 255))
space_rect = space_text.get_rect(center=(screen_width/2, 70))

invaders_text = intro_font.render('INVADERS', False, (255, 255, 255))
invaders_rect = invaders_text.get_rect(center=(screen_width/2, 150))

red_alien_pic = pygame.image.load('graphics/red.png').convert_alpha()
red_alien_rect = red_alien_pic.get_rect(topright=(250, 230))
red_alien_score = test_font.render('= 100pts', False, (240, 79, 80))
red_alien_score_rect = red_alien_score.get_rect(topright=(400, 215))

yellow_alien_pic = pygame.image.load('graphics/yellow.png').convert_alpha()
yellow_alien_rect = yellow_alien_pic.get_rect(topright=(250, 290))
yellow_alien_score = test_font.render('= 200pts', False, (208, 192, 80))
yellow_alien_score_rect = yellow_alien_score.get_rect(topright=(410, 275))

green_alien_pic = pygame.image.load('graphics/green.png').convert_alpha()
green_alien_rect = green_alien_pic.get_rect(topright=(250, 350))
green_alien_score = test_font.render('= 300pts', False, (80, 208, 112))
green_alien_score_rect = green_alien_score.get_rect(topright=(410, 335))

bonus_alien_pic = pygame.image.load('graphics/extra.png').convert_alpha()
bonus_alien_rect = bonus_alien_pic.get_rect(topright=(250, 415))
bonus_alien_score = test_font.render('= ???pts', False, (38, 211, 239))
bonus_alien_score_rect = bonus_alien_score.get_rect(topright=(420, 390))

play_font = pygame.font.Font('font/Pixeled.ttf', 30)
play_text = play_font.render('PLAY!', False, (255, 255, 255))
play_text_rect = play_text.get_rect(center=(320, 500))

# Game Over Screen
game_over_text = intro_font.render('GAME OVER', False, (255, 255, 255))
game_over_text_rect = game_over_text.get_rect(center=(screen_width/2, 200))

play_again_text = play_font.render('PLAY AGAIN?', False, (255, 255, 255))
play_again_text_rect = play_again_text.get_rect(center=(screen_width/2, 400))

# self.image = pygame.image.load('graphics/green.png').convert_alpha()
# self.value = 300
# elif 1 <= row <= 2:
# self.image = pygame.image.load('graphics/yellow.png').convert_alpha()
# self.value = 200
# else:
# self.image = pygame.image.load('graphics/red.png').convert_alpha()
# self.value = 100

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == ALIENPROJECTILE:
                # Create new alien projectiles every 800ms based on ALIENPROJECTILE timer
                if aliens:
                    selected_alien = alien_shooter()
                    alien_projectile.add(
                        Projectile(x_pos=selected_alien.rect.centerx, y_pos=selected_alien.rect.bottom,
                                   screen_height=screen_height,
                                   speed=6))
                    laser_sound.play()

            if event.type == BONUSALIEN:
                spawn_bonus_alien()

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button is clicked
            mouse_pos = pygame.mouse.get_pos()
            if play_text_rect.collidepoint(mouse_pos):
                # "PLAY" button is clicked
                game_active = True
                start_time = int(pygame.time.get_ticks())

    if game_active:
        # background setup
        screen.blit(background_surface, (0, 0))

        # draw player object
        player.draw(screen)
        player.update()

        aliens.draw(screen)
        alien_border_check()
        aliens.update(alien_direction)

        # draw obstacle
        shelter.draw(screen)

        # draw player projectiles
        player.sprite.projectiles.draw(screen)
        player.sprite.projectiles.update()

        # draw alien projectiles
        alien_projectile.draw(screen)
        alien_projectile.update()

        # draw bonus alien
        bonus_alien.draw(screen)
        bonus_alien.update()

        # collision checker
        collision_checker()

        # display lives
        display_lives()

        # display score
        display_score()

        # check if aliens have crossed the threshold boundary which will end the game
        alien_invaded_check()
    else:
        # Display intro screen only when game is first started
        if start_time == 0:
            screen.fill((0, 0, 0))
            # space invaders text
            screen.blit(space_text, space_rect)
            screen.blit(invaders_text, invaders_rect)
            # red alien image and score
            screen.blit(red_alien_pic, red_alien_rect)
            screen.blit(red_alien_score, red_alien_score_rect)
            # yellow alien image and score
            screen.blit(yellow_alien_pic, yellow_alien_rect)
            screen.blit(yellow_alien_score, yellow_alien_score_rect)
            # green alien image and score
            screen.blit(green_alien_pic, green_alien_rect)
            screen.blit(green_alien_score, green_alien_score_rect)
            # bonus alien image and score
            screen.blit(bonus_alien_pic, bonus_alien_rect)
            screen.blit(bonus_alien_score, bonus_alien_score_rect)
            # play text
            screen.blit(play_text, play_text_rect)
        # display game over screen if start time > 0
        else:
            screen.fill((0, 0, 0))
            # display game over text
            screen.blit(game_over_text, game_over_text_rect)
            # display player score
            player_score_text = test_font.render(f'Your Score: {score}', False, (255, 255, 255))
            player_score_text_rect = player_score_text.get_rect(center=(screen_width / 2, 300))
            screen.blit(player_score_text, player_score_text_rect)
            # ask if user would like to play again
            screen.blit(play_again_text, play_again_text_rect)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button is clicked
                mouse_pos = pygame.mouse.get_pos()
                if play_again_text_rect.collidepoint(mouse_pos):
                    # "PLAY AGAIN" button is clicked
                    game_active = True
                    # reset start time
                    start_time = 0
                    start_time = int(pygame.time.get_ticks())
                    # reset score
                    score = 0

                    # remove remaining alien sprites
                    aliens.empty()

                    # remove remaining shelter objects
                    shelter.empty()

                    # draw new alien objects
                    create_aliens(rows=5, cols=8, start_x_pos=60, start_y_pos=60)

                    # generate new shelter from obstacle blocks
                    create_shelter(50, 450)
                    create_shelter(250, 450)
                    create_shelter(450, 450)

                    # regenerate lives to 3
                    lives = 3

                    # reset alien direction back to 1
                    alien_direction = 1

    pygame.display.update()
    clock.tick(60)

# TODO 1. Create player object (take a gif), enable left and right movement up to game edges
# TODO 2. Create enemies (5 rows, 10 columns) with a mix of different aliens worth different points
# TODO 3. Create shelter structures that player can use to hide from incoming shots
# TODO 4. Create the score, high score, level notification text and life notification text.
# TODO 5. Player object fires shots that vanish on contact with any alien or the shelter structure
# TODO 6. Rear-most aliens randomly fire shots that vanish on contact with the player object or shelter structure
# TODO 7. If player shot hits the alien, that alien "explodes" and points are awarded. Score updates.
# TODO 8. If player shot hits the structure, the pixels closest to the shot vanishes.
# TODO 9. If alien shot hits the player, the player object "explodes" and 1 life is lost.
#  If no lives are left, game is over.
# TODO 10. If alien shot hits the structure, the pixels closest to the shot vanishes.
# TODO 11. If all aliens have been destroyed, level clear occurs, start next level.
# TODO 12. Increase the frequency of shots, alien movement speed every level increment.
# TODO 13. When corner aliens touch either edge of the screen, they will all shift downwards by fixed distance.
# TODO 14. If any alien passes the shelter, game is over.
# TODO 15. When game is over, prompt user if they would like to play again