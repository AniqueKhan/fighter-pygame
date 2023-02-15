import pygame as pg
from constants import *

class Fighter():
    def __init__(self,x,y):
        self.rect = pg.Rect(x, y, 80, 180)
        self.y_velocity = self.attack_type = 0
        self.jumping = False

    def draw(self,surface):
        pg.draw.rect(surface,RED,self.rect)

    def move(self,surface):
        dx = dy = 0

        # Get Key Presses
        key = pg.key.get_pressed()

        # Movement
        if key[pg.K_a]:
            dx = -FIGHTER_SPEED
        if key[pg.K_d]:
            dx = FIGHTER_SPEED

        # Jump
        if key[pg.K_w] and not self.jumping:
            self.y_velocity = -30
            self.jumping = True
        
        # Attack
        if key[pg.K_p] or key[pg.K_l]:
            self.attack(surface=surface)
            # Attack Initiated
            if key[pg.K_p]:
                self.attack_type=1
            if key[pg.K_t]:
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
        
        # Update Player Position
        self.rect.x +=dx
        self.rect.y +=dy

    def attack(self,surface):
        attacking_rect = pg.Rect(self.rect.centerx, self.rect.y,2*self.rect.width,self.rect.height)
        pg.draw.rect(surface, GREEN,attacking_rect)