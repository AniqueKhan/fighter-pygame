import pygame as pg
from fighter import Fighter
from constants import *

# Initialization
pg.init()

# Screen
screen = pg.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pg.display.set_caption("Fighter Pygame - Anique")

# Clock
clock = pg.time.Clock()

# Load Images
bg_image = pg.image.load("assets/images/background/background.jpg").convert_alpha()
warrior_sheet = pg.image.load("assets/images/warrior/Sprites/warrior.png").convert_alpha()
wizard_sheet = pg.image.load("assets/images/wizard/Sprites/wizard.png").convert_alpha()

# Define number of steps in each animation
WARRIOR_ANIMATION = [10,8,1,7,7,3,7]
WIZARD_ANIMATION = [8,8,1,8,8,3,7]

# Fighter Data
WARRIOR_SIZE , WIZARD_SIZE = 162 , 250
WARRIOR_SCALE , WIZARD_SCALE = 4 , 3
WARRIOR_OFFSET , WIZARD_OFFSET = [72,56] , [112,107]
WARRIOR_DATA , WIZARD_DATA = {} , {}
WARRIOR_DATA['SIZE'],WARRIOR_DATA['SCALE'],WARRIOR_DATA['OFFSET'] = WARRIOR_SIZE,WARRIOR_SCALE,WARRIOR_OFFSET
WIZARD_DATA['SIZE'],WIZARD_DATA['SCALE'],WIZARD_DATA['OFFSET'] = WIZARD_SIZE,WIZARD_SCALE,WIZARD_OFFSET


# Function for drawing background
def draw_bg():
    scaled_bg = pg.transform.scale(bg_image,(SCREEN_WIDTH,SCREEN_HEIGHT))
    screen.blit(scaled_bg,(0,0))

# Function for drawing health bars
def draw_healthbar(health,x,y):
    ratio = health / 100
    pg.draw.rect(screen,WHITE,(x-2, y-2, 405, 35))
    pg.draw.rect(screen,RED,(x, y, 400, 30))
    pg.draw.rect(screen,YELLOW,(x, y, 400 * ratio, 30))

# Create fighter instances
fighter_1 = Fighter(x=200, y=310,flip=False,data=WARRIOR_DATA,sprite_spreedsheet=warrior_sheet,animation_steps=WARRIOR_ANIMATION)
fighter_2 = Fighter(x=700, y=310,flip=True,data=WIZARD_DATA,sprite_spreedsheet=wizard_sheet,animation_steps=WIZARD_ANIMATION)

# Main game loop
run = True
while run:

    clock.tick(FPS)

    # Draw Background
    draw_bg()

    # Draw healthbars
    draw_healthbar(health=fighter_1.health,x=20,y=20)
    draw_healthbar(health=fighter_2.health, x=580, y=20)

    # Move Fighters
    fighter_1.move(surface=screen,target=fighter_2)
    # fighter_2.move(surface=screen,target=fighter_1)

    # Update Fighters
    fighter_1.update()
    fighter_2.update()

    # Draw fighters
    fighter_1.draw(screen)
    fighter_2.draw(screen)

    # Event handler

    # Quitting the game
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key==pg.K_ESCAPE):
            run = False

    # Update display
    pg.display.update()

pg.quit()