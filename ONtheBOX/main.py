import pygame
from sys import exit #exit() funtion to close game(properly #1)
from player import Player
from backgd import Background
from stuff import Stuff
import os 
BASE_DIR = os.path.dirname(__file__)
clock=pygame.time.Clock() #clockobject made

HEIGHT=608 #we need to write a code to automatically find the size of
LENGTH=1024 #the screen of the player and adjust the screen size automatically i gess
FPS=24
PLAYER_FAT=48
PLAYER_HEIGHT=77
PLAYER_X=150
PLAYER_Y=150
PLAYER_SPEED=20
BLOCKSIZE=32 #must take h and w if make non square blocks
GRAVITY = 0.5
PLAYER_VEL = -10
ICON = pygame.image.load(os.path.join(BASE_DIR, "enemies", "CatBasket.png"))
"""we made them constant for easy to use"""


pygame.init() #nothing just starting on game
#screen = pygame.display.set_mode((1000,600))
screen = pygame.display.set_mode((LENGTH,HEIGHT))
pygame.display.set_caption("we are on the box")

pygame.display.set_icon(ICON)


world = Background(screen,(69,69,69),os.path.join(BASE_DIR, "background", "realbg.jpeg"))
#world=Background(screen,(69,69,69),None)
""" object=pygame.Rect(300,400,32,32)
    pygame.draw.rect(screen,(0,250,250),object,0,1,100,-50,90,1110)
    test code to undersatnt Rect and rect
"""
gameloop=True
object=pygame.Rect(300,400,32,32)
cat=Stuff(screen,LENGTH-((BLOCKSIZE)*6),HEIGHT-(BLOCKSIZE+BLOCKSIZE+25),BLOCKSIZE,BLOCKSIZE,os.path.join(BASE_DIR, "enemies", "CatBasket.png"),2,None)
#define player and objects(for now object and plaer both by player class)

# adding platforms and traps 


floor=[]
for i in range(0,LENGTH,BLOCKSIZE):
    jerry=Stuff(screen,i,HEIGHT-BLOCKSIZE,32,32,os.path.join(BASE_DIR, "lands","forestland.jpeg"),1,None)
    floor.append(jerry)

# adding platforms, just gonna hardcode positions for now and see how it feels
# (col * 32, row * 32) basically
platform_layout = [
    (6,  10, 14),   # first platform low on the left
    (13, 17, 11),   # middle one
    (20, 25, 13),   # longer one in the middle right
    (28, 31,  9),   # high up on the right side
    (3,   6, 10),   # small one on the far left
]

platforms = []
for (start_col, end_col, row) in platform_layout:
    for col in range(start_col, end_col):
        block = Stuff(
            screen,
            col * BLOCKSIZE,
            row * BLOCKSIZE,
            BLOCKSIZE, BLOCKSIZE,
            os.path.join(BASE_DIR, "lands", "forestland.jpeg"),
            1, None
        )
        platforms.append(block)

all_blocks = floor + platforms  # keeping them together makes collision easier later

tom=Player(screen,PLAYER_X,PLAYER_Y,PLAYER_FAT,PLAYER_HEIGHT,all_blocks)

while gameloop==True:
        
   
    world.draw()  
    # tom.movement()
    
    tom.update_direction(5)
    tom.move()
    tom.draw()
    cat.draw()
    for i in all_blocks:
        i.draw()
    

    for event in pygame.event.get():#pygame.event.get gives  all events happned in a [list] every frame (60 frame per sec) 
        if event.type == pygame.QUIT : #pygame.QUIT gives  1 if cross red is pressed 
            
            pygame.quit() #closes pygame (can do gameloop= False also dude)
            exit() #closes entire code (pygame adnpython are diff so alagse close)
        if  event.type == pygame.KEYDOWN and event.key==pygame.K_ESCAPE:
            pygame.quit()
            exit()
    
    tom.movement(PLAYER_SPEED)
    
        
    pygame.draw.rect(screen,(0,250,250),object,0,1,100,-50,90,1110)
    pygame.display.update() #load new screen
    clock.tick(FPS)
