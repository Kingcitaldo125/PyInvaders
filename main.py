import pygame

black = (0,0,0)
red = (255,0,0)
white = (255,255,255)
green = (0,128,64)

def main(winx=800, winy=600):
	pygame.display.init()

	screen = pygame.display.set_mode((winx, winy))
	clock = pygame.time.Clock()

	done = False

	while not done:
		clock.tick(10)
		events = pygame.event.get()

		for e in events:
			if e.type == pygame.MOUSEBUTTONDOWN:
				mx,my = e.pos[0],e.pos[1]
				print(f"Mouse x {mx} y {my}")
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_ESCAPE:
					done = True
					break

		screen.fill(black)
		pygame.display.flip()

	pygame.display.quit()

if __name__ == "__main__":
	main()
