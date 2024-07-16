import pygame
import random

# Initialize Pygame
pygame.init()

# Constants for window dimensions
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
WIN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Enhanced Pong Game")

# Frame rate
FPS = 60

# Colors
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_RED = (255, 0, 0)

# Paddle dimensions
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_RADIUS = 8

# Font for score display
SCORE_FONT = pygame.font.SysFont("comicsans", 50)
TARGET_SCORE = 10

# Sound effect
BOUNCE_SOUND = pygame.mixer.Sound("sound/bounce.mp3")
SCORE_SOUND = pygame.mixer.Sound("sound/score.mp3")

class Paddle:
    VELOCITY = 5

    def __init__(self, x, y, width, height, color):
        self.x = self.start_x = x
        self.y = self.start_y = y
        self.width = width
        self.height = height
        self.color = color

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))

    def move(self, direction=True):
        if direction:
            self.y -= self.VELOCITY
        else:
            self.y += self.VELOCITY

    def reset_position(self):
        self.x = self.start_x
        self.y = self.start_y

class Ball:
    MAX_VELOCITY = 6

    def __init__(self, x, y, radius, color):
        self.x = self.start_x = x
        self.y = self.start_y = y
        self.radius = radius
        self.color = color
        self.x_velocity = self.MAX_VELOCITY
        self.y_velocity = 0

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_velocity
        self.y += self.y_velocity

    def reset_position(self):
        self.x = self.start_x
        self.y = self.start_y
        self.y_velocity = 0
        self.x_velocity *= -1

def draw(win, paddles, ball, left_score, right_score):
    win.fill(COLOR_BLACK)

    left_score_text = SCORE_FONT.render(f"{left_score}", True, COLOR_WHITE)
    right_score_text = SCORE_FONT.render(f"{right_score}", True, COLOR_WHITE)
    win.blit(left_score_text, (WINDOW_WIDTH//4 - left_score_text.get_width()//2, 20))
    win.blit(right_score_text, (WINDOW_WIDTH * 3/4 - right_score_text.get_width()//2, 20))

    for paddle in paddles:
        paddle.draw(win)

    for i in range(10, WINDOW_HEIGHT, WINDOW_HEIGHT//20):
        if i % 2 == 1:
            continue
        pygame.draw.rect(win, COLOR_WHITE, (WINDOW_WIDTH//2 - 5, i, 10, WINDOW_HEIGHT//20))

    ball.draw(win)
    pygame.display.update()

def handle_ball_collision(ball, left_paddle, right_paddle):
    if ball.y + ball.radius >= WINDOW_HEIGHT or ball.y - ball.radius <= 0:
        ball.y_velocity *= -1
        BOUNCE_SOUND.play()

    if ball.x_velocity < 0:
        if left_paddle.y <= ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_velocity *= -1
                middle_y = left_paddle.y + left_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (left_paddle.height / 2) / ball.MAX_VELOCITY
                ball.y_velocity = -1 * (difference_in_y / reduction_factor)
                BOUNCE_SOUND.play()
    else:
        if right_paddle.y <= ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_velocity *= -1
                middle_y = right_paddle.y + right_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (right_paddle.height / 2) / ball.MAX_VELOCITY
                ball.y_velocity = -1 * (difference_in_y / reduction_factor)
                BOUNCE_SOUND.play()

def handle_paddle_movement(keys, left_paddle, right_paddle):
    if keys[pygame.K_w] and left_paddle.y - left_paddle.VELOCITY >= 0:
        left_paddle.move(direction=True)
    if keys[pygame.K_s] and left_paddle.y + left_paddle.VELOCITY + left_paddle.height <= WINDOW_HEIGHT:
        left_paddle.move(direction=False)

    if keys[pygame.K_UP] and right_paddle.y - right_paddle.VELOCITY >= 0:
        right_paddle.move(direction=True)
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.VELOCITY + right_paddle.height <= WINDOW_HEIGHT:
        right_paddle.move(direction=False)

def main():
    running = True
    clock = pygame.time.Clock()

    left_paddle = Paddle(20, WINDOW_HEIGHT//2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT, COLOR_BLUE)
    right_paddle = Paddle(WINDOW_WIDTH - 40, WINDOW_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT, COLOR_RED)
    ball = Ball(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, BALL_RADIUS, COLOR_WHITE)

    left_score = 0
    right_score = 0

    while running:
        clock.tick(FPS)
        draw(WIN, [left_paddle, right_paddle], ball, left_score, right_score)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, left_paddle, right_paddle)

        ball.move()
        handle_ball_collision(ball, left_paddle, right_paddle)

        if ball.x < 0:
            right_score += 1
            ball.reset_position()
            SCORE_SOUND.play()
        elif ball.x > WINDOW_WIDTH:
            left_score += 1
            ball.reset_position()
            SCORE_SOUND.play()

        if left_score >= TARGET_SCORE:
            win_text = "Left Player Wins!"
            text = SCORE_FONT.render(win_text, True, COLOR_WHITE)
            WIN.blit(text, (WINDOW_WIDTH//2 - text.get_width() // 2, WINDOW_HEIGHT//2 - text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(3000)
            left_score = 0
            right_score = 0
        elif right_score >= TARGET_SCORE:
            win_text = "Right Player Wins!"
            text = SCORE_FONT.render(win_text, True, COLOR_WHITE)
            WIN.blit(text, (WINDOW_WIDTH//2 - text.get_width() // 2, WINDOW_HEIGHT//2 - text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(3000)
            left_score = 0
            right_score = 0

    pygame.quit()

if __name__ == "__main__":
    main()
