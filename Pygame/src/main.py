import math
import random
import sys

import pygame
from pygame import mixer

# Initialize pygame
pygame.init()

# Screen dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))

# Title & Icon
pygame.display.set_caption("2D Space Invaders: A nostalgia game")
icon = pygame.image.load('icon.jpg')
pygame.display.set_icon(icon)

# Load the background image
background_image = pygame.image.load("background.png")
background_rect = background_image.get_rect()

# background Sound
mixer.music.load('bg.mp3')
mixer.music.play(-1)

# Initial position of the background
background_y = 0

clock = pygame.time.Clock()
fps = 60

# player
playerImg = pygame.image.load('f.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enm.png'))
    enemyX.append(random.randint(0, 710))
    enemyY.append(random.randint(40, 150))
    enemyX_change.append(2)
    enemyY_change.append(40)

# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 6
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('Pixel Destroyed.ttf', 32)

textX = 10
textY = 10

# Game over text
over_font = pygame.font.Font('HFHourglass.ttf', 50)

# Power-ups
power_ups = []
last_powerup_time = pygame.time.get_ticks()
powerup_interval = 6000  # Set the interval to 4 seconds
powerup_counter = 0
max_powerups_per_interval = random.randint(2, 3)  # Set the maximum number of power-ups per interval
power_upsX = 736
power_upsY = 600


class PowerUp(pygame.sprite.Sprite):
    POWERUP_IMAGES = {
        "speed_boost": pygame.image.load('star_yellow.png'),  # Replace 'speed_boost.png' with your image
        "shield": pygame.image.load('shield.png'),  # Replace 'shield.png' with your image
        "double_score": pygame.image.load('star_yellow.png')  # Replace 'double_score.png' with your image
    }

    def __init__(self, x, y, powerup_type):
        super().__init__()
        self.image = self.POWERUP_IMAGES.get(powerup_type, pygame.Surface((20, 20), pygame.SRCALPHA))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 1
        self.powerup_type = powerup_type

    def update(self):
        self.rect.y += self.speed


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render(f'''GAME OVER''', True, (255, 255, 255))
    screen.blit(over_text, (250, 250))

    larger_font = pygame.font.Font('Pixel Destroyed.ttf', 50)
    score_text = larger_font.render(f"Your Score: {score_value}", True, (255, 255, 255))
    screen.blit(score_text, (250, 320))

    for countdown in range(5, 0, -1):
        # Clear the previous countdown text
        screen.fill((139, 0, 0), (250, 400, 300, 50))
        # Render the countdown text
        countdown_text = larger_font.render(f"Exiting in {countdown}...", True, (255, 255, 255))
        screen.blit(countdown_text, (250, 400))  # Position below the score text
        pygame.display.update()  # Update the screen
        pygame.time.wait(1000)  # Wait for 1 second

    # Exit the game
    pygame.quit()
    sys.exit()


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, ):
    screen.blit(enemyImg[i], (x, y))


def fire(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 5, y + 1))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 28:
        return True
    else:
        return False


def update_bullet(bullet_state):
    global bulletX, bulletY
    if bullet_state == "fire":
        bulletY -= bulletY_change
        if bulletY <= 0:
            bulletY = playerY
            bullet_state = "ready"
    return bulletX, bulletY, bullet_state


# Initial position of the background
background_y = 0
clock = pygame.time.Clock()
# Game Loop
running = True
game_started = False
while running:
    # Update background position
    background_y += 1  # Adjust the speed as needed
    if background_y >= height:
        background_y = 0

    # Draw the background image
    screen.blit(background_image, (0, background_y))
    screen.blit(background_image, (0, background_y - height))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Check if any key is pressed to start the game
        if event.type == pygame.KEYDOWN and not game_started:
            game_started = True

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -4

            if event.key == pygame.K_RIGHT:
                playerX_change = 4

            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_Sound = mixer.Sound('laser.wav')
                    bullet_Sound.play()
                    bulletX = playerX
                    fire(bulletX, bulletY)
            
            if event.key == pygame.K_ESCAPE:
                mixer.music.stop()
                game_over_Sound = mixer.Sound('gameover.wav')
                game_over_Sound.play()
                game_over_text()
                pygame.display.update() 
                pygame.time.wait(5000) 
                running = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Display "Press any key to start" message until a key is pressed
    if not game_started:
        start_message = font.render("Press any key to start", True, (255, 255, 255))
        screen.blit(start_message, (width // 2 - 150, height // 2))

        pygame.display.update()

    # If the game has started, continue with the rest of the game logic
    if game_started:
        # Checking the boundaries of spaceship
        playerX += playerX_change

        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736

        # Boundary for powerups
        if power_upsX <= 0:
            power_upsX = 0
        elif power_upsX >= 736:
            power_upsX = 736

        # Enemy movement
        for i in range(num_of_enemies):
            # Game Over
            if enemyY[i] > 480:
                for j in range(num_of_enemies):
                    enemyY[j] = 2000
                mixer.music.stop()
                game_over_Sound = mixer.Sound('gameover.wav')
                game_over_Sound.play()
                show_score(textX, textY)
                game_over_text()
                pygame.display.update()  # Refresh the screen to show the message
                pygame.time.wait(5000)  # Wait for 5 seconds
                running = False  # Stop the game loop
                break
            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = 3.7
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 710:
                enemyX_change[i] = -3.7
                enemyY[i] += enemyY_change[i]

            # Collision
            collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                explosion_Sound = mixer.Sound('explosion.wav')
                explosion_Sound.play()
                bulletY = 480
                bullet_state = "ready"
                score_value += 1
                enemyX[i] = random.randint(0, 710)
                enemyY[i] = random.randint(10, 150)

            enemy(enemyX[i], enemyY[i])

        # Bullet movement
        if bulletY <= 0:
            bulletY = 480
            bullet_state = "ready"

        if bullet_state == "fire":
            fire(bulletX, bulletY)
            bulletY -= bulletY_change

        # Update and draw power-ups
        for power_up in power_ups:
            power_up.update()
            screen.blit(power_up.image, (power_up.rect.x, power_up.rect.y))

            # Check collision with player using your isCollision method
            if playerX < power_up.rect.x < playerX + 64 and playerY < power_up.rect.y < playerY + 64:
                # Apply power-up effects
                power_ups.remove(power_up)

            # Check if it's time to spawn a new power-up
            current_time = pygame.time.get_ticks()
            if current_time - last_powerup_time > powerup_interval:
                if powerup_counter < max_powerups_per_interval:
                    # Choose a random power-up type from your defined types
                    powerup_type = random.choice(["speed_boost", "shield", "double_score"])
                    # Create the power-up with the chosen type
                    power_up = PowerUp(random.randint(0, width - 10), 0, powerup_type)
                    power_ups.append(power_up)
                    powerup_counter += 1
                else:
                    # Reset counter and generate a new interval for the next set of power-ups
                    powerup_counter = 0
                    last_powerup_time = current_time
                    powerup_interval = random.randint(4000, 12000)  # Set a new random interval

                    # Generate a new random maximum number of power-ups for the next interval
                    max_powerups_per_interval = random.randint(2, 3)  # Set a new random maximum

        # Spawn new power-ups randomly
        if random.randint(0, 100) == 1:
            power_up = PowerUp(random.randint(0, width - 10), 0, "dummy")
            power_ups.append(power_up)

        player(playerX, playerY)
        show_score(textX, textY)

        pygame.display.update()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
