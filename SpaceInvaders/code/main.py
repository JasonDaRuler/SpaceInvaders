import pygame, sys
from player import Player
import obstacle
from alien import Alien, Ufo
from random import choice, randint
from laser import Laser
import os
from alien import Explosion
from alien import UfoExplosion
from player import PlayerExplosion
START_SCREEN = "START"
GAME = "GAME"
HIGH_SCORE = "HIGH_SCORE"

pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

BG = pygame.image.load('graphics/background.png').convert()
font = pygame.font.SysFont(None, 30)
title_font = pygame.font.SysFont(None, 74)

high_score_file = "graphics/high_scores.txt"
	
def save_high_score(new_score):
	scores = load_high_scores()
	scores.append(new_score)
	scores = sorted(scores, reverse=True) [:5]
	with open(high_score_file, "w") as file:
		for score in scores:
			file.write(f"{score}\n")

def load_high_scores():
	if os.path.exists(high_score_file):
		with open(high_score_file, "r") as file:
			scores = [int(line.strip()) for line in file.readlines()]
			return scores
	return []

game_state = START_SCREEN


red_alien = pygame.image.load('graphics/red.png').convert_alpha()
purple_alien = pygame.image.load('graphics/purple.png').convert_alpha()
blue_alien = pygame.image.load('graphics/blue.png').convert_alpha()
extra_alien = pygame.image.load('graphics/extra.png').convert_alpha()

game_state = START_SCREEN

def draw_button(text, rect, color):
    pygame.draw.rect(screen, color, rect)
    label = font.render(text, True, (0, 0, 0))
    screen.blit(label, (rect.x + 20, rect.y + 10))

def main_menu():
    global game_state

    button_width = 150
    button_height = 50
    space_surface = title_font.render("Space", True, (255, 255, 255))
    invaders_surface = title_font.render("Invaders", True, (0, 255, 0))

    total_width = space_surface.get_width() + invaders_surface.get_width() + 10

    space_rect = space_surface.get_rect(left=(screen_width - total_width) / 2, top=screen_height / 10)
    invaders_rect = invaders_surface.get_rect(left=space_rect.right + 10, top=screen_height / 10)

    play_button = pygame.Rect((screen_width / 2) - (button_width / 2), screen_height - 150, button_width, button_height)
    high_score_button = pygame.Rect((screen_width / 2) - (button_width / 2), screen_height - 80, button_width, button_height)

    red_alien_score = font.render("= 100 PTS", True, (255,255,255))
    purple_alien_score = font.render("= 200 PTS", True, (255,255,255))
    blue_alien_score = font.render("= 300 PTS", True, (255,255,255))
    extra_alien_score = font.render("= ??? PTS", True, (255,255,255))

    alien_start_y = screen_height / 4

    while game_state == START_SCREEN:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    game_state = GAME
                elif high_score_button.collidepoint(event.pos):
                    game_state = HIGH_SCORE
					
        screen.fill((0,0,0))
        screen.blit(space_surface, space_rect)
        screen.blit(invaders_surface, invaders_rect)
        draw_button("Play", play_button, (255, 255, 255))
        draw_button("High Score", high_score_button, (255, 255, 255))

        screen.blit(red_alien, (screen_width / 2 - 100, alien_start_y))
        screen.blit(purple_alien, (screen_width / 2 - 100, alien_start_y + 50))
        screen.blit(blue_alien, (screen_width / 2 - 100, alien_start_y + 100))
        screen.blit(extra_alien, (screen_width / 2 - 100, alien_start_y + 150))

        screen.blit(red_alien_score, (screen_width / 2, alien_start_y))
        screen.blit(purple_alien_score, (screen_width / 2, alien_start_y + 50))
        screen.blit(blue_alien_score, (screen_width / 2, alien_start_y + 100))
        screen.blit(extra_alien_score, (screen_width / 2, alien_start_y + 150))
		
        pygame.display.flip()

def game_loop():
	global game_state
	global stats 

	if stats.ships_left <= 0:
		game_state = START_SCREEN

	game_state = START_SCREEN

def high_score_screen():
	global game_state
	scores = load_high_scores()
	print(f"Loaded scores: {scores}")

	button_width = 150
	button_height = 50
	back_button = pygame.Rect((screen_width / 2) - (button_width / 2), screen_height - 100, button_width, button_height)

	while game_state == HIGH_SCORE:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					game_loop()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if back_button.collidepoint(event.pos):
					game_state = START_SCREEN

		screen.fill((0,0,0))

		title_surface = title_font.render("High Scores", True, (255,255,255))
		screen.blit(title_surface, (screen_width / 2 - title_surface.get_width() / 2, 50))

		pygame.draw.rect(screen, (255, 255, 255), back_button)
		back_text = font.render("Back", True, (0,0,0))
		screen.blit(back_text, (back_button.x + 20, back_button.y + 10))

		for i, score in enumerate(scores):
			print(f"Rendering score {score} at position {i + 1}")
			score_surface = font.render(f"{i+1}. {score}", True, (255,255,255))

			y_position = 150 + i * 40
			screen.blit(score_surface, (screen_width / 2 - score_surface.get_width() / 2, y_position))
			
		pygame.display.flip()
 
class Game:
	def __init__(self):
		player_sprite = Player((screen_width / 2,screen_height),screen_width,5)
		self.player = pygame.sprite.GroupSingle(player_sprite)

		self.lives = 3
		self.live_surf = pygame.image.load('graphics/spaceship-edit.png').convert_alpha()
		self.live_x_start_pos = screen_width - (self.live_surf.get_size()[0] * 2 + 20)
		self.score = 0
		self.font = pygame.font.SysFont(None, 40)

		self.shape = obstacle.shape
		self.block_size = 6
		self.blocks = pygame.sprite.Group()
		self.obstacle_amount = 4
		self.obstacle_x_positions = [num * (screen_width / self.obstacle_amount) for num in range(self.obstacle_amount)]
		self.create_multiple_obstacles(*self.obstacle_x_positions, x_start = screen_width / 15, y_start = 480)

		self.aliens = pygame.sprite.Group()
		self.alien_lasers = pygame.sprite.Group()
		self.alien_setup(rows = 4, cols = 8)
		self.alien_direction = 1
		self.alien_speed = 0.2
		self.alien_speed_multiplier = 1.1
  
		self.extra = pygame.sprite.GroupSingle()
		self.extra_spawn_time = randint(40,80)
  
		self.after_explosion_image = pygame.image.load('graphics/500.png').convert_alpha()
		self.after_explosion_time = 1

		global music
		music = pygame.mixer.Sound('audio/music.wav')
		music.set_volume(0.2)
		music.play(loops = -1)
		self.laser_sound = pygame.mixer.Sound('audio/laser.wav')
		self.laser_sound.set_volume(0.5)
		self.explosion_sound = pygame.mixer.Sound('audio/explosion.wav')
		self.explosion_sound.set_volume(0.3)

	
	def create_obstacle(self, x_start, y_start,offset_x):
		for row_index, row in enumerate(self.shape):
			for col_index,col in enumerate(row):
				if col == 'x':
					x = x_start + col_index * self.block_size + offset_x
					y = y_start + row_index * self.block_size
					block = obstacle.Block(self.block_size,(241,79,80),x,y)
					self.blocks.add(block)

	def create_multiple_obstacles(self,*offset,x_start,y_start):
		for offset_x in offset:
			self.create_obstacle(x_start,y_start,offset_x)

	def alien_setup(self,rows,cols,x_distance = 60,y_distance = 48,x_offset = 70, y_offset = 100):
		for row_index, row in enumerate(range(rows)):
			for col_index, col in enumerate(range(cols)):
				x = col_index * x_distance + x_offset
				y = row_index * y_distance + y_offset
				v = x + y
				if row_index == 0: alien_sprite = Alien('blue',x,y)
				elif 1 <= row_index <= 2: alien_sprite = Alien('purple',x,y)
				else: alien_sprite = Alien('red',x,y) 
				self.aliens.add(alien_sprite)
	
	def alien_position_checker(self):
		all_aliens = self.aliens.sprites()
		for alien in all_aliens:
			if alien.rect.right >= screen_width:
				self.alien_direction = -1
				self.alien_move_down(2)
			elif alien.rect.left <= 0: 
				self.alien_direction = 1
				self.alien_move_down(2)

	def alien_move_down(self,distance):
		if self.aliens:
			for alien in self.aliens.sprites():
				alien.rect.y += distance


	def alien_shoot(self):
		if self.aliens.sprites():
			random_alien = choice(self.aliens.sprites())
			laser_sprite = Laser(random_alien.rect.center,6,screen_height)
			self.alien_lasers.add(laser_sprite)
			self.laser_sound.play()

	def extra_alien_timer(self):
		self.extra_spawn_time -= 1
		if self.extra_spawn_time <= 0:
			self.extra.add(Ufo(choice(['right','left']),screen_width))
			self.extra_spawn_time = randint(400,800)

	def collision_checks(self):
		global music
		panic_sound = pygame.mixer.Sound('audio/panic1.wav')
		panic_sound_played = False
		if self.player.sprite and self.player.sprite.lasers:
			for laser in self.player.sprite.lasers:
				if pygame.sprite.spritecollide(laser,self.blocks,True):
					laser.kill()
				aliens_hit = pygame.sprite.spritecollide(laser,self.aliens,True)
    
				if aliens_hit:
					for alien in aliens_hit:
						self.score += alien.value
					self.alien_speed *= self.alien_speed_multiplier
					explosion = Explosion(alien.rect.centerx, alien.rect.centery,2)  
					explosion_group.add(explosion)
					laser.kill()
					self.explosion_sound.play()
     
				if pygame.sprite.spritecollide(laser,self.blocks,True):
					laser.kill()
				ufo_hit = pygame.sprite.spritecollide(laser,self.extra,True)
				if ufo_hit:
					for ufo in ufo_hit:
						self.score += 500
					explosion = UfoExplosion(ufo.rect.centerx,ufo.rect.centery,2)  
					explosion_group.add(explosion)
					laser.kill()


		if self.alien_lasers:
			for laser in self.alien_lasers:
				if pygame.sprite.spritecollide(laser,self.blocks,True):
					laser.kill() 
					explosion = Explosion(laser.rect.centerx, laser.rect.centery,1)
					explosion_group.add(explosion)
				if pygame.sprite.spritecollide(laser,self.player,False):
					laser.kill()
					self.lives -= 1
					explosion = Explosion(self.player.sprite.rect.centerx, self.player.sprite.rect.centery,5)
					explosion_group.add(explosion)
					if self.lives < 0:
						explosion = PlayerExplosion(self.player.sprite.rect.centerx, self.player.sprite.rect.centery,5)
						explosion_group.add(explosion)  
						laser.kill()
					if self.lives == 0:
						self.player.sprite.kill()
					
		if self.aliens:
			for alien in self.aliens:
				pygame.sprite.spritecollide(alien,self.blocks,True)
				if pygame.sprite.spritecollide(alien,self.player,False):
					explosion = Explosion(self.player.sprite.rect.centerx, self.player.sprite.rect.centery,10)
					explosion_group.add(explosion)
					pygame.time.wait(2000)
					self.reset_game()
					pygame.quit()
					sys.exit()
    
	panic_sound = False

	def update_aliens(self):
		for alien in self.aliens:
			alien.rect.x += self.alien_direction * self.alien_speed
		self.alien_position_checker()
  
	def display_lives(self):
		for live in range(self.lives - 1):
			x = self.live_x_start_pos + (live * (self.live_surf.get_size()[0] + 10))
			screen.blit(self.live_surf,(x,8))

	def display_score(self):
		score_surf = self.font.render(f'score: {self.score}',False,'white')
		score_rect = score_surf.get_rect(topleft = (10,-10))
		screen.blit(score_surf,score_rect)

	def victory_message(self):
		if not self.aliens.sprites():
			victory_surf = self.font.render('You won',False,'white')
			victory_rect = victory_surf.get_rect(center = (screen_width / 2, screen_height / 2))
			screen.blit(victory_surf,victory_rect)

	def reset_game(self):
		self.lives = 3
		self.score = 0
		self.blocks.empty()
		self.create_multiple_obstacles(*self.obstacle_x_positions, x_start=screen_width / 15, y_start=480)

		self.aliens.empty()
		self.alien_setup(rows=4, cols=8)

		self.alien_lasers.empty()
		self.extra.empty()
		self.extra_spawn_time = randint(40, 80)

	def run(self):
		if self.player.sprite:
			self.player.update()
		self.alien_lasers.update()
		self.extra.update()
		self.aliens.update(self.alien_direction)
		self.alien_position_checker()
		self.extra_alien_timer() 
		self.update_aliens() 
		self.collision_checks()
		explosion_group.update()
		if self.player.sprite:
			self.player.sprite.lasers.draw(screen)
			self.player.draw(screen)
   
		self.blocks.draw(screen)
		self.aliens.draw(screen)
		self.alien_lasers.draw(screen)
		self.extra.draw(screen)
		explosion_group.draw(screen)
  
		self.display_lives()
		self.display_score()
		self.victory_message()


		if self.lives == 0:
			pygame.time.wait(2000)
			global game_state
			save_high_score(self.score)
			game_state = START_SCREEN
			self.reset_game()

explosion_group = pygame.sprite.Group()

if __name__ == '__main__':
	pygame.init()
	screen_width = 600
	screen_height = 600
	screen = pygame.display.set_mode((screen_width,screen_height))
	clock = pygame.time.Clock()
	game = Game()

	ALIENLASER = pygame.USEREVENT + 1
	pygame.time.set_timer(ALIENLASER,800)

	while True:
		if game_state == START_SCREEN:
			main_menu()
		elif game_state == GAME:
			screen.fill((30, 30, 30))
			game.run()
		elif game_state == HIGH_SCORE:
			high_score_screen()


		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == ALIENLASER and game_state == GAME:
				game.alien_shoot()

		screen.fill((30,30,30))
		game.run()
			
		pygame.display.flip()
		clock.tick(60)