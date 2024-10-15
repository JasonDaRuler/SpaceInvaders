import pygame
import random

class Alien(pygame.sprite.Sprite):

	def __init__(self,color,x,y,initial_speed= 0):
		super().__init__()

		self.frame_1 = pygame.image.load(f'graphics/{color}.png').convert_alpha()
		self.frame_2 = pygame.image.load(f'graphics/{color}-edited.png').convert_alpha()
		self.frames = [self.frame_1, self.frame_2]
		self.current_frame = 0

		self.image = self.frames[self.current_frame]

		self.rect = self.image.get_rect(topleft = (x,y))

		self.animation_time = 300
		self.last_update = pygame.time.get_ticks()

		if color == 'red': self.value = 100
		elif color == 'purple': self.value = 200
		else: self.value = 300
  
		self.base_speed = initial_speed
		self.speed = initial_speed

	def update(self,direction):
		speed_increase = 0.2 
		self.speed = self.base_speed + speed_increase
		self.rect.x += direction * self.speed
		self.rect.x += direction * self.speed
		self.rect.y += direction * self.speed
		self.rect.y -= direction * self.speed
		current_time = pygame.time.get_ticks()
   
		if current_time - self.last_update > self.animation_time:
			self.current_frame = (self.current_frame + 1) % len(self.frames)
			self.image = self.frames[self.current_frame]
			self.last_update = current_time

class Explosion(pygame.sprite.Sprite):
	def __init__(self, x, y, size):
		super().__init__()
		pygame.sprite.Sprite.__init__(self)
		self.images = []
		for num in range(1, 4):
			img = pygame.image.load(f"graphics/exp{num}.png")
			if size == 1:
				img = pygame.transform.scale(img, (20, 20))
			if size == 2:
				img = pygame.transform.scale(img, (40, 40))
			if size == 3:
				img = pygame.transform.scale(img, (160, 160))
			
			self.images.append(img)
		self.index = 0
		self.image = self.images[self.index]
		self.rect = self.image.get_rect(center=(x,y))
		self.rect.center = [x, y]
		self.counter = 0


	def update(self):
		explosion_speed = 3
		self.counter += 1

		if self.counter >= explosion_speed and self.index < len(self.images) - 1:
			self.counter = 0
			self.index += 1
			self.image = self.images[self.index]

		if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
			self.kill()

class UfoExplosion(pygame.sprite.Sprite):
	def __init__(self, x, y, size):
		super().__init__()
		pygame.sprite.Sprite.__init__(self)
		self.images = []
		for num in range(1, 4):
			img = pygame.image.load(f"graphics/500.png")
			img = pygame.transform.scale(img, (160, 160))
			
			self.images.append(img)
		self.index = 0
		self.image = self.images[self.index]
		self.rect = self.image.get_rect(center=(x,y))
		self.rect.center = [x, y]
		self.counter = 0


	def update(self):
		explosion_speed = 3
		
		self.counter += 1

		if self.counter >= explosion_speed and self.index < len(self.images) - 1:
			self.counter = 0
			self.index += 1
			self.image = self.images[self.index]

		if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
			self.kill()

class Ufo(pygame.sprite.Sprite):
	def __init__(self,side,screen_width):
		super().__init__()
		self.image = pygame.image.load('graphics/extra.png').convert_alpha()
		
		if side == 'right':
			x = screen_width + 50
			self.speed = - 3
		else:
			x = -50
			self.speed = 3

		self.rect = self.image.get_rect(topleft = (x,80))

	def update(self):
		self.rect.x += self.speed

		
