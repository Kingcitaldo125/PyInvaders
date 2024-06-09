import pygame

from time import sleep
from random import randrange

from threading import Lock, Thread

from alien import Alien, Spaceship
from player import Player
from bullet import Bullet
from barrier import Barrier


black = (0,0,0)
white = (255,255,255)
green = (50,255,0)

done = False
glock = Lock()

def setup_barriers(winx, winy):
	barriers = []
	xpos = winx * 0.15
	ypos = winy * 0.75
	width = 75
	height = 25

	for i in range(4):
		barriers.append(Barrier(int(xpos), int(ypos), width, height))
		xpos += winx * 0.2

	return barriers

def setup_aliens(winx, winy):
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
	global done, glock
	row_update = 0
	interval = 1

	while not done:
		rupdate = row_update
		with glock:
			for a in aliens:
				# Figure out which direction they will move
				if rupdate == 1:
					a.x -= (a.move_pixels)
					a.flip_direction()
					row_update = 0
				elif rupdate == 2:
					a.x += (a.move_pixels)
					a.flip_direction()
					row_update = 0

			if done:
				break

			for a in aliens:
				res = a.check_update(winx, winy)
				if res != 0:
					row_update = res
					# Make the aliens move faster
					# after they finish strafing the current row
					interval -= 0.05
					break

			# If any alien hit a wall, move the formation down a row
			if row_update != 0:
				for a in aliens:
					a.row_update()
			else:
				for a in aliens:
					a.update(winx, winy)

		sleep(interval)

def update_player_aliens(player, aliens, dt):
	global glock
	if len(player.bullets) < 1:
		return

	# Move the player's bullets
	for bt in player.bullets:
		bt.y -= bt.velocity * dt
		if bt.y < 0:
			player.bullets.remove(bt)
			continue

	results = False
	y_collision_offset = 5
	
	with glock:
		for a in aliens:
			acoll1 = (a.x + a.width) >= player.x and a.x <= (player.x + player.width)
			acoll2 = (a.y + a.height) >= player.y and a.y <= (player.y + player.height)

			# Alien hit the player
			if acoll1 and acoll2:
				return True

			if len(player.bullets) < 1:
				continue

			# Handle bullet position updates and bullet-alien collision
			for bt in player.bullets:
				xcoll = (bt.x + bt.width) >= a.x and bt.x <= (a.x + a.width)
				ycoll = (bt.y + (bt.height * 2)) >= a.y and (bt.y - y_collision_offset) <= (a.y + a.height)

				if xcoll and ycoll:
					aliens.remove(a)
					player.bullets.remove(bt)
					break

	return results

def g_render(screen, player, spaceship, aliens, barriers, alien_bullets):
	screen.fill(black)

	player.render(screen)

	if spaceship is not None:
		spaceship.render(screen)

	for a in aliens:
		a.render(screen)

	for b in barriers:
		b.render(screen)

	for bt in alien_bullets:
		bt.render(screen)

def main(screen, aliens, barriers, winx, winy):
	global done

	clock = pygame.time.Clock()

	player = Player(winx/2, winy-50)

	alien_bullets = []
	spaceship = None

	row_update = 0

	alien_updater.start()

	while not done:
		dt = clock.tick(30)

		# Handle bullets hitting a barrier shard
		for barrier in barriers:
			barrier.check_shard_collision(player.bullets, alien_bullets)

		res = update_player_aliens(player, aliens, dt)

		# Alien hit the player
		if res:
			print("Player Dead!")
			print("Game Over!")
			player.set_dead()
			g_render(screen, player, spaceship, aliens, alien_bullets)
			pygame.display.flip()
			sleep(3)
			return

		if spaceship is not None:
			for bt in player.bullets:
				xcoll = (bt.x + bt.width) >= spaceship.x and bt.x <= (spaceship.x + a.width)
				ycoll = (bt.y + (bt.height * 2)) >= spaceship.y and (bt.y - 1) <= (spaceship.y + a.height)

				if xcoll and ycoll:
					spaceship = None
					player.bullets.remove(bt)

		for a in aliens:
			rn = randrange(0,1000)
			if rn == 123:
				alien_bullets.append(Bullet(a.x, a.y))

		for bt in alien_bullets:
			bt.y += bt.velocity * dt
			if bt.y >= winy:
				alien_bullets.remove(bt)
				continue

			xcoll = (bt.x + bt.width) >= player.x and bt.x <= (player.x + player.width)
			ycoll = (bt.y + bt.height) >= player.y

			if xcoll and ycoll:
				print("Player Dead!")
				alien_bullets = []
				player.set_dead()
				player.clear_bullets()
				g_render(screen, player, spaceship, aliens, barriers, alien_bullets)
				pygame.display.flip()
				sleep(3)
				player.unset_dead()

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
			srn = randrange(0,1000)
			if srn == 50: # create the spaceship
				direction = randrange(0,2)
				direction = -1 if direction == 0 else 1
				spaceship = Spaceship(-10 if direction == 1 else winx + 10, 20, direction)

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

		g_render(screen, player, spaceship, aliens, barriers, alien_bullets)
		pygame.display.flip()

if __name__ == "__main__":
	winx=800
	winy=600

	pygame.display.init()
	screen = pygame.display.set_mode((winx, winy))

	aliens = setup_aliens(winx, winy)
	barriers = setup_barriers(winx, winy)
	alien_updater = Thread(target=update_aliens_movement, args=(winx, winy, aliens))

	try:
		main(screen, aliens, barriers, winx, winy)
	except Exception as e:
		print(e)
		done = True
		alien_updater.join()

	if alien_updater.is_alive():
		alien_updater.join()

	pygame.display.quit()
