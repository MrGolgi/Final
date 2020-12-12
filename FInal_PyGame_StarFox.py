"""
File: Final_PyGame_StarFox.py
Author: Jason Dusek
CIS 1415 Intro to Programming
Final Project
Date: 12/07/2020

"""
import pygame as p #because I don't want to type pygame over and over
import random
import string
from tkinter import *
"""Importing pygame.locals keeps key presses simple"""
from pygame.locals import *

"""some constants and variables to create before the game """
WIDTH = 800
HEIGHT = 600
gameSpeed = 300
enemySpeed = 300
lives = 3
points = 0
highScores = {}

"""create the player class and its movement, boundaries, and shooting """
class Player(p.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__() #super was a fun addition to these classes to avoid recalling the class
        self.surf = p.image.load("assets/player.png").convert()
        self.rect = self.surf.get_rect()
    """move the player with the keyboard"""    
    def update(self, keys):
        if keys[K_UP]:
            self.rect.move_ip(0, -1)
        if keys[K_DOWN]:
            self.rect.move_ip(0, 1)
        if keys[K_LEFT]:
            self.rect.move_ip(-1, 0)
        if keys[K_RIGHT]:
            self.rect.move_ip(1, 0)
        """keeps the player on the screen"""
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
                
    def fire(self):
        laser = Laser(self.rect.centerx, self.rect.centery) #love these pygame center methods
        lasers.add(laser)
        all_sprites.add(laser)

"""create laser sprite class"""
class Laser(p.sprite.Sprite):
    def __init__(self, x, y):
        super(Laser, self).__init__()
        self.surf = p.image.load("assets/plyLaser.png").convert()
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
        self.rect = self.surf.get_rect(
            center=(
                random.randint(WIDTH + 20, WIDTH + 100),
                random.randint( (0 + self.surf.get_height() // 2), (HEIGHT - self.surf.get_height() // 2) )))
        self.speed = 1
    """move the enemies and 'delete' them after they leave the screen """
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
           
p.init()
"""
a whole mess of loading that would, ideally, be in a game or gameSceen method or class.
"""
screen = p.display.set_mode((WIDTH, HEIGHT))
bgimg = p.image.load("assets/b1.jpg")
caption = p.display.set_caption("PyStarFox")
font = p.font.Font(p.font.get_default_font(), 32)
clock = p.time.Clock()
addEnemy = p.USEREVENT + 1
p.time.set_timer(addEnemy, enemySpeed)

player = Player()


""" all sprite groups, groups for lasers, enemies, and player to use pygame collision """
enemies = p.sprite.Group()
lasers = p.sprite.Group()
all_sprites = p.sprite.Group()
all_sprites.add(player)


def set_points(points):
    points += 100
    return points

gameplay = True
"""
Mainloop for gameplay. Sorry its ugly. I could have spent many more hours on this...
"""
while gameplay:
    
    for event in p.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                gameplay = False
            """ pewpewpew <- yes, fire the laser"""  
            if event.key == K_SPACE:
                player.fire()
        elif event.type == QUIT:
            gameplay = False
            """add in enemies and add them to their sprite groups"""
        elif event.type == addEnemy:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
            
    """update key presses for player movement """
    keys = p.key.get_pressed()
    player.update(keys)
    """class update functions to continually add new sprites to sprite groups in pyGame"""
    enemies.update()
    lasers.update()
    #screen.fill((0, 0, 0)) used prior to loading background image
    screen.blit(bgimg, (0,0))
    text = font.render("POINTS: "+str(points) +" LIVES: "+str(lives), True, (255,255,255) )
    
    """two sets of collisons to detect: player to enemies, lasers to enemies """
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
    """ dectect if player collides with any sprites from enemies group"""
    if p.sprite.spritecollideany(player, enemies):
        """cycle through 3 lives"""
        if (lives == 1):
            lives -=1
            if (lives == 0):
                player.kill()
                gameplay = False
            """last life, kill the player"""
        else:
            lives -=1
            for enemy in enemies:
                enemy.kill()
    """detect if any lasers from laser group collide with any enemies with enemy group"""
    if (p.sprite.groupcollide(enemies, lasers, True, True)):
        points += 100
        gameSpeed += 10
    """display the points and lives on screen"""
    text = font.render("POINTS: "+str(points) +" LIVES: "+str(lives), True, (255,255,255) )
    screen.blit(text, (10,10) )
    """udpate the screen after every update"""
    p.display.flip()
    """slow the game down!...or make it consistent between computer speeds"""
    clock.tick(gameSpeed)
    
"""I decided on a random 3 caps letters for player intiials since the screen entry was taking too long """
plyInt = ''.join(random.choice(string.ascii_uppercase) for i in range(3))

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

""" function to set the high scores into the dictionary of highScores """
def set_high_scores(dictionary, initials, pts):
    top=5
    highScores = dictionary
    plyInt = initials
    points = pts
    highScores.update({plyInt:points})
    with open("assets/highScores.txt","a") as f: #I like using the 'as' command for imports and opens now
        for i,(plyInt,points) in enumerate(sorted(highScores.items(), key= lambda x:-x[1], reverse=True)):
            f.write(f"{plyInt}:{points}\n")

            """
            if i == top-1:
                break
                
            I left this in although, I'm not very good at enumerate() yet, I was hoping to limit the
            highscores to the top 5.
            """

""" function to get the high scores from the file and read them back into the dictionary """
def get_high_scores():
    """try/except and validation"""
    try:
        with open("assets/highScores.txt","r") as f:
            for line in f:
                plyInt,_,points = line.partition(":")
                if plyInt and points:
                    highScores[plyInt]=int(points)
    except FileNotFoundError:
        print("File Not Found")
        return {}
    return highScores

"""run the set_highScore functions"""
set_high_scores(highScores, plyInt, points)

print(plyInt+": "+str(points))
hs = get_high_scores()
print("High Scores: ")
for key, value in sorted(hs.items(), key=lambda x: x[1], reverse=True):
    print(key, ' : ', value)

