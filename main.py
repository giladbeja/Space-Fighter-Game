import pygame
import os
import pygame_menu
import random
pygame.font.init()
pygame.mixer.init()
pygame.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("First game")

snd = False

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

rxloc = []
ryloc = []

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))
backgroundmusic = pygame.mixer.Sound(os.path.join('Assets', 'background+music.mp3'))
pygame.mixer.Sound.set_volume(backgroundmusic, 0.05)
pygame.mixer.Sound.set_volume(BULLET_FIRE_SOUND, 0.5)
pygame.mixer.Sound.set_volume(BULLET_HIT_SOUND, 0.5)


HEALTH_FONT = pygame.font.SysFont('Arial', 40)
WINNER_FONT = pygame.font.SysFont('Arial', 40)

FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 3

shipwidth, shipheight = 55,40

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2
WINDOWRESIZED = pygame.USEREVENT + 3

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
	YELLOW_SPACESHIP_IMAGE, (shipwidth, shipheight)), 90)
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
	RED_SPACESHIP_IMAGE, (shipwidth, shipheight)), 270)

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
	for bullet in yellow_bullets:
		bullet.x += BULLET_VEL
		if red.colliderect(bullet):
			pygame.event.post(pygame.event.Event(RED_HIT))
			yellow_bullets.remove(bullet)
		elif bullet.x > WIDTH:
			yellow_bullets.remove(bullet)
			
	for bullet in red_bullets:
		bullet.x -= BULLET_VEL
		if yellow.colliderect(bullet):
			pygame.event.post(pygame.event.Event(YELLOW_HIT))
			red_bullets.remove(bullet)
		elif bullet.x < 0:
			red_bullets.remove(bullet)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

def draw_winner(text):
	draw_text = WINNER_FONT.render(text, 1, WHITE)
	WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
	pygame.display.update()
	pygame.time.delay(3000)
def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
	WIN.blit(SPACE, (0,0))
	pygame.draw.rect(WIN, BLACK, BORDER)

	red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
	yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
	WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
	WIN.blit(yellow_health_text, (10, 10))


	
	WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
	WIN.blit(RED_SPACESHIP, (red.x, red.y))

	for bullet in red_bullets:
		pygame.draw.rect(WIN, RED, bullet)
	for bullet in yellow_bullets:
		pygame.draw.rect(WIN, YELLOW, bullet)
	
	pygame.display.update()
		
def yellow_handle_movement(keys_pressed, yellow):
		if keys_pressed[pygame.K_a] and yellow.x - VEL > 0: #LEFT
			yellow.x -= VEL
		if keys_pressed[pygame.K_d] and yellow.x + VEL +yellow.width < BORDER.x: #RIGHT
			yellow.x += VEL
		if keys_pressed[pygame.K_w] and yellow.y - VEL > 0: #UP
			yellow.y -= VEL
		if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15: #DOWN
			yellow.y += VEL
			
def red_handle_movement(keys_pressed, red):
		if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width: #LEFT
			red.x -= VEL
		if keys_pressed[pygame.K_RIGHT] and red.x + VEL +red.width < WIDTH: #RIGHT
			red.x += VEL
		if keys_pressed[pygame.K_UP] and red.y - VEL > 0: #UP
			red.y -= VEL
		if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15: #DOWN
			red.y += VEL

def red_ai_movement(test, red):
	rxloc = random.randint(475, 860)
	ryloc = random.randint(15, 450)
	print(rxloc, ryloc)
	if red.x != rxloc:
		if red.x < rxloc:
			for i in range(10):
				red.x += 1
		elif red.x > rxloc:
			for i in range(10):
				red.x -= 1
	if red.y != ryloc:
		if red.y < ryloc:
			for i in range(10):
				red.y += 1
		elif red.y > ryloc:
			for i in range(10):
				red.y -= 1
	if red.y == ryloc and red.x == rxloc:
		pygame.time.delay(1000)



def splayer():
	mode = True
	start_the_game(True)

def mplayer():
	mode = False
	start_the_game(False)


def start_the_game(mode):
	# Do the job here !
	red = pygame.Rect(700, 300, shipwidth, shipheight)
	yellow = pygame.Rect(100, 300, shipwidth, shipheight)

	red_bullets = []
	yellow_bullets = []

	red_health = 10
	yellow_health = 10
	
	clock = pygame.time.Clock()
	run = True
	while run:
		clock.tick(FPS)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()
				print("player quit")

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q and len(yellow_bullets) < MAX_BULLETS:
					bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
					yellow_bullets.append(bullet)
					if snd == True:
						BULLET_FIRE_SOUND.play()

				if event.key == pygame.K_SPACE and len(red_bullets) < MAX_BULLETS:
					bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
					red_bullets.append(bullet)
					if snd == True:
						BULLET_FIRE_SOUND.play()

			if event.type == RED_HIT:
				red_health -=1
				if snd == True:
					BULLET_HIT_SOUND.play()
				
			if event.type == YELLOW_HIT:
				yellow_health -= 1
				if snd == True:
					BULLET_HIT_SOUND.play()


		winner_text = ""
		if red_health <= 0:
			winner_text = "Player 1 wins!"
		if yellow_health <= 0:
			winner_text = "Player 2 wins!"
		if winner_text != "":
			draw_winner(winner_text)
			menu.mainloop(WIN)
			pygame.mixer.stop()
			break
		
		test = pygame.event.pump()
		keys_pressed = pygame.key.get_pressed()
		yellow_handle_movement(keys_pressed, yellow)
		if mode == False:
			red_handle_movement(keys_pressed, red)
		elif mode == True:
			red_ai_movement(test, red)
		handle_bullets(yellow_bullets, red_bullets, yellow, red)
		draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)


def flscrn():
	WIN = pygame.display.set_mode((get_screen, HEIGHT), pygame.FULLSCREEN)
	pygame.display.update()


menu = pygame_menu.Menu('SpaceWars', WIDTH, HEIGHT,
					   theme=pygame_menu.themes.THEME_SOLARIZED)



menu.add.text_input('Name : ')
#menu.add.button('Play', start_the_game)
#menu.add.button('Toggle Fullscreen', flscrn)
menu.add.button('Singleplayer', splayer)
menu.add.button('Multiplayer', mplayer)
menu.add.button('Quit', pygame_menu.events.EXIT)

def main():
		if snd == True:
			pygame.mixer.Sound.play(backgroundmusic)
		menu.mainloop(WIN)

if __name__ == "__main__":
	main()
