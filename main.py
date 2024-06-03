import pygame

from time import sleep

from alien import Alien
from player import Player

black = (0,0,0)
white = (255,255,255)
green = (50,255,0)

def setup(winx, winy):
	aliens = []
	xoffset = winx * 0.15
	yoffset = winy * 0.15
	xmove_offset = 15
	ymove_offset = 15
	x = xoffset
	y = yoffset

	for j in range(11):
		aliens.append(Alien(x, y, 3))
		x += (winx / xmove_offset)

	x = xoffset
	y += (winy / ymove_offset)

	for i in range(2):
		for j in range(11):
			aliens.append(Alien(x, y, 2))
			x += (winx / xmove_offset)
		x = xoffset
		y += (winy / ymove_offset)

	for i in range(2):
		for j in range(11):
			aliens.append(Alien(x, y, 1))
			x += (winx / xmove_offset)
		x = xoffset
		y += (winy / ymove_offset)

	return aliens

def update_aliens(winx, winy, aliens, row_update):
	rupdate = row_update
	for a in aliens:
		if rupdate == 1:
			a.x -= (a.move_pixels)
			a.flip_direction()
			row_update = 0
		elif rupdate == 2:
			a.x += (a.move_pixels)
			a.flip_direction()
			row_update = 0

	for a in aliens:
		res = a.check_update(winx, winy)
		if res != 0:
			row_update = res
			break

	if row_update == 1:
		for a in aliens:
			a.row_update()
	elif row_update == 2:
		for a in aliens:
			a.row_update()
	else:
		for a in aliens:
			a.update(winx, winy)

	return row_update

def main(winx=800, winy=600):
	pygame.display.init()

	screen = pygame.display.set_mode((winx, winy))
	#clock = pygame.time.Clock()

	aliens = setup(winx, winy)
	player = Player(winx/2, winy-50)

	interval = 0.5

	row_update = 0
	done = False

	while not done:
		player.update()

		row_update = update_aliens(winx, winy, aliens, row_update)

		for e in pygame.event.get():
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_SPACE:
					print("Fire!")
				if e.key == pygame.K_LEFT:
					player.move(winx, winy, -1)
				if e.key == pygame.K_RIGHT:
					player.move(winx, winy, 1)
				if e.key == pygame.K_ESCAPE:
					done = True
					break

		screen.fill(black)

		player.render(screen)

		for a in aliens:
			a.render(screen)

		pygame.display.flip()

		sleep(interval)

	pygame.display.quit()

if __name__ == "__main__":
	main()
