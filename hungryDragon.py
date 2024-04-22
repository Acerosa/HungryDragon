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
playerLives = PLAYER_STARTING_LIVES
coinVelocity = COIN_STARTING_VELOCITY

#Set colors
GREEN = (0, 255, 0)
DARKGREEN = (10, 50, 10)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

#Set fonts
font = pygame.font.Font('Hungry_Dragon_assets/AttackGraffiti.ttf', 32)

#Set text
scoreText = font.render("Score: " + str(score), True, GREEN, DARKGREEN)
scoreRect = scoreText.get_rect()
scoreRect.topleft = (10, 10)

titleText = font.render("Hungry dragon", True, GREEN, WHITE)
titleRect = titleText.get_rect()
titleRect.centerx = WINDOW_WIDTH // 2
titleRect.y = 10

livesText = font.render("Lives: " + str(playerLives), True, GREEN, DARKGREEN)
livesRect = livesText.get_rect()
livesRect.topright = (WINDOW_WIDTH - 10, 10)

gameOverText = font.render("GAMEOVER", True, GREEN, DARKGREEN)
gameOverRect = gameOverText.get_rect()
gameOverRect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

continueText = font.render("Press a key to play again", True, GREEN, DARKGREEN)
continueRect = continueText.get_rect()
continueRect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 32)


#Set sounds and music
coinSound = pygame.mixer.Sound("Hungry_Dragon_assets/coin_sound.wav")
missSound = pygame.mixer.Sound("Hungry_Dragon_assets/miss_sound.wav")
missSound.set_volume(.1)
pygame.mixer.music.load("Hungry_Dragon_assets/ftd_background_music.wav")

#Set images
playerImage = pygame.image.load("Hungry_Dragon_assets/dragon_right.png")
playerRect = playerImage.get_rect()
playerRect.left = 32
playerRect.centery = WINDOW_HEIGHT // 2

coinImage = pygame.image.load("Hungry_Dragon_assets/coin.png")
coinRect = coinImage.get_rect()
coinRect.x = WINDOW_WIDTH + BUFFER_DISTANCE
coinRect.y = random.randint(64, WINDOW_HEIGHT - 32)

# Add levels
LEVELS = [(10, 10), (15, 12), (20, 15)]  # Format: (COIN_VELOCITY, COIN_ACCELERATION)
currentLevel = 0

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
    if keys[pygame.K_UP] and playerRect.top > 64:
        playerRect.y -= PLAYER_VELOCITY  # Move the dragon up by PLAYER_VELOCITY units

    # Check if the down arrow key is pressed and the dragon's bottom position is below the bottom boundary
    if keys[pygame.K_DOWN] and playerRect.bottom < WINDOW_HEIGHT:
        playerRect.y += PLAYER_VELOCITY  # Move the dragon down by PLAYER_VELOCITY units

    return True  # Return True to indicate that the function executed successfully


def resetCoin():
    # Reset the  x-position of the coin outside the right edge of the window
    coinRect.x = WINDOW_WIDTH + BUFFER_DISTANCE
    # Set the y-position of the coin to a random value within the window area
    coinRect.y = random.randint(64, WINDOW_HEIGHT - 32)


def updateGame():
    # Grab global variables to update them in the function
    global score, playerLives, coinVelocity, currentLevel

    # Check if the coin has reached the left edge of the window
    if coinRect.x < 0:
        # Decrease player's lives count when the coin is missed
        playerLives -= 1
        # Play the miss sound effect
        missSound.play()
        # Reset the coin to a new random position
        resetCoin()
    else:
        # Move the coin towards the left side of the window
        coinRect.x -= LEVELS[currentLevel][0]

    # Check if there's collision between the player and the coin
    if playerRect.colliderect(coinRect):
        # Increase player's score when the coin is caught
        score += 1
        # Play the coin collection sound effect
        coinSound.play()
        # Increase the coin velocity to increase difficulty
        coinVelocity += LEVELS[currentLevel][1]
        # Reset the coin to a new random position
        resetCoin()
    if score == 10 and currentLevel < len(LEVELS) - 1:
        currentLevel += 1

def showGameOver():
    # Blit the "GAME OVER" text to the screen
    display_surface.blit(gameOverText, gameOverRect)
    # Blit the "Press any key to play again" to the screen
    display_surface.blit(continueText, continueRect)
    # Update to show the game over screen
    pygame.display.update()


def gameReseter():
    # Grabbing global variables to use them in the function
    global score, playerLives, coinVelocity, currentLevel

    # Reset the game variables to their initial values
    score = 0  # Reset the player's score to zero
    playerLives = PLAYER_STARTING_LIVES  # Resting the player's lives
    playerRect.y = WINDOW_HEIGHT // 2  # Resting the player's vertical position
    coinVelocity = COIN_STARTING_VELOCITY  # Resting the coin velocity
    currentLevel = 0 # Resting the current level
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

# Define game states
MENU = 0
PLAYING = 1
GAME_OVER = 2
gameState = PLAYING


# Main game loop
pygame.mixer.music.play(-1, 0.0)
running = True
while running:
    # Check for user input
    running = moveDragon()  # update game accordingly
    if gameState == PLAYING:  # If the game state is playing
        updateGame()  # update the game accordingly
        if playerLives == 0:  # If player has no lives left
            gameState = GAME_OVER  # Set game state to game over
    elif gameState == GAME_OVER:  # If the game state is game over
        showGameOver()  # Display the game over
        if not gameOverHandler():  # If the player chooses to quit
            running = False  # Exit the game loop

    # Render game elements on the screen
    scoreText = font.render("Score: " + str(score), True, GREEN, DARKGREEN)  # score text
    livesText = font.render("Lives: " + str(playerLives), True, GREEN, DARKGREEN)  # lives text

    # Check player lives for game over
    if playerLives == 0:
        gameOverHandler()  # Display game over
        # Handle game over to continue the game
        if not gameOverHandler():
            running = False  # Exit the game loop if the player wants quit

    # Fill the background
    display_surface.fill(BLACK)
    # Blit game elements
    display_surface.blit(scoreText, scoreRect)  # Render score text
    display_surface.blit(titleText, titleRect)  # Render title text
    display_surface.blit(livesText, livesRect)  # Render lives text
    pygame.draw.line(display_surface, WHITE, (0, 64), (WINDOW_WIDTH, 64), 2)  # Draw a line
    display_surface.blit(playerImage, playerRect)  # Render the player
    display_surface.blit(coinImage, coinRect)  # Render the coin

    pygame.display.update()  # Update the display
    clock.tick(FPS)  # Cap the frame rate

# End the game
pygame.quit()  # Quit the Pygame close and window
