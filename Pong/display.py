import pygame, sys, random

class Block(pygame.sprite.Sprite):
    def __init__(self, path, x_pos, y_pos):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(center = (x_pos, y_pos))
       

class Player(Block):
    def __init__(self, path, x_pos, y_pos, speed):
        super().__init__(path, x_pos, y_pos)
        self.speed = speed
        self.movement = 0
    
    def screen_constrain(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height
        
    def update(self, ball_ground):
        self.rect.y += self.movement
        self.screen_constrain()

class Ball(Block):
    def __init__(self, path, x_pos, y_pos, speed_x, speed_y, paddle):
        super().__init__(path, x_pos, y_pos)
        self.speed_x = speed_x * random.choice([-1, 1])
        self.speed_y = speed_y * random.choice([-1, 1])
        self.paddle = paddle
        self.active = True
        self.score_time = 0
    
    def update(self):
        if self.active:
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y
            self.collision()
        else:
            self.restart_counter()

    def collision(self):
        if self.rect.top < 0 or self.rect.bottom > screen_height:
            pygame.mixer.Sound.play(pong_sound)
            self.speed_y *= -1
        
        if pygame.sprite.spritecollide(self, self.paddle, False):
            pygame.mixer.Sound.play(pong_sound)
            collision_paddle = pygame.sprite.spritecollide(self, self.paddle, False)[0].rect
            if abs(self.rect.right - collision_paddle.left) < 10 and self.speed_x > 0:
                self.speed_x *= -1
            if abs(self.rect.left - collision_paddle.right) < 10 and self.speed_x < 0:
                self.speed_x *= -1
            if abs(self.rect.top - collision_paddle.bottom) < 10 and self.speed_y < 0:
                self.rectf.top = collision_paddle.bottom
                self.speed_y *= -1
            if abs(self.rect.bottom - collision_paddle.top) < 10 and self.speed_y > 0:
                self.rect.bottom = collision_paddle.top
                self.speed_y *= -1
    def reset_ball(self):
        self.active = False
        self.speed_x *= random.choice([-1, 1])
        self.speed_y *= random.choice([-1, 1])
        self.score_time = pygame.time.get_ticks()
        self.rect.center = (screen_width / 2, screen_height / 2)
        
    def restart_counter(self):
        current_time = pygame.time.get_ticks()
        countdown_timer = 3
        
        if current_time - self.score_time <= 700:
            countdown_timer = 3
        if 700 < current_time - self.score_time <= 1400:
            countdown_timer = 2
        if 1400 < current_time - self.score_time <= 2100:
            countdown_timer = 1
        if current_time - self.score_time > 2100:
            self.active = True

        time_count = game_font.render(str(countdown_timer), True, (light_grey))
        time_count_rect = time_count.get_rect(center = (screen_width / 2, screen_height / 2 + 50))
        pygame.draw.rect(screen, bg_color, time_count_rect)
        screen.blit(time_count, time_count_rect)

class Opponent(Block):

    def __init__(self, path, x_pos, y_pos, speed):
        super().__init__(path, x_pos, y_pos)
        self.speed = speed
        

    def update(self, ball_group):
        if self.rect.top < ball_group.sprite.rect.y:
            self.rect.y += self.speed
        if self.rect.bottom > ball_group.sprite.rect.y:
            self.rect.y -= self.speed
        self.constrain()

    def constrain(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height

class GameManager:
    def __init__(self, ball_group, paddle_group):
        self.player_score = 0
        self.opponent_score = 0
        self.ball_group = ball_group
        self.paddle_group = paddle_group

    def run_game(self):
        self.paddle_group.draw(screen)
        self.ball_group.draw(screen)

        self.paddle_group.update(self.ball_group)
        self.ball_group.update()
        self.reset_ball()
        self.draw_score()

    def reset_ball(self):
        if self.ball_group.sprite.rect.right >= screen_width:
            self.opponent_score += 1
            self.ball_group.sprite.reset_ball()
        if self.ball_group.sprite.rect.left <= 0:
            self.player_score += 1
            self.ball_group.sprite.reset_ball()

    def draw_score(self):
        player_score = game_font.render(str(self.player_score), True, (light_grey))
        opponent_score = game_font.render(str(self.opponent_score), True, (light_grey))

        player_score_rect = player_score.get_rect(midleft = (screen_width / 2 + 40, screen_height / 2 ))
        opponent_score_rect = opponent_score.get_rect(midright = (screen_width / 2 - 40, screen_height / 2 ))
        
        screen.blit(player_score, player_score_rect)
        screen.blit(opponent_score, opponent_score_rect)
        

    

# def ball_animation():
#     global ball_speed_x, ball_speed_y, player_score, opponent_score, score_time
#     ball.x += ball_speed_x
#     ball.y += ball_speed_y

#     if ball.top <= 0 or ball.bottom >= screen_height:
#         pygame.mixer.Sound.play(pong_sound)
#         ball_speed_y *= -1

    
#     if ball.left <= 0:
#         player_score += 1  
#         score_time = pygame.time.get_ticks()
#     if ball.right >= screen_width:
#         opponent_score += 1 
#         score_time = pygame.time.get_ticks()   
#     if ball.colliderect(player) and ball_speed_x > 0:
#         pygame.mixer.Sound.play(pong_sound)
#         if abs(ball.right - player.left) < 10:
#             ball_speed_x *= -1
#         elif abs(ball.bottom - player.top) < 10 and ball_speed_y > 0:
#             ball_speed_y *= -1
#         elif abs(ball.top - player.bottom) < 10 and ball_speed_y < 0:
#             ball_speed_y *= -1
#     if ball.colliderect(opponent):
#         pygame.mixer.Sound.play(pong_sound)
#         if abs(ball.left - opponent.right) < 10:
#             ball_speed_x *= -1
#         elif abs(ball.bottom - opponent.top) < 10 and ball_speed_y > 0:
#             ball_speed_y *= -1
#         elif abs(ball.top - opponent.bottom) < 10 and ball_speed_y < 0:
#             ball_speed_y *= -1

# def player_animation():
#     player.y +=   player.movement
#     if player.top <= 0:
#         player.top = 0
#     if player.bottom >= screen_height:
#         player.bottom = screen_height

# def opponent_animation():
#     if opponent.top < ball.y:
#         opponent.top += opponent_speed
#     if opponent.bottom > ball.y:
#         opponent.bottom -= opponent_speed
#     if opponent.top <= 0:
#         opponent.top = 0
#     if opponent.bottom >= screen_height:
#         opponent.bottom = screen_height
    
# def ball_restart():
#     global ball_speed_x, ball_speed_y, score_time
#     current_time = pygame.time.get_ticks()
#     ball.center = (screen_width/2, screen_height/2)

#     if current_time - score_time < 700:
#         number_three = game_font.render("3", True, light_grey)
#         screen.blit(number_three, (screen_width/2 - 10, screen_height/2 + 20))
#     if 700 < current_time - score_time < 1400:
#         number_two = game_font.render("2", True, light_grey)
#         screen.blit(number_two, (screen_width/2 - 10, screen_height/2 + 20))
#     if 1400 < current_time - score_time < 2100:
#         number_one = game_font.render("1", True, light_grey)
#         screen.blit(number_one, (screen_width/2 - 10, screen_height/2 + 20))
    
#     if current_time - score_time < 2100:
#         ball_speed_x = 0
#         ball_speed_y = 0
#     else:
#         ball_speed_x = 7 * random.choice((1, -1))
#         ball_speed_y = 7 * random.choice((1, -1))
#         score_time = None
# #general setup    
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
clock = pygame.time.Clock()

# Set up the drawing window
screen_width = 1200
screen_height = 600
screen = pygame.display.set_mode([screen_width, screen_height])
pygame.display.set_caption('Pong')

# game objects
player = Player('Paddle.png', screen_width - 20, screen_height/2, 5)
opponent = Opponent('Paddle.png', 20, screen_height/2, 5)
paddle_group = pygame.sprite.Group()
paddle_group.add(player)
paddle_group.add(opponent)

ball = Ball('Ball.png', screen_width/2, screen_height/2, 4, 4, paddle_group)
ball_sprite = pygame.sprite.GroupSingle()
ball_sprite.add(ball)

game_manager = GameManager(ball_sprite, paddle_group)

# ball_speed_x = 8 * random.choice((1,-1))
# ball_speed_y = 8 * random.choice((1,-1))
#   player.movement = 0
# opponent_speed = 7
# player_score = 0
# opponent_score = 0
# score_time = True
game_font = pygame.font.Font('freesansbold.ttf', 32)
bg_color = ('grey12')
light_grey = (200, 200, 200)
pong_sound = pygame.mixer.Sound('bounce.mp3')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.movement -= player.speed
            if event.key == pygame.K_DOWN:
                player.movement += player.speed
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                player.movement += player.speed
            if event.key == pygame.K_DOWN:
                player.movement -= player.speed

        
            

    
    # animate
    # ball_animation()
    # player_animation()
    # opponent_animation()
   

    # Draw rectangles
    screen.fill(bg_color)
    

    # pygame.draw.rect(screen, light_grey, player)
    # pygame.draw.rect(screen, light_grey, opponent)
    # pygame.draw.ellipse(screen, light_grey, ball)
    pygame.draw.aaline(screen, light_grey, (screen_width/2, 0), (screen_width/2, screen_height))
    # if score_time:
    #     ball_restart()
    # Draw text
    # player_text = game_font.render(f'{player_score}', True, light_grey)
    # screen.blit(player_text, [650, 300])
    # opponent_text = game_font.render(f'{opponent_score}', True, light_grey)
    # screen.blit(opponent_text, [535, 300])
    game_manager.run_game()
    # Draw on the screen surface
    pygame.display.flip()
    clock.tick(60)