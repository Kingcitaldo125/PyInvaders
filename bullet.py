from pygame import draw


class Bullet():
	def __init__(self, x, y, velocity=0.5):
		self.x = x
		self.y = y
		self.width = 2
		self.height = 15
		self.velocity = velocity #pixels per update

	def render(self, rendertarget):
		draw.rect(rendertarget, (255,255,255), (self.x, self.y, self.width, self.height))
		#draw.circle(rendertarget, (255,255,255), (int(self.x), int(self.y)), 3)
