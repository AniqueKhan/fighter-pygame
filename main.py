import pygame as pg
from fighter import Fighter
from constants import *

# Initialization
pg.mixer.init()
pg.init()

# Screen
screen = pg.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pg.display.set_caption("Fighter Pygame - Anique")

# Audio 
pg.mixer.music.load("assets/audio/music.mp3")
pg.mixer.music.set_volume(0.4)
pg.mixer.music.play(-1,0.0,5000)

sword_fx,magic_fx = pg.mixer.Sound('assets/audio/sword.wav'),pg.mixer.Sound('assets/audio/magic.wav')
sword_fx.set_volume(0.4)
magic_fx.set_volume(0.4)

# Load Images
bg_image = pg.image.load("assets/images/background/background.jpg").convert_alpha()
warrior_sheet = pg.image.load("assets/images/warrior/Sprites/warrior.png").convert_alpha()
wizard_sheet = pg.image.load("assets/images/wizard/Sprites/wizard.png").convert_alpha()

# Victory Image
victory_image = pg.image.load("assets/images/icons/victory.png").convert_alpha()


# Clock
clock = pg.time.Clock()

# Tracking last update time
last_update = pg.time.get_ticks()

# Define fonts
count_font = pg.font.Font("assets/fonts/turok.ttf",80)
score_font = pg.font.Font("assets/fonts/turok.ttf",30)

# Score --> [P1,P2]
score =[0,0]

# Rounds
round_over = False

# Intro Count
intro_count = INTRO_COUNT

# Draw text on the screen
def draw_text(text,font,text_color,x,y):
    img = font.render(text,True,text_color)
    screen.blit(img,(x,y))

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
fighter_1 = Fighter(player=1,x=200, y=310,flip=False,data=WARRIOR_DATA,sprite_spreedsheet=warrior_sheet,animation_steps=WARRIOR_ANIMATION,attack_sound=sword_fx)
fighter_2 = Fighter(player=2,x=700, y=310,flip=True,data=WIZARD_DATA,sprite_spreedsheet=wizard_sheet,animation_steps=WIZARD_ANIMATION,attack_sound=magic_fx)

# Main game loop
run = True
while run:

    clock.tick(FPS)

    # Draw Background
    draw_bg()

    # Draw healthbars
    draw_healthbar(health=fighter_1.health,x=20,y=20)
    draw_healthbar(health=fighter_2.health, x=580, y=20)

    # Draw Scores
    draw_text(text=f"P1: {str(score[0])}", font=score_font, text_color=RED, x=20, y=60)
    draw_text(text=f"P2: {str(score[1])}", font=score_font, text_color=RED, x=580, y=60)

    # Countdown
    if intro_count <= 0 :
        # Move Fighters
        fighter_1.move(target=fighter_2,round_over=round_over)
        fighter_2.move(target=fighter_1,round_over=round_over)
    else:
        # Show countdown
        draw_text(str(intro_count), count_font,RED,SCREEN_WIDTH/2,SCREEN_HEIGHT/3)
        # Update countdown
        if pg.time.get_ticks() - last_update >= 1000:
            intro_count-=1
            last_update=pg.time.get_ticks()

    # Update Fighters
    fighter_1.update()
    fighter_2.update()

    # Draw fighters
    fighter_1.draw(screen)
    fighter_2.draw(screen)

    # Check for round over
    if not round_over:
        if fighter_1.dead:
            score[1]+=1
            round_over=True
            round_over_time = pg.time.get_ticks()
        elif fighter_2.dead:
            score[0]+=1
            round_over=True
            round_over_time = pg.time.get_ticks()
    else:
        # Display Victory Image
        screen.blit(source=victory_image, dest=(350,150))
        if fighter_2.dead: draw_text(text=f"P1 Won!", font=count_font, text_color=RED, x=390, y=190)
        if fighter_1.dead: draw_text(text=f"P2 Won!", font=count_font, text_color=RED, x=390, y=190)

        # Reset Everything
        if pg.time.get_ticks()-round_over_time>ROUND_OVER_COOLDOWN:
            round_over = False
            intro_count = INTRO_COUNT
            fighter_1 = Fighter(player=1,x=200, y=310,flip=False,data=WARRIOR_DATA,sprite_spreedsheet=warrior_sheet,animation_steps=WARRIOR_ANIMATION,attack_sound=sword_fx)
            fighter_2 = Fighter(player=2,x=700, y=310,flip=True,data=WIZARD_DATA,sprite_spreedsheet=wizard_sheet,animation_steps=WIZARD_ANIMATION,attack_sound=magic_fx)




    # Event handler

    # Quitting the game
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key==pg.K_ESCAPE):
            run = False

    # Update display
    pg.display.update()

pg.quit()