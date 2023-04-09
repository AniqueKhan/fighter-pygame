import pygame as pg

# Initialization
pg.mixer.init()
pg.init()

# Constants

# Screen Dimensions
SCREEN_WIDTH,SCREEN_HEIGHT = 1000,600

# Colors
RED = (255,0,0)
GREEN = (0,255,0)
YELLOW = (255,255,0)
WHITE = (255,255,255)
BLUE = (0,0,255)

FIGHTER_SPEED = 10

GRAVITY = 2

# Frames per second
FPS = 60

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

# Introduction Countdown
INTRO_COUNT = 3

# Round Over Cooldown --> Wait for 2 seconds after round is finished
ROUND_OVER_COOLDOWN = 2000

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


class Fighter():
    def __init__(self,player,x,y,flip,data,sprite_spreedsheet,animation_steps,attack_sound):

        self.player = player
        self.attack_sound = attack_sound

        # 0:Idle 1:Run 2:Jump 3:Attack1 4:Attack2 5:Hit 6:Death --> Action Sequence
        self.y_velocity = self.attack_type = self.attack_cooldown = self.frame_index = self.action = 0

        self.size,self.image_scale ,self.offset= data["SIZE"],data["SCALE"],data["OFFSET"]
        self.animation_list = self.load_images(sprite_spreedsheet=sprite_spreedsheet,animation_steps=animation_steps)
        self.update_time = pg.time.get_ticks()
        self.rect = pg.Rect(x, y, 80, 180)
         
        self.image = self.animation_list[self.action][self.frame_index]
        self.jumping = self.attacking = self.running = self.hit = self.dead = False
        self.flip = flip
        self.health = 100

    # Handle Animation Updates
    def update(self):
        animation_cooldown = 70

        # Check what action the player is performing
        if self.health <= 0:
            self.health,self.dead =0,True
            self.update_action(6)
        elif self.hit:self.update_action(5)
        elif self.attacking:
            if self.attack_type==1:self.update_action(3)  
            elif self.attack_type==2:self.update_action(4)
        elif self.jumping: self.update_action(2)
        elif self.running: self.update_action(1)
        else: self.update_action(0)
            

        # Update Image
        self.image = self.animation_list[self.action][self.frame_index]

        # Check if enough time has passed since last update
        if pg.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index+=1
            self.update_time = pg.time.get_ticks()
        
        # Check if the animation has finished
        if self.frame_index >= len(self.animation_list[self.action]):

            # If the player is dead then end the animation
            if self.dead: self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0

                # Checking if the attack animation was executed
                # After finishing the animation , reset back to idle
                if self.action in (3,4): 
                    self.attacking = False
                    self.attack_cooldown = 30

                # Checking if the attack animation was executed
                # After finishing the animation , reset back to idle
                if self.action==5: 
                    self.hit = False

                    # If the player was in the middle of an attack , then the attack is stopped
                    self.attacking = False
                    self.attack_cooldown = 30
                 

    def update_action(self,next_action):
        if self.action != next_action:
            self.action = next_action

            # Update the animation settings
            self.frame_index , self.update_time = 0, pg.time.get_ticks()

    def load_images(self,sprite_spreedsheet,animation_steps):
        animation_list=[]
        for y,animation in enumerate(animation_steps):
            temporary_image_list =[]
            for x in range(animation):
                temporary_image = sprite_spreedsheet.subsurface(x*self.size,y*self.size,self.size,self.size)
                temporary_image_list.append(pg.transform.scale(temporary_image,(self.size*self.image_scale,self.size*self.image_scale)))
            animation_list.append(temporary_image_list)
        return animation_list

    def draw(self,surface):
        img = pg.transform.flip(surface=self.image, flip_x=self.flip, flip_y=False)
        surface.blit(source=img,dest=(self.rect.x - (self.offset[0]*self.image_scale) ,self.rect.y - (self.offset[1]*self.image_scale)))

    def move(self,target,round_over):
        dx = dy = 0
        self.running ,self.attack_type = False , 0

        # Get Key Presses
        key = pg.key.get_pressed()

        # Can only perform other actions if not currently attacking
        if not self.attacking and not self.dead and not round_over:
            if self.player==1:
                # Movement
                if key[pg.K_a]:
                    dx = -FIGHTER_SPEED
                    self.running = True
                if key[pg.K_d]:
                    dx = FIGHTER_SPEED
                    self.running = True

                # Jump
                if key[pg.K_w] and not self.jumping:
                    self.y_velocity = -30
                    self.jumping = True
                
                # Attack
                if key[pg.K_t] or key[pg.K_f]:
                    self.attack(target=target)
                    # Attack Initiated
                    if key[pg.K_t]: self.attack_type=1
                    if key[pg.K_f]: self.attack_type=2
            
            if self.player==2:
                # Movement
                if key[pg.K_LEFT]:
                    dx = -FIGHTER_SPEED
                    self.running = True
                if key[pg.K_RIGHT]:
                    dx = FIGHTER_SPEED
                    self.running = True

                # Jump
                if key[pg.K_UP] and not self.jumping:
                    self.y_velocity = -30
                    self.jumping = True
                
                # Attack
                if key[pg.K_p] or key[pg.K_l]:
                    self.attack(target=target)
                    # Attack Initiated
                    if key[pg.K_p]: self.attack_type=1
                    if key[pg.K_l]: self.attack_type=2

        # Apply Gravity
        self.y_velocity += GRAVITY
        dy += self.y_velocity

        # Ensures Player Stays On The Screen

        # Left/Right
        if self.rect.left + dx <0:
            dx = -self.rect.left
        if self.rect.right + dx > SCREEN_WIDTH:
            dx = SCREEN_WIDTH- self.rect.right

        # Up/Down
        if self.rect.bottom + dy > SCREEN_HEIGHT - 110:
            self.y_velocity=0
            self.jumping = False
            dy = SCREEN_HEIGHT-110-self.rect.bottom

        # Ensure player face each other
        self.flip = False if target.rect.centerx > self.rect.centerx else True

        # Apply cooldown
        if self.attack_cooldown > 0 : self.attack_cooldown-=1
        
        # Update Player Position
        self.rect.x +=dx
        self.rect.y +=dy

    def attack(self,target):
        if not self.attack_cooldown:
            self.attacking = True
            self.attack_sound.play()

            attacking_rect = pg.Rect(self.rect.centerx - (2*self.rect.width*self.flip), self.rect.y,2*self.rect.width,self.rect.height)

            if attacking_rect.colliderect(target.rect):
                target.health -= 10
                target.hit = True





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