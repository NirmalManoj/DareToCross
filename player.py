import pygame
import configme
import random
from fixed_obstacle import Fixed
from small_fish import Fish
from sharks import Shark

# This class contains all the details of a player, obstacle he has, etc.


class Player(pygame.sprite.Sprite):
    pygame.init()
    # Set speed vector of player
    # The screen has been divided into 11 partitions in the list_regions
    # Each region represent a specific partition in the background
    score_now = 0
    region_now = 0
    region_pre = 0

    change_x = 0  # Change of x co-ordinate which should take effect on player
    change_y = 0  # Change of y co-ordinate which should take effect on player

    # The start_region and end_region of player1 and player2
    # are different and it gets initialized once they are called
    start_region = 1
    end_region = 10
    time = 0
    situation = "none"
    level = None
    enemy_list = None  # Will contain list of all obstacles
    enemy_fixed = None  # Will contain list of all fixed obstacles
    enemy_moving = None  # Will contain list of all moving obstacles
    # Following three variables are to be used as temporary
    # varialbes of obstacles while adding new obstacles
    fixed = None
    moving = None
    movingShark = None

    def __init__(self, player_number):
        pygame.sprite.Sprite.__init__(self)
        self.enemy_list = pygame.sprite.Group()
        self.enemy_fixed_list = pygame.sprite.Group()
        self.enemy_moving_list = pygame.sprite.Group()
        self.image = pygame.image.load("images/arrowup.png")

        # Set start_region and end_region according to the player number
        if player_number == 1:
            self.start_region = 10
            self.end_region = 0
        else:
            self.image = pygame.transform.flip(self.image, False, True)
            self.start_region = 0
            self.end_region = 10

        # Placing the location of the player randomly on the start_region
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(1000-configme.PLAYER_WIDTH)
        self.rect.y = configme.list_regions[self.start_region][0]+5

    # This funciton finds the respective region at which the
    # player situates at the moment
    def find_region(self):
        if self.start_region == 0:
            for i in range(11):
                if configme.list_regions[i][0] <= self.rect.y and \
                        self.rect.y <= configme.list_regions[i][1]:
                    return i
        for i in range(10, -1, -1):
            if configme.list_regions[i][0] <= \
                    self.rect.y + configme.PLAYER_HEIGHT and \
                    self.rect.y + configme.PLAYER_HEIGHT:
                return i

    # This function finds if the player has attained
    # extra scores and returns the corresponding value
    def score(self):
        tem_region = self.find_region()

        # Basic idea is, if a player starts from region 0,
        # he can't reach region 2 without passing through region 1
        # Using this we check if a player has crossed
        # a unique region in that particular round
        if self.start_region == 0:
            if tem_region == self.region_now + 2:
                self.region_now = self.region_now+1
                if tem_region % 2 == 0:
                    return 10
                else:
                    return 5
        if self.start_region == 10:
            if tem_region == self.region_now - 2:
                self.region_now = self.region_now-1
                if tem_region % 2 == 0:
                    return 10
                else:
                    return 5
        return 0

    def put_fixed_obstacle(self, a, b):

        # Select a random number between a and b (inclusive)
        # and puts that many obstacles on screen
        for i in range(0, 6):
            j = i*2

            rnum = random.randrange(a, b+1)
            for t in range(rnum):
                x = random.randrange(0, 1000-130)
                self.fixed = Fixed(x, configme.list_regions[j][0]+5)
                block_hit_list = pygame.sprite.spritecollide(
                    self.fixed, self.enemy_fixed_list, False)

                # Checks if the new obstacle collides with
                # previously put obstacle. If yes, leave it.
                # This adds a texture of randomness to the game
                if len(block_hit_list) > 0:
                    continue
                # Add the fixed obstacle to both enemy_list and fixed_enemy
                self.enemy_fixed_list.add(self.fixed)
                self.enemy_list.add(self.fixed)

    # This fucntion puts moving fish obstacle
    def put_moving_fish_obstacle(self, player_level):
        # Velocity of the moving object is decided
        # based on the current level of the player
        velocity = 2.5 + player_level*2.5
        for i in range(0, 5):
            j = i*2 + 1

            for t in range(2):
                x = random.randrange(0, 1000-130)
                self.moving = Fish(x, configme.list_regions[j][0]+15, velocity)

                block_hit_list = pygame.sprite.spritecollide(
                    self.moving, self.enemy_moving_list, False)
                if len(block_hit_list) > 0:
                    continue
                self.enemy_moving_list.add(self.moving)
                self.enemy_list.add(self.moving)

    # This fucntion puts moving fish obstacle
    def put_moving_shark_obstacle(self, a, player_level):
        # Velocity of the moving object is decided
        # based on the current level of the player
        velocity = 2.5 + player_level*2.5
        for i in range(0, 5):
            j = i*2 + 1

            for t in range(a):
                x = random.randrange(0, 1000-130)
                self.movingShark = Shark(
                    x, configme.list_regions[j][0]+15, velocity)

                block_hit_list = pygame.sprite.spritecollide(
                    self.movingShark, self.enemy_moving_list, False)
                if len(block_hit_list) > 0:
                    continue
                self.enemy_moving_list.add(self.movingShark)
                self.enemy_list.add(self.movingShark)

    # This function sets up the game according the player level for each player

    def setup_game(self, player_level):
        # Initializing variables
        self.score_now = 0

        self.region_now = self.start_region
        self.change_x = 0
        self.change_y = 0
        self.time = 0
        self.situation = "none"
        self.level = None
        self.enemy_list = None
        self.enemy_fixed = None
        self.enemy_moving = None
        self.fixed = None
        self.moving = None
        # return
        self.enemy_list = []
        self.enemy_fixed_list = []
        self.enemy_moving_list = []
        self.enemy_list = pygame.sprite.Group()
        self.enemy_fixed_list = pygame.sprite.Group()
        self.enemy_moving_list = pygame.sprite.Group()

        # Putting fixed and moving obstacles according to the player level
        if player_level == 1:
            time = 100
            self.put_fixed_obstacle(1, 2)

        if player_level == 2:
            time = 120
            self.put_fixed_obstacle(2, 3)
            # return
        if player_level == 3:
            time = 130
            self.put_fixed_obstacle(2, 4)
        if player_level == 4:
            time = 150
            self.put_fixed_obstacle(2, 5)

        if player_level >= 5:
            time = 150 + (player_level-4)*20
            self.put_fixed_obstacle(3, 5)

        if player_level <= 2:
            self.put_moving_fish_obstacle(player_level)
        if player_level == 3:
            self.put_moving_shark_obstacle(1, player_level)
        if player_level >= 4:
            self.put_moving_shark_obstacle(2, player_level)

        # Adding player
        # If player collides with any obstacle in the initial position,
        # give him/her another location

        self.rect.x = random.randrange(1000)
        self.rect.y = configme.list_regions[self.start_region][0]+5
        block_hit_list = []
        block_hit_list = pygame.sprite.spritecollide(
            self, self.enemy_list, False)
        while block_hit_list:
            self.rect.x = random.randrange(1000)
            self.rect.y = configme.list_regions[self.start_region][0]+5
            block_hit_list = []
            block_hit_list = pygame.sprite.spritecollide(
                self, self.enemy_list, False)

    # Update all the stats related to the player

    def update(self):
        # Updating the lcoation of the player
        self.rect.x += self.change_x
        self.rect.y += self.change_y

        # Checking if the player collides any of the obstacles
        block_hit_list = []
        block_hit_list = pygame.sprite.spritecollide(
            self, self.enemy_list, False)
        for block in block_hit_list:
            if self.change_x > 0:
                self.rect.right = block.rect.left
            if self.change_x < 0:
                self.rect.left = block.rect.right
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            if self.change_y < 0:
                self.rect.top = block.rect.bottom
            self.change_x = 0
            self.change_y = 0
            self.situation = "Crashed"
            # If the player collides with any obstacle

        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x+configme.PLAYER_WIDTH > 1000:
            self.rect.x = 1000-configme.PLAYER_WIDTH
        if self.rect.y < 50:
            self.rect.y = 50
        if self.rect.y+configme.PLAYER_HEIGHT > 800:
            self.rect.y = 800-configme.PLAYER_HEIGHT

        # If the player's current region is the end_region,
        # situation = "Reached"
        if self.find_region() == self.end_region:
            self.situation = "Reached"
        ext_score = 10
        ext_score = self.score()
        self.score_now = self.score_now + ext_score

    # This function gives the current score of the player
    # without considering the time
    def get_score(self):
        return self.score_now

    def situation_now(self):
        return self.situation

    # Move player to left
    def go_left(self):
        self.change_x = -5

    # Move player to right
    def go_right(self):
        self.change_x = 5

    def drawer(self, screen):
        screen.fill(configme.GREEN)

    # Move player to up
    def go_up(self):
        self.change_y = -5

    # Move player to down
    def go_down(self):
        self.change_y = 5

    # Sets the change in x-y co-ordinates to zero
    def stop(self):
        self.change_x = 0
        self.change_y = 0
