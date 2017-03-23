"""Pain Train the Video Game, by Charlie Weiss and Diego Garcia"""
"""TODO:
- Obstacle placement
- Graphic design
- Interactive Start screen
- Interactive End screen
- Pain Train name"""

import pygame
import math

# Colors
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (0,0,255)
DIMGRAY = (105,105,105)
SLATEGRAY = (112,128,144)

"""Model classes"""
class Player(object):
	def __init__(self,x=0,y=0,width=50,height=50,dx=1,dy=0,shiftdx=0,jumpdy=-.75):
		# places player below and to the right of the coordinate given
		self.x = x
		self.y = y-height
		self.width = width
		self.height = height
		self.dx = dx
		self.dy = dy
		self.shiftdx = shiftdx
		self.jumpdy = jumpdy # variable dy is set to when controller jumps

	def train_wreck(self, train):
		return (train.x+train.width) > self.x

	def shift_world(self):
		return self.x > 350

	def go_back(self):
		return self.x < 130

	def hit_platform(self,platform):
		return (self.y + self.height) > platform.y and (self.y + self.height) < (platform.y+platform.height) and self.x < (platform.x+platform.width) and (self.x+self.width) > platform.x

	def fall_to_death(self):
		return self.y > 480

	def on_platform(self,platform):
		return self.x < (platform.x+platform.width) and (self.x+self.width) > platform.x and (self.y+self.height)==platform.y

class PainTrain(object):
	def __init__(self,x=0,y=0,width=200,height=200,constdx=.05,dx=0,shiftdx=-1):
		# places train centered above coordinate given
		self.x = x
		self.y = y-height
		self.width = width
		self.height = height
		self.constdx = constdx
		self.dx = dx
		self.shiftdx = shiftdx

	def step(self):
		self.x += self.constdx

# classes for level objects
class Ground(object):
	def __init__(self, x = 0, y = 300, width = 2400, height = 180,dx=0,shiftdx=-1):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.dx = dx
		self.shiftdx = shiftdx

class Platform(object):
	def __init__(self, x=0,y=0,width = 100, height = 20, dx=0, shiftdx=-1):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.dx = dx
		self.shiftdx = shiftdx

"""View classes"""
class PlayerView(object):
	def __init__(self, model):
		self.model = model

	def draw(self, surface):
		model = self.model
		# this takes (x,y,width,height)
		pygame.draw.rect(surface,SLATEGRAY,(model.x,model.y,model.width,model.height))

class PainTrainView(object):
	def __init__(self, model):
		self.model = model

	def draw(self, surface):
		model = self.model
		# this takes (x,y,width,height)
		pygame.draw.rect(surface,BLACK,(model.x,model.y,model.width,model.height))

class GroundView(object):
	def __init__(self, model):
		self.model = model

	def draw(self, surface):
		model = self.model
		# this takes (x,y,width,height)
		pygame.draw.rect(surface,DIMGRAY,(model.x,model.y,model.width,model.height))

class ObstacleView(object):
	# can be used for any rectangular object
	def __init__(self,model):
		self.model = model

	def draw(self,surface):
		model = self.model
		pygame.draw.rect(surface,BLACK,(model.x,model.y,model.width,model.height))

"""Controller classes"""
class Controller(object):
	def __init__(self,models):
		self.models = models
		self.player = models[0] # make sure this aligns with all_models in main

	def handle_event(self):
		# time passed isn't actually time based... based on while loop efficiency
		player = self.player
		models = self.models
		jump = False
		keys = pygame.key.get_pressed() # checking pressed keys
		for model in models:
			if keys[pygame.K_LEFT]:
				if player.go_back():
					model.x -= model.shiftdx
				else:
					model.x -= model.dx
			if keys[pygame.K_RIGHT]:
				if player.shift_world():
					model.x += model.shiftdx
				else:
					model.x += model.dx
			if model.y and player.on_platform(model):
				jump = True

		if keys[pygame.K_UP] and jump==True:
			player.dy = player.jumpdy

def main():
	pygame.init()
	screen = pygame.display.set_mode((640,480))

	# Images
	gameover = pygame.image.load('gameover1.bmp').convert()

	# models
	# level models:
	ground1 = Ground(width=1500, x=0) #x=0?
	ground2 = Ground(width=1500, x=1800)
	platform1 = Platform(800,10)
	platform2 = Platform(1200,200)
	platform3 = Platform(1600,10)
	platform4 = Platform(2200,10)
	platform5 = Platform(2400,10)
	# player/NPC models:
	player = Player(300,300)
	train = PainTrain(0,300)
	#models = [train, player, ground, platform1]
	all_models = [player,train,ground1,ground2,platform1,platform2,platform3,platform4,platform5]
	collision_models = [ground1,ground2,platform1,platform2,platform3,platform4,platform5]

	# views
	views = []
	views.append(PlayerView(player))
	views.append(PainTrainView(train))
	views.append(GroundView(ground1))
	views.append(GroundView(ground2))
	views.append(ObstacleView(platform1))
	views.append(ObstacleView(platform2))
	views.append(ObstacleView(platform3))
	views.append(ObstacleView(platform4))
	views.append(ObstacleView(platform5))

	# controller
	controller = Controller(all_models)
	running = True
	counter = 0

	# variable to make speed lower
	delta_speed = .00005 # good one is .00005

	while running == True:
		counter += 1
		if counter%5 == 0: # adjust if it's running too slow. A little jank, sorry.
			controller.handle_event()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

		if player.train_wreck(train) or player.fall_to_death():
			train.constdx = 0
			player.dx = 0
			running = False

		#for ground in ground_models:
		#	if not player.hit_platform(ground) and player.dy==0:
		#		player.dy = .001


		# keep train moving
		train.step()

		# code for player jumping
		player.y += player.dy
		# make player fall
		if player.dy != 0:
			player.dy += 0.001 # if you lower this, also lower jumpdy in player class
		# make player's jump speed lower with time
		if player.jumpdy < -.05:
			player.jumpdy += delta_speed

		#handle collisions
		for model in collision_models:
			if player.hit_platform(model) and player.dy>0:
				player.dy = 0
				player.y = model.y - player.height
			elif player.hit_platform(model) and player.dy<0:
				player.y = model.y+model.height
				player.dy = .001
			if not player.on_platform(model) and player.dy==0:
				player.dy = .001

		# decrease speed of player (and all things relative to it)
		for model in all_models:
			# good delta speed is .00005
			if model.dx > .01:
				model.dx -= delta_speed
			elif model.dx < -.01:
				model.dx += delta_speed
			if model.shiftdx > .01:
				model.shiftdx -= delta_speed
			elif model.shiftdx < -.01:
				model.shiftdx += delta_speed

		screen.fill(WHITE)
		for view in views:
			view.draw(screen)

		pygame.display.update()

	running = True
	while running == True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
		screen.blit(gameover,(60,60))
		pygame.display.flip()

	pygame.quit()

if __name__ == '__main__':
	main()
