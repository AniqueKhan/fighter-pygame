import pygame as pg
from constants import *

class Fighter():
    def __init__(self,x,y,flip,data,sprite_spreedsheet,animation_steps):

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
        pg.draw.rect(surface,RED,self.rect)
        surface.blit(source=img,dest=(self.rect.x - (self.offset[0]*self.image_scale) ,self.rect.y - (self.offset[1]*self.image_scale)))

    def move(self,surface,target):
        dx = dy = 0
        self.running ,self.attack_type = False , 0

        # Get Key Presses
        key = pg.key.get_pressed()

        # Can only perform other actions if not currently attacking
        if not self.attacking:
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
            if key[pg.K_p] or key[pg.K_l]:
                self.attack(surface=surface,target=target)
                # Attack Initiated
                if key[pg.K_p]:
                    self.attack_type=1
                if key[pg.K_l]:
                    self.attack_type=2

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

    def attack(self,surface,target):
        if not self.attack_cooldown:
            self.attacking = True

            attacking_rect = pg.Rect(self.rect.centerx - (2*self.rect.width*self.flip), self.rect.y,2*self.rect.width,self.rect.height)

            if attacking_rect.colliderect(target.rect):
                target.health -= 10
                target.hit = True

            pg.draw.rect(surface, GREEN,attacking_rect)