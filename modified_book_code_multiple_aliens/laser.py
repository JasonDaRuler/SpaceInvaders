import pygame as pg
from pygame.sprite import Sprite
from random import randint

class Laser(Sprite):
    @staticmethod
    def random_color(): 
        return (randint(0, 255), randint(0, 255), randint(0, 255))
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        # self.color = self.settings.laser_color
        self.color = Laser.random_color()
        self.rect = pg.Rect(0, 0, self.settings.laser_width,
                                self.settings.laser_height)
        self.rect.midtop = ai_game.ship.rect.midtop
        self.y = float(self.rect.y)

    def update(self):
        self.y -= self.settings.laser_speed
        self.rect.y = self.y

    def draw(self):
        pg.draw.rect(self.screen, self.color, self.rect)

def main():
    print("\nYou have to run from alien_invasion.py\n")

if __name__ == "__main__":
    main()
