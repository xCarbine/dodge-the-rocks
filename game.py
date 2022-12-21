# Mohammed Alwosaibi (hst6pw)

# modules
import random

import pygame
import gamebox

'''
This game is a single-player game where a block is being controlled by the player
that will try to dodge obstacles falling from the sky. The color of the block changes
based on how many lives the player has left. The game also speeds up with time, and so
does the player's speed. There will be an added mechanism where the player can gain lives
if they collect a heart that spawns at random, but they are capped at 3 lives. The player
will have a purple color with 3 lives, yellow with 2 lives, red with 1 life, and black with
no lives.
'''

'''
REQUIRED FEATURES:
User Input: A-D, movement keys for player.
Game Over: player fails to dodge obstacles and loses all three lives.
Small Enough Window: Window is 800 pixels wide and 600 pixels high.
Graphics/Images: player is a box that changes colors, obstacles are rock images falling from the sky.
'''

'''
OPTIONAL FEATURES:
- Restart from Game Over: player will be able to restart when and if they lose.
- Collectibles: player will be able to pick up hearts to gain extra lives.
- Timer: there will be a timer to keep track of the score.
- Health Bar: the player's color will change based on how many lives they have.
'''

# constants
IMMUNITY_TICKS = 30  # ticks of immunity before player can start losing lives again

player_speed = 10  # speed of player

# starting lives
lives = 3

# counter to insure player doesn't instantly lose all lives
counter = IMMUNITY_TICKS

# boolean that tells whether game is over
game_over = False

# possible speeds of rocks
rock_speeds = [4, 6, 8, 10, 12]

# variable to keep track of score
score = 0

# list of whether rocks have been set a speed
rocks_sped_up = [False] * 4

# heart spawned or not
heart_spawned = False

# total ticks player
total_ticks = 0

# variables related to the window and sprites
camera = gamebox.Camera(800, 600)
player_outline = gamebox.from_color(400, 570, 'black', 60, 60)
player = gamebox.from_color(400, 570, 'purple', 50, 50)
rocks = [gamebox.from_image(100, -80, 'rock.png'),
         gamebox.from_image(300, -80, 'rock.png'),
         gamebox.from_image(500, -80, 'rock.png'),
         gamebox.from_image(700, -80, 'rock.png')]
game_over_text = gamebox.from_text(400, 300, '', 100, 'red')
score_text = gamebox.from_text(30, 30, str(score), 40, 'red')


def tick(keys):
    """A function that will be called 30 times a second given a set of input keys

    @param keys: a set of input keys
    """
    # global variables
    global player_speed, total_ticks, heart_spawned, lives, player, counter, game_over, game_over_text, player_outline, rocks, score, score_text, rocks_sped_up, rock_speeds, heart

    # erase everything that was on the screen
    camera.clear('#A8EFF4')

    if not game_over:
        if not heart_spawned and random.randint(1, 100) == 1:
            heart_spawned = True
            heart = gamebox.from_image(random.randint(30, 770), 570, 'heart.png')

        if heart_spawned and player.touches(heart):
            if lives != 3:
                lives += 1
            heart_spawned = False

        for i in range(len(rocks)):
            if not rocks_sped_up[i]:
                rocks[i].speedy = random.choice(rock_speeds)
                rocks_sped_up[i] = True
            if rocks[i].y >= 680:
                rocks[i].y = -80
                rocks_sped_up[i] = False
            rocks[i].move_speed()

        # allow the player to move left or right, and stay still if both keys are pressed.
        if not (pygame.K_RIGHT in keys and pygame.K_LEFT in keys):
            if pygame.K_RIGHT in keys and player_outline.x < 770:
                player.x = min(player.x + player_speed, 770)
                player_outline.x = min(player_outline.x + player_speed, 770)
            elif pygame.K_LEFT in keys and player_outline.x > 30:
                player.x = max(player.x - player_speed, 30)
                player_outline.x = max(player_outline.x - player_speed, 30)

        if counter == IMMUNITY_TICKS:
            for rock in rocks:
                if player.touches(rock):
                    lives -= 1
                    counter = 0

        if counter != IMMUNITY_TICKS:
            counter += 1

        # change color of player when lives reach certain thresholds
        if lives == 3:
            player = gamebox.from_color(player.x, 570, 'purple', 50, 50)
        if lives == 2:
            player = gamebox.from_color(player.x, 570, 'yellow', 50, 50)
        elif lives == 1:
            player = gamebox.from_color(player.x, 570, 'red', 50, 50)
        elif lives == 0:
            player = gamebox.from_color(player.x, 570, 'black', 50, 50)
            game_over_text = gamebox.from_text(400, 300, 'Game Over. Press Y To Play Again!', 50, 'red')
            game_over = True

        score += 1/30
        total_ticks += 1
        score_text = gamebox.from_text(30, 30, str(int(score)), 40, 'red')

        if total_ticks % 300 == 0:
            rock_speeds_copy = []
            for i in range(5):
                rock_speeds_copy.append(rock_speeds[i] + 2)
            rock_speeds = rock_speeds_copy
            player_speed += 2

    if game_over and pygame.K_y in keys:
        lives = 3
        counter = IMMUNITY_TICKS
        game_over = False
        score = 0
        rocks_sped_up = [False] * 4
        rock_speeds = [4, 6, 8, 10, 12]
        player_outline = gamebox.from_color(400, 570, 'black', 60, 60)
        player = gamebox.from_color(400, 570, 'purple', 50, 50)
        rocks = [gamebox.from_image(100, -80, 'rock.png'),
                 gamebox.from_image(300, -80, 'rock.png'),
                 gamebox.from_image(500, -80, 'rock.png'),
                 gamebox.from_image(700, -80, 'rock.png')]
        game_over_text = gamebox.from_text(400, 300, '', 100, 'red')
        score_text = gamebox.from_text(30, 30, str(int(score)), 40, 'red')
        heart_spawned = False
        total_ticks = 0
        player_speed = 10

    # draw everything on the screen
    camera.draw(gamebox.from_image(400, 300, 'https://www.wallpapertip.com/wmimgs/78-786969_blue-line-skull-wallpaper-dark-punisher-wallpaper-hd.jpg'))
    camera.draw(player_outline)
    camera.draw(player)
    if heart_spawned:
        camera.draw(heart)
    for rock in rocks:
        camera.draw(rock)
    camera.draw(game_over_text)
    camera.draw(score_text)
    camera.display()


# loop the tick function 30 times a second
gamebox.timer_loop(30, tick)
