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

	def check_hit(self, alien_bullets):
		pass

	def fire(self):
		if len(self.bullets) > 0:
			return
		self.bullets.append(Bullet(self.x + int(self.width // 2), self.y - 10))

	def update(self):
		for b in self.bullets:
			b.y -= b.velocity
			if b.y + b.height < 0:
				self.bullets.remove(b)
				continue

	def move(self, winx, winy, direction):
		move_speed = 30 # pixels

		# Check to see if we need to move down a row
		result = False

		if self.x + self.width + move_speed >= winx:
			self.x -= move_speed
			return
		if self.x - move_speed <= 0:
			self.x += move_speed
			return

		self.x += move_speed * direction

		return result

	def render(self, rendertarget):
		for b in self.bullets:
			b.render(rendertarget)

		rendertarget.blit(self.image, (self.x, self.y))
