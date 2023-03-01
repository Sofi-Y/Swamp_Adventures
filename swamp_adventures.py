import pygame
from pygame.locals import *
import sys
import random
import time
import os
import schedule

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("music1.mp3")
pygame.mixer.music.play()
vec = pygame.math.Vector2

im = pygame.image.load('end.png')
im1 = pygame.image.load('swamp_fon2.png')
im2 = pygame.image.load('crown.png')
white = (255, 64, 64)
# displaysurface.fill((white))
# displaysurface.blit(img,(0,0))
HEIGHT = 1080
WIDTH = 1920
ACC = 0.5
FRIC = -0.12
FPS = 50
screen_rect = (0, 0, WIDTH, HEIGHT)
A_Vel_x = random.choice([i for i in range(1, 10)])
A_Vel_y = random.choice([i for i in range(1, 10)])
M_Vel_x = random.choice([i for i in range(1, 10)])
M_Vel_y = random.choice([i for i in range(0, 10)])
gravity = 8
GRAVITY = 1
platform_vel = 5

resolution = (400, 300)
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

gameOver = False

FramePerSec = pygame.time.Clock()
 
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.update()
pygame.display.set_caption("Swamp Adventures")


def start_screen():
    fon = pygame.transform.scale(pygame.image.load('заставка.png'), (WIDTH, HEIGHT))
    displaysurface.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        FramePerSec.tick(FPS)

       
start_screen()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        # self.image = pygame.image.load("character.png")
        # self.surf = pygame.Surface((30, 30))
        self.score = 0
        self.surf = pygame.image.load("frog1012.png")
        # self.surf.fill((255,255,0))
        self.rect = self.surf.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.surf)
        self.pos = vec((10, 1040))  # 360
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.jumping = False

        self.WW = 0
        # print(self.vel, type(self.vel), list(self.vel))

    def move(self):
        self.acc = vec(0,0.5)
    
        pressed_keys = pygame.key.get_pressed()
                
        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC
                 
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
         
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
             
        self.rect.midbottom = self.pos
 
    def jump(self):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -15
 
    def cancel_jump(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3
        if self.score >= 10:
            self.surf = pygame.image.load("frog301-k.png")
        else:
            self.surf = pygame.image.load("frog301.png")
 
    def update(self):       
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if self.vel.y > 0:        
            if hits:
                if self.pos.y < hits[0].rect.bottom:
                    if hits[0].point == True:   
                        hits[0].point = False
                        self.score += 1
                    self.pos.y = hits[0].rect.top + 1
                    self.vel.y = 0
                    self.jumping = False
                    if self.score >= 10:
                        self.surf = pygame.image.load("frog1012-k.png")
                    else:
                        self.surf = pygame.image.load("frog1012.png")

        # self.surf.set_size(int(surf.get_width()) * 2, int(surf.get_height()) * 2)
        
    def change(self):
        #self.surf = pygame.image.load("frog2.png")
        if self.score >= 10:
            self.surf = pygame.image.load("frog201-k.png")
        else:
            self.surf = pygame.image.load("frog201.png")

    def change_again(self):
        if self.score >= 10:
            self.surf = pygame.image.load("frog1012-k.png")
        else:
            self.surf = pygame.image.load("frog1012.png")

    def dragonfly(self):
        self.score += 5

    def change_size(self):
        pass

 
P1 = Player()





class Ball(pygame.sprite.Sprite):
    def __init__(self, radius=15, x=random.choice([i for i in range(1, 400)]),
                 y=0):
        super().__init__()
        self.radius = radius
        #self.surf = pygame.Surface((2 * radius, 2 * radius),
                                    # pygame.SRCALPHA, 32)
        self.surf = pygame.image.load("swamp\dragonfly11.png")
        #pygame.draw.circle(self.surf, pygame.Color("red"),
                           # (radius, radius), radius)
        self.rect = pygame.Rect(x, y, 2 * radius, 2 * radius)
        self.vy = 20
        self.dx = 10
        self.dy = 10
        self.x = x
        self.y = y
        self.rect = self.surf.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.surf)
        self.frames = ['swamp\dragonfly11.png', 'swamp\dragonfly21.png',
                               'swamp\dragonfly31.png', 'swamp\dragonfly41.png']
        self.index = 0
 
        #now the image that we will display will be the index from the image array 
        self.surf = pygame.image.load(self.frames[self.index])
 
        #creating a rect at position x,y (5,5) of size (150,198) which is the size of sprite 

    def move(self):
        if not pygame.sprite.collide_mask(self, P1) and self.rect.center[0] < WIDTH:
            self.rect = self.rect.move(3, 0)
        else:
            P1.dragonfly()
            self.kill()

    def update(self):
        # when the update method is called, we will increment the index
        self.index += 1

        #if the index is larger than the total images
        if self.index >= len(self.frames):
            #we will make the index to 0 again
            self.index = 0
        
        #finally we will update the image that will be displayed
        self.surf = pygame.image.load(self.frames[self.index])


class Mosquito(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('mosquito1.png')
        self.surf = pygame.image.load('mosquito1.png')
        self.rect = self.surf.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        self.QQ = 0
        self.mask = pygame.mask.from_surface(self.surf)
        self.M_Vel_x = random.choice([i for i in range(1, 10)])
        self.M_Vel_y = random.choice([i for i in range(0, 10)])

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)
            
    def move(self):
        if (not pygame.sprite.collide_mask(self, P1) and
                self.rect.center[0] < WIDTH and self.rect.center[0] < HEIGHT):
            self.rect = self.rect.move(self.M_Vel_x, self.M_Vel_y)
        elif pygame.sprite.collide_mask(self, P1) and self.QQ < 1:
            P1.change_size()
            self.QQ += 1
            self.kill()
        else:
            self.kill()

# MOSQUITO

        # random.choice([i for i in range(1, 400)])
class Arrow(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # self.surf = pygame.Surface((2 * radius, 2 * radius),
                                    # pygame.SRCALPHA, 32)
        self.surf = pygame.image.load("arrow1.png")
        #pygame.draw.circle(self.surf, pygame.Color("red"),
                           # (radius, radius), radius)
        #self.rect = pygame.Rect(x, y, 2 * radius, 2 * radius)
        self.image = pygame.image.load('arrow1.png')
        self.rect = self.surf.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.surf)
        self.A_Vel_x = random.choice([i for i in range(1, 10)])
        self.A_Vel_y = random.choice([i for i in range(1, 10)])
        # creating a rect at position x,y (5,5) of size (150,198) which is the size of sprite

    def move(self):
        if not pygame.sprite.collide_mask(self, P1):
            self.rect = self.rect.move(self.A_Vel_x, self.A_Vel_y)  # 3,4
        elif pygame.sprite.collide_mask(self, P1):
            time.sleep(1)
            #displaysurface.fill((255, 0, 0))
            displaysurface.blit(im, (0, 0))
            pygame.display.update()
            time.sleep(0.5)
            pygame.quit()
            sys.exit()

        # self.rect = self.rect.move(0, self.vy)
       
            
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)


            
class platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # self.surf = pygame.Surface((random.randint(50,100), 12))
        # self.surf.fill((0, 255, 0))
        self.surf = pygame.image.load("water_lily11.png")
        self.rect = self.surf.get_rect(center=(random.randint(-1000, WIDTH - 10),
                                                 random.randint(-1000, HEIGHT - 30)))
        self.speed = random.randint(-5, 5)  # 5
        # random.randint(-1, 1)
        
        self.point = True   
        self.moving = True
        self.mask = pygame.mask.from_surface(self.surf)
    
    def move(self):
        if self.moving == True:  
            self.rect.move_ip(self.speed, 0)
            if self.speed > 0 and self.rect.left > WIDTH:
                self.rect.right = 0
            if self.speed < 0 and self.rect.right < 0:
                self.rect.left = WIDTH

    def update(self):
        pass


class Particle(pygame.sprite.Sprite):
    # сгенерируем частицы разного размера
    fire = [pygame.image.load("star.png")]  # [load_image("star.png")]

    for scale in (5, 10, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(all_sprites)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()
        self.surf = pygame.image.load("star.png")
        # у каждой частицы своя скорость — это вектор
        self.velocity = [dx, dy]
        # и свои координаты
        self.rect.x, self.rect.y = pos

        # гравитация будет одинаковой (значение константы)
        self.gravity = GRAVITY

    def update(self):
        # применяем гравитационный эффект: 
        # движение с ускорением под действием гравитации
        self.velocity[1] += self.gravity
        # перемещаем частицу
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # убиваем, если частица ушла за экран
        if not self.rect.colliderect(screen_rect):
            self.kill()

    def move(self):
        pass
    

class Crown(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load("crown.png")
        self.rect = self.surf.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        self.ticks = pygame.time.get_ticks()
        
    def update(self):
        if self.ticks // 1000 >= 10:
            self.kill()

    def move(self):
        pass

     
def check(platform, groupies):
    if pygame.sprite.spritecollideany(platform, groupies):
        return True
    else:
        for entity in groupies:
            if entity == platform:
                continue
            if (abs(platform.rect.top - entity.rect.bottom) < 40) and (abs(platform.rect.bottom - entity.rect.top) < 40):
                return True
        C = False

 
def plat_gen():
    while len(platforms) < 6:
        width = random.randrange(50, 100)
        p  = platform()      
        C = True
         
        while C:
            p = platform()
            p.rect.center = (random.randrange(0, WIDTH - width),
                             random.randrange(-50, 0))
            C = check(p, platforms)
        platforms.add(p)
        all_sprites.add(p)
 
 

def create_particles(position):
    # количество создаваемых частиц
    particle_count = 20
    # возможные скорости
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))

        
PT1 = platform()
B = Ball()
A = Arrow()
M = Mosquito()
K = Crown()

PT1.surf = pygame.Surface((WIDTH, 40))
PT1.surf.fill((154, 205, 50))
PT1.rect = PT1.surf.get_rect(center=(WIDTH / 2, HEIGHT - 10))
 
all_sprites = pygame.sprite.Group()
all_sprites.add(PT1)
all_sprites.add(P1)


def job():
    all_sprites.add(Ball())


def job1():
    all_sprites.add(Arrow())

    
def job2():
    all_sprites.add(Mosquito())


def job3():
    C = True
    pl = platform()
    while C:
        pl = platform()
        C = check(pl, platforms)
    platforms.add(pl)
    all_sprites.add(pl)
    
    
def job4():
    if K in all_sprites:
        all_sprites.remove(K)


schedule.every(5).seconds.do(job)
schedule.every(10).seconds.do(job1)  # 10
schedule.every(15).seconds.do(job2)  # 15
schedule.every(30).seconds.do(job3)
schedule.every(5).seconds.do(job4)
# all_sprites.add(B)
# all_sprites.add(A)
# all_sprites.add(M)

platforms=pygame.sprite.Group()
platforms.add(PT1)

PT1.moving=False
PT1.point=False

for x in range(random.randint(4, 50)):
    C = True
    pl = platform()
    while C:
        pl = platform()
        C = check(pl, platforms)
    platforms.add(pl)
    all_sprites.add(pl)    # 5

interval = 0.5
interval1 = 0.2

nxt = pygame.time.get_ticks() + (2 * 1000)
nxt1 = pygame.time.get_ticks() + (1000)
while True:
    P1.update()
    # if P1.score == 2:
        # all_sprites.add(K)
    all_sprites.update()
    schedule.run_pending()
    # pygame.mixer.music.play(0)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            # создаём частицы по щелчку мыши
            create_particles(pygame.mouse.get_pos())
        if event.type == pygame.KEYDOWN:    
            if event.key == pygame.K_SPACE:
                P1.jump()
                P1.change()
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
                # P1.change_again()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                P1.cancel_jump()
        # if int(P1.score) % 2 == 0:
            # P1.change1()
       # if int(P1.score) == 1:
            # P1.upgrade()
        

    if P1.rect.top > HEIGHT:
        for entity in all_sprites:
            entity.kill()
            time.sleep(1)
            #displaysurface.fill((255, 0, 0))
            displaysurface.blit(im, (0, 0))
            pygame.display.update()
            time.sleep(1)
            pygame.quit()
            sys.exit()
 
    if P1.rect.top <= HEIGHT / 3:
        P1.pos.y += abs(P1.vel.y)
        for plat in platforms:
            plat.rect.y += abs(P1.vel.y)
            if plat.rect.top >= HEIGHT:  # HEIGHT
                plat.kill()

    if P1.score == 10:
        create_particles((WIDTH / 2, (HEIGHT / 2) + 150))
        all_sprites.add(K)


    plat_gen()
    
    
    displaysurface.fill((0, 0, 0))
    displaysurface.blit(im1, (0, 0))
        
   
    f = pygame.font.SysFont("Verdana", 20)
    g = f.render(str(P1.score), True, (0, 0, 255))
    displaysurface.blit(g, (WIDTH/2, 10))   
     
    for entity in all_sprites:
        displaysurface.blit(entity.surf, entity.rect)
        entity.move()
    pygame.display.update()
    FramePerSec.tick(FPS)
