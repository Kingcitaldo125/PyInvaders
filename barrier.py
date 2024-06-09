from pygame import draw


class Barrier():
	def __init__(self, x, y, width, height):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.green = (50,255,0)
		self.shards = []
		self.shard_width = 5
		self.shard_height = 5

		xstep = self.shard_width + 1
		ystep = self.shard_height + 1
		shard_depth = 2

		# Generate the shards
		for i in range(self.x + self.shard_width, self.x + self.shard_width + self.width, xstep):
			for j in range(self.y + self.shard_height, self.y + self.shard_height + self.height, ystep):
				for k in range(shard_depth):
					self.shards.append((i + k, j + k))

	def depleted(self):
		return len(self.shards) == 0

	def check_shard_collision(self, player_bullets, alien_bullets):
		if len(self.shards) < 1:
			return

		for bullet in player_bullets:
			for shard in self.shards:
				bx,by = bullet.x,bullet.y
				sx,sy = shard[0], shard[1]
				if bx >= sx and bx <= (sx + self.shard_width):
					if by <= (sy + self.shard_height) and (by + bullet.height) >= sy:
						self.shards.remove(shard)
						player_bullets.remove(bullet)
						break

		for bullet in alien_bullets:
			for shard in self.shards:
				bx,by = bullet.x,bullet.y
				sx,sy = shard[0], shard[1]
				if bx >= sx and bx <= (sx + self.shard_width):
					if by <= (sy + self.shard_height) and (by + bullet.height) >= sy:
						self.shards.remove(shard)
						alien_bullets.remove(bullet)
						break

	def render(self, rendertarget):
		for shard in self.shards:
			draw.rect(rendertarget, self.green, (int(shard[0]), int(shard[1]), self.shard_width, self.shard_height))
