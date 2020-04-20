import pygame,random
from pygame.locals import *
#O CALCULO DO SCORE TA MEIO ERRADO EU ACHO Q TA ATRASADO

SCREEN_SIZE = (400,700)
SPEED = 10
GRAVITY = 1
GAME_SPEED = 10
GROUND_SIZE = (2*SCREEN_SIZE[0],100)
BACKGROUND_SIZE = (2*SCREEN_SIZE[0],SCREEN_SIZE[1])
PIPE_SIZE = (80, 700)
PIPE_GAP = 100
GAP_BETWEEN_PIPES = SCREEN_SIZE[0]

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.speed = SPEED

        self.images =  [pygame.image.load('bluebird-upflap.png').convert_alpha(),
                        pygame.image.load('bluebird-midflap.png').convert_alpha(),
                        pygame.image.load('bluebird-downflap.png').convert_alpha(),
                        pygame.image.load('bluebird-midflap.png').convert_alpha()]

        self.current_image = 0

        self.image = pygame.image.load('bluebird-upflap.png').convert_alpha()

        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = int((SCREEN_SIZE[0])/2)
        self.rect[1] = int((SCREEN_SIZE[1])/2)

    def update(self):
        self.current_image = (self.current_image + 1) % 4
        self.image = self.images[self.current_image]

        self.speed += GRAVITY
        #UPDATE HEIGHT
        self.rect[1] += self.speed

    def bump(self):
        self.speed = -SPEED

class Ground(pygame.sprite.Sprite):
    def __init__(self,xpos):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('base.png').convert_alpha()
        self.image = pygame.transform.scale(self.image,GROUND_SIZE)

        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = SCREEN_SIZE[1] - GROUND_SIZE[1]

    def update(self):
        self.rect[0] -= GAME_SPEED

class Background(pygame.sprite.Sprite):
    def __init__(self,xpos):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('background-day.png')
        self.image = pygame.transform.scale(self.image,BACKGROUND_SIZE)

        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = 0

    def update(self):
        self.rect[0] -= int(GAME_SPEED/3)

class Pipe(pygame.sprite.Sprite):
    def __init__(self,inverted, xpos,ysize):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('pipe-red.png').convert_alpha()
        self.image = pygame.transform.scale(self.image,PIPE_SIZE)
        self.rect = self.image.get_rect()
        self.rect[0] = xpos

        if inverted:
            self.image = pygame.transform.flip(self.image,False,True)
            self.rect[1] = -(self.rect[3] - ysize)
        else:
            self.rect[1] = SCREEN_SIZE[1] - ysize

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect[0] -= GAME_SPEED




def is_off_screen(sprite):
    return sprite.rect[0] < -(sprite.rect[2])

def gap_between_pipes(sprite):
    return SCREEN_SIZE[0] - sprite.rect[0] >= GAP_BETWEEN_PIPES

def get_random_pipes(xpos):
    size = random.randint(100,300)
    pipe = Pipe(False,xpos,size)
    pipe_inverted = Pipe(True,xpos,SCREEN_SIZE[1] - size - PIPE_GAP)
    return (pipe,pipe_inverted)

#main()
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)

#BACKGROUND = pygame.image.load('background-day.png')
#BACKGROUND = pygame.transform.scale(BACKGROUND,SCREEN_SIZE)

bird_group = pygame.sprite.Group()
bird = Bird()
bird_group.add(bird)

ground_group = pygame.sprite.Group()
for i in range(2):
    ground = Ground(GROUND_SIZE[0] * i)
    ground_group.add(ground)

background_group = pygame.sprite.Group()
for i in range(2):
    background = Background(BACKGROUND_SIZE[0] * i)
    background_group.add(background)

pipe_group = pygame.sprite.Group()
for i in range(3):
    if i == 0:
        pipes = get_random_pipes(SCREEN_SIZE[0]+100)
    else:
        pipes = get_random_pipes(GAP_BETWEEN_PIPES * i + SCREEN_SIZE[0]+100)
    pipe_group.add(pipes[0])
    pipe_group.add(pipes[1])

clock = pygame.time.Clock()

font = pygame.font.Font('freesansbold.ttf', 18)
score = 0

game_over = False
while not game_over:
    clock.tick(30)

    #EVENTS
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == KEYDOWN:
            if event.key == K_q:
                pygame.quit()
                exit()
            if event.key == K_SPACE:
                bird.bump()

    #screen.blit(BACKGROUND,(0,0))
    if is_off_screen(background_group.sprites()[0]):
        background_group.remove(background_group.sprites()[0])
        new_background = Background(BACKGROUND_SIZE[0] - 20)
        background_group.add(new_background)

    if is_off_screen(ground_group.sprites()[0]):
        ground_group.remove(ground_group.sprites()[0])
        new_ground = Ground(GROUND_SIZE[0] - 20)
        ground_group.add(new_ground)

    if gap_between_pipes(pipe_group.sprites()[2]):
        pipe_group.remove(pipe_group.sprites()[0])
        pipe_group.remove(pipe_group.sprites()[0])

        pipes = get_random_pipes(GAP_BETWEEN_PIPES * 2)
        pipe_group.add(pipes[0])
        pipe_group.add(pipes[1])
        score += 1

    background_group.update()
    bird_group.update()
    ground_group.update()
    pipe_group.update()

    background_group.draw(screen)
    bird_group.draw(screen)
    pipe_group.draw(screen)
    ground_group.draw(screen)

    # SCORE
    score_font = font.render('Score: %s' % (score), True, (0, 0, 0))
    score_rect = score_font.get_rect()
    score_rect.topleft = (10, 10)
    screen.blit(score_font, score_rect)

    if (pygame.sprite.groupcollide(bird_group,ground_group, False,False,pygame.sprite.collide_mask) or
        pygame.sprite.groupcollide(bird_group,pipe_group, False,False,pygame.sprite.collide_mask)):
        game_over = True
        break

    pygame.display.update()

while True:
    game_over_font = pygame.font.Font('freesansbold.ttf', 40)
    game_over_screen = game_over_font.render('Game Over', True, (0, 0,0))
    game_over_rect = game_over_screen.get_rect()
    game_over_rect.midtop = (int(SCREEN_SIZE[0]/2),int(SCREEN_SIZE[1]/2)-100)
    screen.blit(game_over_screen, game_over_rect)
    pygame.display.update()
    pygame.time.wait(500)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_q:
                    pygame.quit()
                    exit()