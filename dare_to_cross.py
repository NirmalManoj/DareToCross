import pygame
import pygame.freetype
import configme
import time
import math
from player import Player
from background import Background

pygame.init()
# Loads music
pygame.mixer.music.load("audio/mus.mp3")
# Size of display and initializations
size = [configme.SCREEN_WIDTH, configme.SCREEN_HEIGHT]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Dare to Cross")
# Background image when playing
BackGround = Background('images/bg.png', [0, 0])
# Setting up the game icon
icon = pygame.image.load('images/game_icon.png')
pygame.display.set_icon(icon)
pause = False
clock = pygame.time.Clock()

# this button function is used to make the button for pause/quit/continue


def button(msg, x, y, w, h, ic, ac, action=None):
    # Text for message, co-ordinates, height, width, colors, action
    # Colour of button changes to ac when mouse is hovering over button
    gameDisplay = screen
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # When the button is clicked, do the respective action
    if x+w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac, (x, y, w, h))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(gameDisplay, ic, (x, y, w, h))

    # Displaying given message in a button
    smallText = pygame.font.Font("fonts/miztix.ttf", 40)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x+(w/2)), (y+(h/2)))
    gameDisplay.blit(textSurf, textRect)


# Function to unpause the paused game
def unpause():
    global pause
    pygame.mixer.music.unpause()
    pause = False


# Function to quit game properly
def quit_game():
    pygame.quit()
    quit()


# Function to pause game
def paused():
    pygame.mixer.music.pause()
    gameDisplay = screen

    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Special background color while paused
        screen.fill(configme.PAUSE_COLOR)
        largeText = pygame.font.Font('fonts/timberwolfcond.ttf', 115)
        TextSurf, TextRect = text_objects("Paused", largeText)
        TextRect.center = (configme.SCREEN_WIDTH/2, configme.SCREEN_HEIGHT/2)
        gameDisplay.blit(TextSurf, TextRect)

        mouse = pygame.mouse.get_pos()
        # Button to continue paused game
        button("Continue", 250, 550, 150, 75,
               configme.GREEN, configme.GREEN_DARK, unpause)

        # Button to quit the paused game
        button("QUIT", 610, 550, 150, 75, configme.RED,
               configme.RED_DARK, quit_game)

        pygame.display.update()
        clock.tick(15)


# Function to give time allotted for
# each player depending on their current level
def fetch_time(player_level):
    if player_level == 1:
        t_left = 100
    if player_level == 2:
        t_left = 120
    if player_level == 3:
        t_left = 130
    if player_level == 4:
        t_left = 150

    if player_level >= 5:
        t_left = 150 + (player_level-4)*20

    return t_left


# Used to render fonts while displaying messages after each round
def text_objects(text, font):
    textSurface = font.render(text, True, configme.BLACK)
    return textSurface, textSurface.get_rect()


# To display messages after each round
def message_display(text, gameDisplay):
    largeText = pygame.font.Font('freesansbold.ttf', 50)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = (configme.SCREEN_WIDTH/2, configme.SCREEN_HEIGHT/2)
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()
    time.sleep(2)


# Function stats is to continuously print
# the updated score and time left during a round of game
# Current score of player,
# Time left to finish this round/fail
def stats(score, players_level, time):
    myfont = pygame.freetype.Font(
        "fonts/Blugie.ttf", 24)  # Using freetype.font here
    myfont.render_to(screen, (4, 4), "Score:"+str(score),
                     configme.STAT_COLOR, None, size=64)

    # Here, the time passed is not an integer.
    # So ceiling it as this is used to display time left in second for a player
    time = math.ceil(time)

    myfont.render_to(screen, (500, 4), "Time Left:" +
                     str(time), configme.STAT_COLOR, None, size=64)

    myfont.render_to(screen, (800, 4), "Level: " +
                     str(players_level), configme.STAT_COLOR, None, size=64)

# The screen with which players are greeted once the game starts


def intro_screen():
    global pause

    myfont = pygame.freetype.Font("fonts/Blugie.ttf", 24)
    myfont.render_to(screen, (4, 4), "Dare to Cross?",
                     configme.WHITE, None, size=64)

    # pause is True when this function is called. So as long
    # as player doesn't continue, show this welcome screen
    while pause:
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                # When player press enter, continue to game
                if event.key == pygame.K_RETURN:
                    pause = False

        # Setup for screen and messages when the game is started
        screen.fill(configme.BLACK)
        myfont.render_to(screen, (300, 300), "Dare to Cross?",
                         configme.RED, None, size=120)
        myfont.render_to(screen, (250, 450),
                         "PRESS ENTER TO CONTINUE",
                         configme.RED, None, size=80)
        pygame.display.update()


def main():
    pygame.mixer.music.play(-1)  # Starts music
    
    screen.fill(configme.WHITE)
    pygame.display.flip()
    global pause
    pause = True    # Making pause True before calling intro_screen()
    intro_screen()  # intro_screen() will show the welcome screen
    pause = False

    player1 = Player(1)  # Player object for player one
    player2 = Player(2)  # Player object for player two

    # Initializing player levels as one
    player1_level = 1
    player2_level = 1

    # Variables which represent the scores of the players
    player1_score = 0
    player2_score = 0

    while True:
        done = False

        active_sprite_list = []
        active_sprite_list = pygame.sprite.Group()
        # Contains the sprites of only the players
        active_sprite_list.add(player1)

        # Sets up game for the player 1 according to his current level
        player1.setup_game(player1_level)
        # print(player1_level)
        # Updates the enemy list [moving and still objects] of player 1
        player1.enemy_list.update()
        start_ticks = pygame.time.get_ticks()
        # timer represents the time allocated for the current player
        timer = fetch_time(player1_level)
        seconds = 0
        # variable used to represent the time
        # elapsed since the player started his round

        while not done:
            seconds = (pygame.time.get_ticks()-start_ticks) / \
                1000  # calculate how many seconds
            if seconds > timer:
                # If seconds elapsed more than timer, player loses that round
                time.sleep(0.5)
                break

            for event in pygame.event.get():

                # When the player quits the game, quit.
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                # When any keys are down
                if event.type == pygame.KEYDOWN:
                    # Pause the game while escape key is pressed
                    if event.key == pygame.K_ESCAPE:
                        pause = True
                        paused()
                    # Normal movement in four dimenstions
                    if event.key == pygame.K_LEFT:
                        player1.go_left()
                    if event.key == pygame.K_RIGHT:
                        player1.go_right()
                    if event.key == pygame.K_UP:
                        player1.go_up()
                    if event.key == pygame.K_DOWN:
                        player1.go_down()
                # Once the keys are up, stop the motion of the player
                if event.type == pygame.KEYUP:
                    player1.stop()

            active_sprite_list.update()  # Updating players
            # Updating the obstacles in the round of the corresponding player
            player1.enemy_list.update()
            # Check if opponent crashed with an obstacle
            # or reached the destination
            situation_player1 = player1.situation_now()

            # Gets the score of the player without considering time
            player1_score = player1.get_score()
            # If player reached the destination,
            # then stop player's round and continue
            if situation_player1 == "Reached":
                done = True
                player1_score = player1.get_score()
                # A formula is used to calculate the
                # score the player considering time
                # Final score of the player considering the time also
                player1_score = player1_score + 0.1 * (timer-seconds)
            if situation_player1 == "Crashed":
                # If a player collided with an obstacle,
                # then stop player's round and continue
                done = True
                player1_score = 0
                # Setting player's score as zero since the player failed

            screen.fill([255, 255, 255])
            screen.blit(BackGround.image, BackGround.rect)
            active_sprite_list.draw(screen)  # Draws the player
            # Draws all the obstacles for the player
            player1.enemy_list.draw(screen)
            stats(player1_score, player1_level, timer-seconds)

            clock.tick(60)

            pygame.display.flip()

        # Player 2. Same functions as player one. Using variables
        # that are analogous to the corresponding one's of player 1
        # Not commenting those parts again here
        # as they have been well commented just above

        active_sprite_list = []
        active_sprite_list = pygame.sprite.Group()
        active_sprite_list.add(player2)
        done = False
        player2.setup_game(player2_level)
        # print(player2_level)
        player2.enemy_list.update()
        start_ticks = pygame.time.get_ticks()
        timer = fetch_time(player2_level)
        while not done:
            seconds = (pygame.time.get_ticks()-start_ticks) / \
                1000  # calculate how many seconds
            if seconds > timer:  # if more than 10 seconds close the game
                time.sleep(0.5)
                break
            # print("NO")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                    done = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pause = True
                        paused()
                    if event.key == pygame.K_LEFT:
                        player2.go_left()
                    if event.key == pygame.K_RIGHT:
                        player2.go_right()
                    if event.key == pygame.K_UP:
                        player2.go_up()
                    if event.key == pygame.K_DOWN:
                        player2.go_down()
                if event.type == pygame.KEYUP:
                    player2.stop()

            active_sprite_list.update()
            player2.enemy_list.update()
            situation_player2 = player2.situation_now()
            # print("P@" + situation_player2)
            player2_score = player2.get_score()
            if situation_player2 == "Reached":
                done = True
                player2_score = player2.get_score()
                player2_score = player2_score + 0.1 * (timer-seconds)
            if situation_player2 == "Crashed":
                done = True
                player2_score = 0

            screen.fill([255, 255, 255])
            screen.blit(BackGround.image, BackGround.rect)
            active_sprite_list.draw(screen)
            player2.enemy_list.draw(screen)
            stats(player2_score, player2_level, timer-seconds)
            clock.tick(60)

            pygame.display.flip()

        active_sprite_list.remove(player2)
        active_sprite_list = []
        active_sprite_list = pygame.sprite.Group()

        # Part to check who won the round
        # Changing round accordingly, and displaying the corresponding message

        if player1_score > player2_score:
            player1_level = player1_level + 1
            message_display(configme.WIN_PLAYER1, screen)
        if player1_score < player2_score:
            player2_level = player2_level + 1
            message_display(configme.WIN_PLAYER2, screen)
        if player2_score == player1_score:
            message_display(configme.BOTH_LOST, screen)

    pygame.quit()


if __name__ == "__main__":
    main()
