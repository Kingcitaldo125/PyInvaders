from pygame import image, transform, draw

from os.path import abspath, join
from random import randint


class Spaceship():
	def __init__(self, x, y, direction):
		self.x = x
		self.y = y
		self.width = 35
		self.height = 20
		self.move_pixels = 10
		self.image = None
		self.direction = direction

		image_folder = join('\\'.join(abspath(__file__).split('\\')[:-1]), "images/")

		self.image = image.load(join(image_folder, "spaceship.png")).convert_alpha()
		self.image = transform.scale(self.image, (self.width, self.height))

	def update(self):
		self.x += self.move_pixels * self.direction

	def render(self, rendertarget):
		rendertarget.blit(self.image, (self.x, self.y))

class Alien():
	def __init__(self, x, y, kind_int):
		self.x = x
		self.y = y
		self.width = 25
		self.height = 20
		self.move_pixels = 20
		#self.xoffset = 20
		#self.yoffset = 10
		self.image1 = None
		self.image2 = None
		self.flip = True
		self.direction = 1

		image_folder = join('\\'.join(abspath(__file__).split('\\')[:-1]), "images/")
		kind_str1 = f"Alien{kind_int}1.png"
		kind_str2 = f"Alien{kind_int}2.png"

		self.image1 = image.load(join(image_folder, kind_str1)).convert_alpha()
		self.image1 = transform.scale(self.image1, (self.width, self.height))

		self.image2 = image.load(join(image_folder, kind_str2)).convert_alpha()
		self.image2 = transform.scale(self.image2, (self.width, self.height))

	def check_hit(self, bullet):
		pass

	def flip_direction(self):
		self.direction = self.direction * -1

	def row_update(self):
		self.flip = False if self.flip == True else True
		self.y += self.move_pixels

	def check_update(self, winx, winy):
		# Check to see if we need to move down a row
		result = 0

		if self.x + self.width + self.move_pixels >= winx:
			result = 1
		elif self.x <= 0:
			result = 2

		return result

	def update(self, winx, winy):
		self.flip = False if self.flip == True else True
		self.x += self.move_pixels * self.direction

	def render(self, rendertarget):
		if self.flip:
			rendertarget.blit(self.image1, (self.x, self.y))
		else:
			rendertarget.blit(self.image2, (self.x, self.y))
		#draw.rect(rendertarget, (255,255,255), (self.x, self.y, self. width, self.height), 1)