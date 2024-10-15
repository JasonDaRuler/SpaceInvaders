import pygame 
from laser import Laser


class PlayerExplosion(pygame.sprite.Sprite):
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
   
   
class Player(pygame.sprite.Sprite):
	def __init__(self,pos,constraint,speed):
		super().__init__()
		self.image = pygame.image.load('graphics/spaceship-edit.png').convert_alpha()
		self.rect = self.image.get_rect(midbottom = pos)
		self.speed = speed
		self.max_x_constraint = constraint
		self.max_y_constraint = constraint
		self.ready = True
		self.laser_time = 0
		self.laser_cooldown = 600

		self.lasers = pygame.sprite.Group()

		self.laser_sound = pygame.mixer.Sound('audio/laser.wav')
		self.laser_sound.set_volume(0.5)
    
	def get_input(self):
		keys = pygame.key.get_pressed()

		if keys[pygame.K_UP]:
			self.rect.y -= self.speed
		elif keys[pygame.K_DOWN]:
			self.rect.y += self.speed

		if keys[pygame.K_RIGHT]:
			self.rect.x += self.speed
		elif keys[pygame.K_LEFT]:
			self.rect.x -= self.speed

		if keys[pygame.K_SPACE] and self.ready:
			self.shoot_laser()
			self.ready = False
			self.laser_time = pygame.time.get_ticks()
			self.laser_sound.play()

	def recharge(self):
		if not self.ready:
			current_time = pygame.time.get_ticks()
			if current_time - self.laser_time >= self.laser_cooldown:
				self.ready = True

	def constraint(self):
		if self.rect.left <= 0:
			self.rect.left = 0
		if self.rect.right >= self.max_x_constraint:
			self.rect.right = self.max_x_constraint

	def shoot_laser(self):
		self.lasers.add(Laser(self.rect.center,-8,self.rect.bottom))

	def update(self):
		self.get_input()
		self.constraint()
		self.recharge()
		self.lasers.update()
  
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
			#add the image to the list
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
   