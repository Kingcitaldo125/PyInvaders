import pygame

from time import sleep
from random import randrange

from threading import Thread

from alien import Alien, Spaceship
from player import Player
from bullet import Bullet


black = (0,0,0)
white = (255,255,255)
green = (50,255,0)

done = False

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

def update_aliens_movement(winx, winy, aliens):
	global done
	row_update = 0
	interval = 1

	while not done:
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

		sleep(interval)

def main(winx=800, winy=600):
	global done

	pygame.display.init()

	screen = pygame.display.set_mode((winx, winy))
	clock = pygame.time.Clock()

	aliens = setup(winx, winy)
	player = Player(winx/2, winy-50)

	alien_bullets = []
	spaceship = None

	row_update = 0

	alien_updater = Thread(target=update_aliens_movement, args=(winx, winy, aliens))

	alien_updater.start()

	while not done:
		clock.tick(10)

		player.update()

		for a in aliens:
			rn = randrange(0,1000)
			if rn == 123:
				alien_bullets.append(Bullet(a.x, a.y))

		for bt in alien_bullets:
			bt.y += bt.velocity

		if spaceship is not None:
			spaceship.update()

			# Check out of bounds on the spaceship
			if spaceship.direction == -1:
				if spaceship.x <= -10:
					spaceship = None
			else:
				if spaceship.x >= winx + 10:
					spaceship = None

		if spaceship is None:
			srn = randrange(0,100)
			if srn == 50:
				spaceship = Spaceship(-10, 20)

		for e in pygame.event.get():
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_SPACE:
					player.fire()
				if e.key == pygame.K_LEFT:
					player.move(winx, winy, -1)
				if e.key == pygame.K_RIGHT:
					player.move(winx, winy, 1)
				if e.key == pygame.K_ESCAPE:
					done = True
					break

		screen.fill(black)

		player.render(screen)

		if spaceship is not None:
			spaceship.render(screen)

		for a in aliens:
			a.render(screen)

		for bt in alien_bullets:
			bt.render(screen)

		pygame.display.flip()

	alien_updater.join()
	pygame.display.quit()

if __name__ == "__main__":
	main()
