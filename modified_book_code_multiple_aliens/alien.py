import pygame as pg
from vector import Vector
from point import Point
from laser import Laser 
from pygame.sprite import Sprite
from timer import Timer
from random import randint

class Alien(Sprite):
    alien_images0 = [pg.image.load(f"images/alien{n}.png") for n in range(1,4)]
    alien_images1 = [pg.image.load(f"images/alien{n}.png") for n in range(1,4)]
    alien_images2 = [pg.image.load(f"images/alien{n}.png") for n in range(1,4)]
    alien_images = [alien_images0, alien_images1, alien_images2]
    # alien_explosion_images = []  # fill in explosion images here

    def __init__(self, ai_game, v): 
        super().__init__()
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.v = v

        type = randint(0, 2)
        self.timer = Timer(images=Alien.alien_images[type], delta=type*350, start_index=type % 2)
        # self.explosion_timer = Timer(images=Alien.alien.explosion_images, start_index=Alien.n % 2,
        #                              loop_continuously=False)
        self.image = self.timer.current_image()
        print(self.image)
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def check_edges(self):
        sr = self.screen.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        r = self.rect 
        return self.x + self.rect.width >= sr.right or self.x <= 0

    def update(self):
        self.x += self.v.x
        self.y += self.v.y
        self.image = self.timer.current_image()
        self.draw()

    def draw(self): 
        self.rect.x = self.x
        self.rect.y = self.y
        self.screen.blit(self.image, self.rect)


def main():
    print('\n run from alien_invasions.py\n')

if __name__ == "__main__":
    main()




