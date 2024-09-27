import pygame
import random
pygame.init()
pygame.mixer.init()  

# Constants
WIDTH, HEIGHT = 800, 500
GROUND_HEIGHT = 50
OBSTACLE_SPACING = 400  
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60

#game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino Game")

# assets
dino_img = pygame.image.load("img/Dino.png")

#multiple obstacle images
obstacle_imgs = [pygame.image.load("img/obstacle1.png"),
                 pygame.image.load("img/obstacle2.png"),
                 pygame.image.load("img/obstacle3.png")]

ground_img = pygame.image.load("img/ground.png")


background_img = pygame.image.load("img/background.jpg")
background_img = pygame.transform.scale(background_img, (WIDTH * 2, HEIGHT))

ground_img = pygame.transform.scale(ground_img, (WIDTH, GROUND_HEIGHT))

font = pygame.font.Font(None, 36)

#  background music
pygame.mixer.music.load("music/background_music.mp3")  
pygame.mixer.music.play(-1)  

# jump sound effect
jump_sound = pygame.mixer.Sound("music/jump_sound.wav")  

# Ground variables
ground_x = 0
ground_x_speed = -5

# Background variables
background_x = 0
background_x_speed = -1  

# Game variables
dino_x = 50
dino_y = HEIGHT - GROUND_HEIGHT - dino_img.get_height()
dino_y_speed = 0
jump_velocity = -24 
gravity = 1
obstacles = []
score = 0
highest_score = 0

# Initial obstacles
obstacle_x = WIDTH
while obstacle_x < WIDTH + OBSTACLE_SPACING:
    obstacle_img = random.choice(obstacle_imgs)  
    obstacle = {
        "img": obstacle_img,
        "x": obstacle_x,
        "y": HEIGHT - GROUND_HEIGHT - obstacle_img.get_height(),
        "speed": -5
    }
    obstacles.append(obstacle)
    obstacle_x += OBSTACLE_SPACING

def create_obstacle():
    obstacle_img = random.choice(obstacle_imgs)  
    obstacle = {
        "img": obstacle_img,
        "x": WIDTH,
        "y": HEIGHT - GROUND_HEIGHT - obstacle_img.get_height(),
        "speed": -5
    }
    obstacles.append(obstacle)

running = True

game_over = False
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over and not is_jumping:
                dino_y_speed = jump_velocity
                is_jumping = True
                jump_sound.play()  

    if not game_over:
        dino_y += dino_y_speed
        dino_y_speed += gravity

        if dino_y >= HEIGHT - GROUND_HEIGHT - dino_img.get_height():
            dino_y = HEIGHT - GROUND_HEIGHT - dino_img.get_height()
            dino_y_speed = 0
            is_jumping = False

        for obstacle in obstacles:
            obstacle["x"] += obstacle["speed"]
            if obstacle["x"] < -obstacle["img"].get_width():
                obstacles.remove(obstacle)
                create_obstacle()
                score += 1
                if score > highest_score:
                    highest_score = score

        ground_x += ground_x_speed
        if ground_x < -ground_img.get_width():
            ground_x = 0

        background_x += background_x_speed
        if background_x < -WIDTH:
            background_x = 0

        if not is_jumping:
            dino_rect = pygame.Rect(dino_x, dino_y, dino_img.get_width(), dino_img.get_height())
            for obstacle in obstacles:
                obstacle_rect = pygame.Rect(obstacle["x"], obstacle["y"], obstacle["img"].get_width(), obstacle["img"].get_height())
                if dino_rect.colliderect(obstacle_rect):
                    game_over = True

    screen.fill(WHITE)
    screen.blit(background_img, (background_x, 0))  # Set the background image.
    screen.blit(ground_img, (ground_x, HEIGHT - GROUND_HEIGHT))
    screen.blit(ground_img, (ground_x + ground_img.get_width(), HEIGHT - GROUND_HEIGHT))
    screen.blit(dino_img, (dino_x, dino_y))
    for obstacle in obstacles:
        screen.blit(obstacle["img"], (obstacle["x"], obstacle["y"]))
    pygame.draw.rect(screen, BLACK, (0, HEIGHT - GROUND_HEIGHT, WIDTH, GROUND_HEIGHT))

    # Display score
    score_text = font.render(f"Score: {score}", True, BLACK)
    highest_score_text = font.render(f"Highest Score: {highest_score}", True, BLACK)
    screen.blit(score_text, (10, 10))
    screen.blit(highest_score_text, (10, 50))

    if game_over:
        game_over_text = font.render("Game Over! Press R to restart", True, BLACK)
        screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2 - 50))

    pygame.display.update()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_r]:
        if game_over:
            game_over = False
            dino_y = HEIGHT - GROUND_HEIGHT - dino_img.get_height()
            dino_y_speed = 0
            obstacles = []
            for i in range(3):
                create_obstacle() 
            score = 0

    clock.tick(FPS)

pygame.quit()