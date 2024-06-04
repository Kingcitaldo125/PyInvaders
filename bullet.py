from pygame import draw


class Bullet():
	def __init__(self, x, y, velocity=50):
		self.x = x
		self.y = y
		self.width = 3
		self.height = 8
		self.velocity = velocity #pixels per update

	def check_update(self, winy):
		return self.y <= winy

	def render(self, rendertarget):
		draw.rect(rendertarget, (255,255,255), (self.x, self.y, self.width, self.height))
