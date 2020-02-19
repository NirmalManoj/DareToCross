"""
Global constants
"""

# Colors
BLACK = (0,   0,   0)
WHITE = (255, 255, 255)
BLUE = (0,   0, 255)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
RED_DARK = (255, 0, 0)
GREEN_DARK = (0, 255, 0)
PAUSE_COLOR = (68, 56, 128)
STAT_COLOR = (224, 94, 54)
# Screen dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

# Dimensitons of objects
FIXED_OBJECT_WIDTH = 110

PLAYER_WIDTH = 44
PLAYER_HEIGHT = 40


padding = 50  # Leaving space for the score and time left

# Y co-ordinates of te partitions in the screen
list_regions = [
    [0+padding, 50+padding], [50+padding, 140+padding],
    [140+padding, 190+padding], [190+padding, 280+padding],
    [280+padding, 330+padding], [330+padding, 420+padding],
    [420+padding, 470+padding], [470+padding, 560+padding],
    [560+padding, 610+padding], [610+padding, 700+padding],
    [700+padding, 750+padding]
]


list_regions1 = [
    (0+padding, 50+padding), (50+padding, 150+padding),
    (150+padding, 200+padding), (200+padding, 300+padding),
    (300+padding, 350+padding), (350+padding, 450+padding),
    (450+padding, 500+padding), (500+padding, 600+padding),
    (600+padding, 650+padding), (650+padding, 750+padding),
    (750+padding, 800+padding)
]

# Winning/Losing messages
WIN_PLAYER1 = "Player One Won!"
WIN_PLAYER2 = "Player Two Won!"

BOTH_LOST = "Hehe..both of you lost!!"
