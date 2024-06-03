from pygame import image, transform

from os.path import abspath, join

from bullet import Bullet


class Player():
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.width = 25
		self.height = 20
		self.xoffset = 20
		self.yoffset = 10
		self.image = None
		self.bullets = []

		image_folder = join('\\'.join(abspath(__file__).split('\\')[:-1]), "images/")

		self.image = image.load(join(image_folder, "player.png")).convert_alpha()
		self.image = transform.scale(self.image, (self.width, self.height))

	def check_hit(self, bullet):
		pass

	def fire(self):
		self.bullets.append(Bullet(self.x, self.y))

	def update(self):
		for b in self.bullets:
			b.update()

	def move(self, winx, winy, direction):
		move_speed = 30 # pixels

		# Check to see if we need to move down a row
		result = False

		if self.x + self.width + move_speed >= winx:
			return
		if self.x - move_speed <= 0:
			return

		self.x += move_speed * direction

		return result

	def render(self, rendertarget):
		rendertarget.blit(self.image, (self.x, self.y))
