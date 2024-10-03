import pygame as pg
from vector import Vector
from point import Point
from laser import Laser 
from time import sleep
from pygame.sprite import Sprite

class Ship(Sprite):
    def __init__(self, ai_game, v=Vector()):
        super().__init__()
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.stats = ai_game.stats
        self.sb = None

        self.image = pg.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom
        scr_r = self.screen_rect 
        self.x = float(scr_r.midbottom[0])
        self.y = float(scr_r.height)
        self.v = v
        self.lasers = pg.sprite.Group()
        self.firing = False
        self.fleet = None

    def set_fleet(self, fleet): self.fleet = fleet 

    def set_sb(self, sb): self.sb = sb

    def reset_ship(self):
        self.lasers.empty()
        self.center_ship()

    def center_ship(self):         
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def bound(self):
        x, y, scr_r = self.x, self.y, self.screen_rect
        self.x = max(0, min(x, scr_r.width - self.rect.width)) 
        self.y = max(0, min(y, scr_r.height - self.rect.height))

    def ship_hit(self):
        self.stats.ships_left -= 1
        print(f"Only {self.stats.ships_left} ships left now")
        self.sb.prep_ships()
        if self.stats.ships_left <= 0:
            self.ai_game.game_over()

        self.lasers.empty()
        self.fleet.aliens.empty()

        self.center_ship()
        self.fleet.create_fleet()

        sleep(0.5) 

    def fire_laser(self):
        laser = Laser(self.ai_game) 
        self.lasers.add(laser)
        
    def open_fire(self): self.firing = True 

    def cease_fire(self): self.firing = False

    def update(self):
        self.x += self.v.x 
        self.y += self.v.y
        self.bound()
        if self.firing:
            self.fire_laser()
        self.lasers.update()
        for laser in self.lasers.copy():
            if laser.rect.bottom <= 0:
                self.lasers.remove(laser)
        for laser in self.lasers.sprites():
            laser.draw() 
        self.draw()

    def draw(self): 
        self.rect.x, self.rect.y = self.x, self.y
        self.screen.blit(self.image, self.rect)

def main():
    print('\n*** message from ship.py --- run from alien_invasions.py\n')

if __name__ == "__main__":
    main()
