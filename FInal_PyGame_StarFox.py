import pygame as p
import random
import string
from tkinter import *
"""Importing pygame.locals keeps key presses simple"""
from pygame.locals import *

WIDTH = 800
HEIGHT = 600
gameSpeed = 300
enemySpeed = 300
lives = 3
points = 0
highScores = {}

class Player(p.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = p.image.load("assets/player.png").convert()
        self.surf.set_colorkey((255,255,255), RLEACCEL)
        self.rect = self.surf.get_rect()
    """all the keyboard commands for the player"""    
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -1)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 1)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-1, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(1, 0)
        """keep the player on the screen"""
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            
    def fire(self):
        laser = Laser(self.rect.centerx, self.rect.centery)
        lasers.add(laser)
        all_sprites.add(laser)
 
class Laser(p.sprite.Sprite):
    def __init__(self, x, y):
        super(Laser, self).__init__()
        self.surf = p.image.load("assets/plyLaser.png").convert()
        self.surf.set_colorkey((255,255,255), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.rect.centery = y
        self.rect.centerx = x
        """laser definitely needs to move faster than ships"""
        self.speedx = 5
        
    def update(self):
        """laser moves forward, so positive increments"""
        self.rect.x += self.speedx
        if self.rect.left > WIDTH:
            self.kill()

class Enemy(p.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = p.image.load("assets/ship.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(WIDTH + 20, WIDTH + 100),
                random.randint( (0 + self.surf.get_height() // 2), (HEIGHT - self.surf.get_height() // 2) ),
            )
        )
        self.speed = 1

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
           
p.init()

screen = p.display.set_mode((WIDTH, HEIGHT))
caption = p.display.set_caption("PyStarFox")
font = p.font.Font(p.font.get_default_font(), 32)
clock = p.time.Clock()
ADDENEMY = p.USEREVENT + 1
p.time.set_timer(ADDENEMY, enemySpeed)

player = Player()


""" all sprite groups, groups for lasers, enemies, and player to use pygame collision """
enemies = p.sprite.Group()
lasers = p.sprite.Group()
all_sprites = p.sprite.Group()
all_sprites.add(player)

def setPoints(points):
    points += 100
    return points

gameplay = True

while gameplay:
    
    for event in p.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                gameplay = False
              
            if event.key == K_SPACE:
                player.fire()
        elif event.type == QUIT:
            gameplay = False

        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
            

    pressed_keys = p.key.get_pressed()
    player.update(pressed_keys)

    enemies.update()
    lasers.update()
    screen.fill((0, 0, 0))
    text = font.render("POINTS: "+str(points) +" LIVES: "+str(lives), True, (255,255,255) )
    

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    if p.sprite.spritecollideany(player, enemies):
        if (lives == 1):
            lives -=1
            if (lives == 0):
                player.kill()
                gameplay = False
                
        else:
            lives -=1
            for enemy in enemies:
                enemy.kill()

    if (p.sprite.groupcollide(enemies, lasers, True, True)):
        points += 100
        gameSpeed += 10
        if (enemySpeed > 0):
            enemySpeed -= 10
        else:
            enemySpeed = 0

    text = font.render("POINTS: "+str(points) +" LIVES: "+str(lives), True, (255,255,255) )
    screen.blit(text, (10,10) )
    p.display.flip()
    clock.tick(gameSpeed)
    

plyInt = random.choice(string.ascii_letters)

"""
Leaving this code in but commented out. Yes, the game is functional, but I also spent a great
amount of time trying to have a popup box on the screen asking for player initials and then use
those initials for the High Score display 

def updatePlayerInt():
    entry.destroy()
    return plyInt.get(1.0,END)

entry = Tk()
entry.title("High Scores")
Label(entry, text="Enter Initials: ").grid(row=0)
Label(entry, text="Points: ").grid(row=1)
Label(entry, text=str(points)).grid(row=1, column=1)
e1 = Entry(entry, textvariable= txtVar, width=5).grid(row=0, column=1)
plyInt = StringVar(entry, txtVar)
b1 = Button(entry,text="Submit",command=updatePlayerInt).grid(row=2, column =1)
entry.mainloop()
"""

def set_highScores(dictionary, initials, pts, fn = "assets/highScores.txt", top_n=5):
    highScores = dictionary
    plyInt = initials
    points = pts
    highScores.update({plyInt:points})
    with open(fn,"a") as f:
        for idx,(plyInt,points) in enumerate(sorted(highScores.items(), key= lambda x:-x[1], reverse=True)):
            f.write(f"{plyInt}:{points}\n")
            if top_n and idx == top_n-1:
                break

def get_highScores(fn = "assets/highScores.txt"):
    
    try:
        with open(fn,"r") as f:
            for line in f:
                plyInt,_,points = line.partition(":")
                if plyInt and points:
                    highScores[plyInt]=int(points)
    except FileNotFoundError:
        print("File Not Found")
        return {}
    return highScores

set_highScores(highScores, plyInt, points)

print(plyInt+": "+str(points))
hs = get_highScores()
print("High Scores: ")
print(hs)

