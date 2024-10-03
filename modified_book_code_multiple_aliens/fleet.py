import pygame as pg
from vector import Vector
from point import Point
from laser import Laser 

from alien import Alien
from pygame.sprite import Sprite

class Fleet(Sprite):
    def __init__(self, ai_game): 
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.ship = ai_game.ship
        self.aliens = pg.sprite.Group()
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        self.sb = ai_game.sb
        self.v = Vector(self.settings.alien_speed, 0)
        # alien = Alien(ai_game=ai_game)
        # self.aliens.add(alien)
        self.spacing = 1.4
        self.create_fleet()
        # self.create_row()

    def reset_fleet(self):
        self.aliens.empty()
        self.create_fleet()

    def create_fleet(self):
        alien = Alien(ai_game=self.ai_game, v=self.v)
        alien_height = alien.rect.height
        current_y = alien_height
        while current_y < (self.settings.scr_height - self.spacing * 6 * alien_height):
            self.create_row(current_y)
            current_y += self.spacing * alien_height
        
    def create_row(self, y):
        alien = Alien(ai_game=self.ai_game, v=self.v)
        alien_width = alien.rect.width
        current_x = alien_width 
        while current_x < (self.settings.scr_width - self.spacing * alien_width):
             new_alien = Alien(self, v=self.v)
             new_alien.rect.y = y
             new_alien.y = y
             new_alien.x = current_x
             new_alien.rect.x = current_x
             self.aliens.add(new_alien)
             current_x += self.spacing * alien_width

    def check_edges(self):
        for alien in self.aliens:
            if alien.check_edges(): 
                return True 
        return False
    
    def check_bottom(self):
        for alien in self.aliens:
            if alien.rect.bottom >= self.settings.scr_height:
                self.ship.ship_hit()
                return True
        return False

    def update(self): 
        collisions = pg.sprite.groupcollide(self.ship.lasers, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            self.ship.lasers.empty()
            self.create_fleet()
                    # Increase level.
            self.stats.level += 1
            self.sb.prep_level()
            return
        if pg.sprite.spritecollideany(self.ship, self.aliens):
            print("Ship hit!")
            self.ship.ship_hit()
            return
        
        if self.check_bottom():
            return 
        
        if self.check_edges():
            self.v.x *= -1 
            for alien in self.aliens:
                alien.v.x = self.v.x
                alien.y += self.settings.fleet_drop_speed
            
        for alien in self.aliens:
            alien.update()

    def draw(self): pass
        # for alien in self.aliens:
        #     alien.draw()

def main():
    print('\n run from alien_invasions.py\n')

if __name__ == "__main__":
    main()
