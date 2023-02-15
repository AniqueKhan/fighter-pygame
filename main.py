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
fighter_1 = Fighter(200, 310)
fighter_2 = Fighter(700, 310)

# Main game loop
run = True
while run:

    clock.tick(FPS)

    # Draw Background
    draw_bg()

    # Draw healthbars
    draw_healthbar(fighter_1.health, 20, 20)
    draw_healthbar(fighter_2.health, 580, 20)

    # Move Fighters
    fighter_1.move(surface=screen,target=fighter_2)

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