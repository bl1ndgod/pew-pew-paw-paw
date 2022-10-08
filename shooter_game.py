from pygame import *
from random import *
#Init
mixer.init()
font.init()
#NeSounds
#mixer.music.load('space.ogg')
#mixer.music.play()
window = display.set_mode((700,800))    
display.set_caption('Игра')

#Images
background = transform.scale(image.load('galaxy.jpg'),(700,800))
hero = transform.scale(image.load('rocket.png'), (35,35))
enemy = transform.scale(image.load('ufo.png'), (50,50))
bullet = transform.scale(image.load('bullet.png'), (100,100))
asteroid = transform.scale(image.load('asteroid.png'), (100,100))
#Clock
FPS = 60
clock =  time.Clock()

font1 = font.SysFont('Arial', 31)
lost = 0
game = True
counter = 0
counter2 = 0
yes = False
times = 0
monsters_killed = 0
finished = False
win = True
reload_check = 0
tumbler = False
counter_reload = 5
hp = 3
can = True

class GameSprite(sprite.Sprite):
    def __init__(self, img, width, height, player_x, player_y, step):
        super().__init__()
        self.width = width
        self.height = height
        self.image = transform.scale(image.load(img), (self.width, self.height))
        self.rect = self.image.get_rect()
        self.step = step
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self): #вывести на экран
        window.blit(self.image, (self.rect.x, self.rect.y))

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.step # пуля все время летит вверх
        if self.rect.y < -self.height:
            self.kill()

class Player(GameSprite): # корабль которым мы управляем
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x >= self.step:
            self.rect.x -= self.step 
        if keys[K_d] and self.rect.x <= (700 - self.width - self.step):
            self.rect.x += self.step
    def fire(self): # выстрел - создается пуля и добавляеся в группу пуль
        global reload_check
        global can
        if can == True:
            bullet = Bullet("bullet.png", 10, 25, (self.rect.x + 30), 770, 3)
            bullets.add(bullet)
            reload_check += 1
    def reload(self):
        global reload_check
        global tumbler
        global counter_reload
        global can
        if reload_check == 5:
            can = False
            tumbler = True
            counter_reload = 180
            reload_check = 0
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.step
        global lost
        if self.rect.y >= 800:
            lost += 1
            self.rect.y = randint(-150, -50)
            self.rect.x = randint(0, 650)
            self.step = randint(2,4)
class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.step
        if self.rect.y >= 1000:
            self.rect.y = randint(-300, -100)
            self.rect.x = randint(0, 630)
#Groups
hero = Player('rocket.png',45,65, 250, 700, 5)
bullets = sprite.Group()
enemies = sprite.Group()
asteroids = sprite.Group()
asteroid = Asteroid('asteroid.png',75,75,randint(0, 650),randint(-150, -50), randint(1,2))
asteroids.add(asteroid)

for i in range(5):
    enemy = Enemy("ufo.png", 75,75,randint(0, 630),randint(-150, -50), 2)
    enemies.add(enemy)


while game:
    window.blit(background, (0,0))
    #text render
    text_lost = font1.render("Пропущено: " + str(lost) + " из 7", 1, (255,255,255))
    text_win = font1.render("Сбито: " + str(monsters_killed) + " из 15", 1, (255,255,255))
    text_reload = font1.render("Перезарядка... " + str(int(counter_reload / 60)), 1, (200,0,0))
    text_hp = font1.render('Здоровье:' + str(hp), 1, (0, 150, 50))
    time1 = font1.render("Времени прошло: " + str(times), 1, (255,255,255))
    time = font1.render("Времени прошло: " + str(times), 1, (0,100,255))
    text_ammo = font1.render("Зарядов: " + str(reload_check) + " из 5",1, (200,0,0))
    #text blit
    window.blit(text_lost, (0,0))
    window.blit(text_win,(0,25))
    window.blit(text_hp,(543,20))
    window.blit(text_ammo,(503,40))
    hero.reset()
    if finished:
        window.blit(time, (235,400))
        
    #counters   
    counter2 += 1
    if counter2 == 60 and finished != True:
        times += 1
        counter2 = 0
    #keys
    for e in event.get():
        if e.type == QUIT:
            game = False    
        elif e.type == KEYDOWN and e.key == K_SPACE and finished == False:
            hero.fire()
    if not finished:
        hero.reset()
        hero.update()
        hero.reload()
        bullets.draw(window)
        bullets.update()
        enemies.draw(window)
        enemies.update()
        asteroids.draw(window)
        asteroids.update()
        window.blit(time1, (450,0))
        kill_list = sprite.groupcollide(enemies, bullets, True, True)
        if tumbler == True:
            counter_reload  -= 1
            if counter_reload <= -5:
                tumbler == False 
                can = True
                counter_reload = 180
            if can == False:
                window.blit(text_reload, (200,750))

        for enem in kill_list: #Monster killed
            monsters_killed += 1
            enemy = Enemy("ufo.png", 75,75,randint(0, 630),randint(-150, -50), randint(2,3))
            enemies.add(enemy)
        if monsters_killed >= 15:
            finished = True
        elif lost >= 7  :
            finished = True
            win = False
        if sprite.spritecollide(hero, asteroids, True) or sprite.spritecollide(hero, enemies, True):
            hp -= 1
        if hp == 0:
            finished = True
            win = False       
    else:
        if win == True: #Победа
           pass
        if win == False: #Поражение
            pass
  
    display.update()
    clock.tick(FPS)