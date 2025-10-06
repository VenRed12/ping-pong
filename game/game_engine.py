import pygame
from .paddle import Paddle
from .ball import Ball

# Game Engine

WHITE = (255, 255, 255)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        # Load sounds
        self.paddle_sound = pygame.mixer.Sound("sounds/paddle_hit.wav")
        self.wall_sound = pygame.mixer.Sound("sounds/wall_bounce.wav")
        self.score_sound = pygame.mixer.Sound("sounds/score.wav")

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        self.player_score = 0
        self.ai_score = 0
        self.font = pygame.font.SysFont("Arial", 30)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def update(self):
    # Move the ball first
        self.ball.move()

    # Collision check after moving the ball
        if self.ball.rect().colliderect(self.player.rect()) or self.ball.rect().colliderect(self.ai.rect()):
            self.ball.velocity_x *= -1  # reverse horizontal direction
            self.paddle_sound.play()  # <-- Play paddle hit sound

        # Optional: slightly adjust Y velocity based on where it hits the paddle
        # This makes the ball bounce at an angle
            if self.ball.rect().colliderect(self.player.rect()):
                offset = (self.ball.y + self.ball.height / 2) - (self.player.y + self.player.height / 2)
            else:  # AI paddle
                offset = (self.ball.y + self.ball.height / 2) - (self.ai.y + self.ai.height / 2)
            self.ball.velocity_y += offset * 0.05  # tweak the factor for realistic bounce

    # Check for scoring
        if self.ball.x <= 0:
            self.ai_score += 1
            self.score_sound.play()  # <-- Play score sound

            self.ball.reset()
        elif self.ball.x >= self.width:
            self.player_score += 1
            self.score_sound.play()  # <-- Play score sound

            self.ball.reset()

    # Move AI paddle
        self.ai.auto_track(self.ball, self.height)


    def render(self, screen):
        # Draw paddles and ball
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

        # Draw score
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width//4, 20))
        screen.blit(ai_text, (self.width * 3//4, 20))

    def check_game_over(self, screen):
        if hasattr(self, "winning_score"):
            target = self.winning_score
        else:
            target = 5  # default if not set yet

        if self.player_score >= target or self.ai_score >= target:
            winner = "Player Wins!" if self.player_score >= target else "AI Wins!"
            
            # Display winner
            screen.fill((0, 0, 0))
            text = self.font.render(winner, True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.width // 2, self.height // 2))
            screen.blit(text, text_rect)
            pygame.display.flip()
            pygame.time.delay(1500)  # short delay before showing replay menu

            # Show replay menu
            self.replay_menu(screen)


    def replay_menu(self, screen):
        screen.fill((0, 0, 0))
        menu_font = pygame.font.SysFont("Arial", 28)

        options = [
            "Press 3 for Best of 3",
            "Press 5 for Best of 5",
            "Press 7 for Best of 7",
            "Press ESC to Exit"
        ]

        for i, option in enumerate(options):
            text = menu_font.render(option, True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.width // 2, self.height // 2 - 60 + i * 40))
            screen.blit(text, text_rect)

        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_3:
                        self.winning_score = 2  # Best of 3 → first to 2 wins
                        waiting = False
                    elif event.key == pygame.K_5:
                        self.winning_score = 3  # Best of 5 → first to 3 wins
                        waiting = False
                    elif event.key == pygame.K_7:
                        self.winning_score = 4  # Best of 7 → first to 4 wins
                        waiting = False
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()
        
        # Reset scores and positions
        self.player_score = 0
        self.ai_score = 0
        self.ball.reset()
        self.player.y = self.height // 2 - self.paddle_height // 2
        self.ai.y = self.height // 2 - self.paddle_height // 2

