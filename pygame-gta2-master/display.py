import pygame, sys

class Car(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.car_image = pygame.image.load("Audi.png")
        self.car_image = pygame.transform.scale(self.car_image, (175, 175))
        self.image = self.car_image
        self.rect = self.image.get_rect(center = (500, 200))
        self.angle = 0
        self.rotation_speed = 1.8
        self.direction = 0
        self.forward = pygame.math.Vector2(0, -1)
        self.active = False
    
    def set_rotation(self):
        if self.direction == 1:
            self.angle += self.rotation_speed
        if self.direction == -1:
            self.angle -= self.rotation_speed

        self.image = pygame.transform.rotozoom(self.car_image, self.angle, 0.25)
        self.rect = self.image.get_rect(center = (self.rect.center))

    def get_rotation(self):
        if self.direction == 1:
            self.forward.rotate_ip(self.rotation_speed)
        if self.direction == -1:
            self.forward.rotate_ip(-self.rotation_speed)
    
    def move(self):
        if self.active:
            self.rect.center += self.forward * 5

    def update(self):
        self.set_rotation()
        self.get_rotation()
        self.move()
        





pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Car")
clock = pygame.time.Clock()
bg_game = pygame.image.load("Track.png")
bg_game = pygame.transform.scale(bg_game, (screen_width, screen_height))

#create Object
car = Car()
cars = pygame.sprite.GroupSingle()
cars.add(car)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                car.direction = -1
            if event.key == pygame.K_d:
                car.direction = 1
            if event.key == pygame.K_w:
                car.active = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d:
                car.direction = 0
            if event.key == pygame.K_w:
                car.active = False

    screen.blit(bg_game, (0, 0))
    cars.draw(screen)
    cars.update()
    pygame.display.update()
    clock.tick(60)