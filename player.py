from pygame import draw, image, transform

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
		self.image1 = None
		self.image2 = None
		self.bullets = []
		self.dead = False

		image_folder = join('\\'.join(abspath(__file__).split('\\')[:-1]), "images/")
		kind_str1 = f"player.png"
		kind_str2 = f"player_dead.png"

		self.image1 = image.load(join(image_folder, kind_str1)).convert_alpha()
		self.image1 = transform.scale(self.image1, (self.width, self.height))

		self.image2 = image.load(join(image_folder, kind_str2)).convert_alpha()
		self.image2 = transform.scale(self.image2, (self.width, self.height))

	def check_hit(self, alien_bullets):
		pass

	def set_dead(self):
		self.dead = True

	def unset_dead(self):
		self.dead = False

	def clear_bullets(self):
		self.bullets = []

	def fire(self):
		if len(self.bullets) > 0:
			return
		self.bullets.append(Bullet(self.x + int(self.width // 2), self.y - 10, velocity=1))

	def move(self, winx, winy, direction):
		move_speed = 20 # pixels

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

		if not self.dead:
			rendertarget.blit(self.image1, (self.x, self.y))
		else:
			rendertarget.blit(self.image2, (self.x, self.y))
		#draw.rect(rendertarget, (255,255,255), (self.x, self.y, self.width, self.height), 1)
