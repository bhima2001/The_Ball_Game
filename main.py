import pygame
import sys
import random


pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
pygame.display.set_caption("The Ball Game")

game_font = pygame.font.Font("assets/PressStart2P-Regular.ttf", 24)

# Classes


class Ball(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.running_sprites = []

        self.running_sprites.append(pygame.transform.scale(
            pygame.image.load("assets/gameball.png"), (60, 70)))


        self.x_pos = x_pos
        self.y_pos = y_pos
        self.current_image = 0
        self.image = self.running_sprites[self.current_image]
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.velocity = 50
        self.gravity = 4.5

    def jump(self):
        jump_sfx.play()
        if self.rect.centery >= 360:
            while self.rect.centery - self.velocity > 40:
                self.rect.centery -= 1


    def apply_gravity(self):
        if self.rect.centery <= 360:
            self.rect.centery += self.gravity

    def update(self):
        self.animate()
        self.apply_gravity()

    def animate(self):
        self.current_image += 0.05
        if self.current_image >= 2:
            self.current_image = 0


class Spike(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.sprites = []
        for i in range(1, 7):
            current_sprite = pygame.transform.scale(
                pygame.image.load(f"assets/spikes/spike{i}.png"), (100, 100))
            self.sprites.append(current_sprite)
        self.image = random.choice(self.sprites)
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def update(self):
        self.x_pos -= game_speed
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))



# Variables


game_speed = 5
player_score = 0
game_over = False
obstacle_timer = 0
obstacle_spawn = False
obstacle_cooldown = 1000

# Surfaces

ground = pygame.image.load("assets/ground.png")
ground = pygame.transform.scale(ground, (1280, 20))
ground_x = 0
ground_rect = ground.get_rect(center=(640, 400))

# Groups

obstacle_group = pygame.sprite.Group()
ball_group = pygame.sprite.GroupSingle()

# Objects
BALL = Ball(50, 360)
ball_group.add(BALL)

#Jump SFX
jump_sfx = pygame.mixer.Sound("assets/sfx/jump.mp3")

# Functions
def end_game():
    global player_score, game_speed
    game_over_text = game_font.render("Game Over!", True, "black")
    game_over_rect = game_over_text.get_rect(center=(640, 300))
    score_text = game_font.render(f"Score: {int(player_score)}", True, "black")
    score_rect = score_text.get_rect(center=(640, 340))
    try_again = game_font.render("Press Spacebar to try again", True, "black")
    try_again_rect=try_again.get_rect(center=(640,380))
    screen.blit(game_over_text, game_over_rect)
    screen.blit(score_text, score_rect)
    screen.blit(try_again,try_again_rect)
    game_speed = 5
    obstacle_group.empty()


while True:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                BALL.jump()
                if game_over:
                    game_over = False
                    game_speed = 5
                    player_score = 0

    screen.fill("white")

    # Collisions
    if pygame.sprite.spritecollide(ball_group.sprite, obstacle_group, False):
        game_over = True
    if game_over:
        end_game()

    if not game_over:
        game_speed += 0.0025

        if pygame.time.get_ticks() - obstacle_timer >= obstacle_cooldown:
            obstacle_spawn = True

        if obstacle_spawn:
            new_obstacle = Spike(1280, 340)
            obstacle_group.add(new_obstacle)
            obstacle_timer = pygame.time.get_ticks()
            obstacle_spawn = False

        player_score += 0.1
        player_score_surface = game_font.render(
            str(int(player_score)), True, ("black"))
        screen.blit(player_score_surface, (1150, 10))


        ball_group.update()
        ball_group.draw(screen)

        obstacle_group.update()
        obstacle_group.draw(screen)

        ground_x -= game_speed

        screen.blit(ground, (ground_x, 375))
        screen.blit(ground, (ground_x + 1280, 375))

        if ground_x <= -1280:
            ground_x = 0

    clock.tick(120)
    pygame.display.update()
