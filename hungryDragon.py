import pygame, random

#Initialize pygame
pygame.init()

#Set display surface
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 400
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Hungry dragon")

#Set FPS and clock
FPS = 60
clock = pygame.time.Clock()

#Set game values
PLAYER_STARTING_LIVES = 5
PLAYER_VELOCITY = 10
COIN_STARTING_VELOCITY = 10
COIN_ACCELERATION = .5
BUFFER_DISTANCE = 100

score = 0
player_lives = PLAYER_STARTING_LIVES
coin_velocity = COIN_STARTING_VELOCITY

#Set colors
GREEN = (0, 255, 0)
DARKGREEN = (10, 50, 10)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

#Set fonts
font = pygame.font.Font('Hungry _Dragon_assets/AttackGraffiti.ttf', 32)

#Set text
score_text = font.render("Score: " + str(score), True, GREEN, DARKGREEN)
score_rect = score_text.get_rect()
score_rect.topleft = (10, 10)

title_text = font.render("Hungry dragon", True, GREEN, WHITE)
title_rect = title_text.get_rect()
title_rect.centerx = WINDOW_WIDTH//2
title_rect.y = 10

lives_text = font.render("Lives: " + str(player_lives), True, GREEN, DARKGREEN)
lives_rect = lives_text.get_rect()
lives_rect.topright = (WINDOW_WIDTH - 10, 10)

game_over_text = font.render("GAMEOVER", True, GREEN, DARKGREEN)
game_over_rect = game_over_text.get_rect()
game_over_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

continue_text = font.render("Press a key to play again", True, GREEN, DARKGREEN)
continue_rect = continue_text.get_rect()
continue_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 32)


#Set sounds and music
coin_sound = pygame.mixer.Sound("Hungry _Dragon_assets/coin_sound.wav")
miss_sound = pygame.mixer.Sound("Hungry _Dragon_assets/miss_sound.wav")
miss_sound.set_volume(.1)
pygame.mixer.music.load("Hungry _Dragon_assets/ftd_background_music.wav")

#Set images
player_image = pygame.image.load("Hungry _Dragon_assets/dragon_right.png")
player_rect = player_image.get_rect()
player_rect.left = 32
player_rect.centery = WINDOW_HEIGHT//2

coin_image = pygame.image.load("Hungry _Dragon_assets/coin.png")
coin_rect = coin_image.get_rect()
coin_rect.x = WINDOW_WIDTH + BUFFER_DISTANCE
coin_rect.y = random.randint(64, WINDOW_HEIGHT - 32)


# Game functionality

# Define functions for better organization
def moveDragon():
    # Check for any events (such as quitting the game)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False  # If the user quits, return False to exit the game loop

    # Get the state of all keyboard keys
    keys = pygame.key.get_pressed()

    # Check if the up arrow key is pressed and the dragon's top position is above the top boundary
    if keys[pygame.K_UP] and player_rect.top > 64:
        player_rect.y -= PLAYER_VELOCITY  # Move the dragon up by PLAYER_VELOCITY units

    # Check if the down arrow key is pressed and the dragon's bottom position is below the bottom boundary
    if keys[pygame.K_DOWN] and player_rect.bottom < WINDOW_HEIGHT:
        player_rect.y += PLAYER_VELOCITY  # Move the dragon down by PLAYER_VELOCITY units

    return True  # Return True to indicate that the function executed successfully


def resetCoin():
    # Reset the  x-position of the coin outside the right edge of the window
    coin_rect.x = WINDOW_WIDTH + BUFFER_DISTANCE
    # Set the y-position of the coin to a random value within the window area
    coin_rect.y = random.randint(64, WINDOW_HEIGHT - 32)


def updateGame():
    # Grab global variables to update them in the function
    global score, player_lives, coin_velocity

    # Check if the coin has reached the left edge of the window
    if coin_rect.x < 0:
        # Decrease player's lives count when the coin is missed
        player_lives -= 1
        # Play the miss sound effect
        miss_sound.play()
        # Reset the coin to a new random position
        resetCoin()
    else:
        # Move the coin towards the left side of the window
        coin_rect.x -= coin_velocity

    # Check if there's collision between the player and the coin
    if player_rect.colliderect(coin_rect):
        # Increase player's score when the coin is caught
        score += 1
        # Play the coin collection sound effect
        coin_sound.play()
        # Increase the coin velocity to increase difficulty
        coin_velocity += COIN_ACCELERATION
        # Reset the coin to a new random position
        resetCoin()

def showGameOver():
    # Blit the "GAME OVER" text to the screen
    display_surface.blit(game_over_text, game_over_rect)
    # Blit the "Press any key to play again" to the screen
    display_surface.blit(continue_text, continue_rect)
    # Update to show the game over screen
    pygame.display.update()


def gameReseter():
    # Grabbing global variables to use them in the function
    global score, player_lives, coin_velocity

    # Reset the game variables to their initial values
    score = 0  # Reset the player's score to zero
    player_lives = PLAYER_STARTING_LIVES  # Reset the player's lives to the original value
    player_rect.y = WINDOW_HEIGHT // 2  # Reset the player's vertical position to the center of the window
    coin_velocity = COIN_STARTING_VELOCITY  # Reset the coin velocity to the original value

    # Restart the background music
    pygame.mixer.music.play(-1, 0.0)

def gameOverHandler():
    # Stop the background music
    pygame.mixer.music.stop()
    # Pausing the game
    is_paused = True
    # Continue loop while game is paused
    while is_paused:
        # Check for events
        for event in pygame.event.get():
            # If any key is pressed, reset the game
            if event.type == pygame.KEYDOWN:
                gameReseter()
                is_paused = False  # Unpause game
            # If the user wants to quit return False to exit the game loop
            if event.type == pygame.QUIT:
                return False
    # return True to continue the game loop
    return True


# Main game loop
pygame.mixer.music.play(-1, 0.0)
running = True
while running:
    # Check for user input
    running = moveDragon()  # update game accordingly
    updateGame()  # update the game accordingly

    # Render game elements on the screen
    score_text = font.render("Score: " + str(score), True, GREEN, DARKGREEN)  # score text
    lives_text = font.render("Lives: " + str(player_lives), True, GREEN, DARKGREEN)  # lives text

    # Check player lives for game over
    if player_lives == 0:
        gameOverHandler()  # Display game over
        # Handle game over to continue the game
        if not gameOverHandler():
            running = False  # Exit the game loop if the player wants quit

    # Fill the background
    display_surface.fill(BLACK)
    # Blit game elements
    display_surface.blit(score_text, score_rect)  # Render score text
    display_surface.blit(title_text, title_rect)  # Render title text
    display_surface.blit(lives_text, lives_rect)  # Render lives text
    pygame.draw.line(display_surface, WHITE, (0, 64), (WINDOW_WIDTH, 64), 2)  # Draw a line
    display_surface.blit(player_image, player_rect)  # Render the player
    display_surface.blit(coin_image, coin_rect)  # Render the coin

    pygame.display.update()  # Update the display
    clock.tick(FPS)  # Cap the frame rate

# End the game
pygame.quit()  # Quit the Pygame close and window
