import pygame
from sys import exit #exit() funtion to close game(properly #1)
from player import Player
from backgd import Background
from stuff import Stuff
clock=pygame.time.Clock() #clockobject made

HEIGHT=600 #we need to write a code to automatically find the size of
LENGTH=1000 #the screen of the player and adjust the screen size automatically i gess
FPS=24
PLAYER_FAT=32
PLAYER_HEIGHT=32
PLAYER_X=150
PLAYER_Y=150
PLAYER_SPEED=20
ICON=pygame.image.load("enemies\CatBasket.png")
"""we made them constant for easy to use"""

pygame.init #nothing just starting on game
#screen = pygame.display.set_mode((1000,600))
screen = pygame.display.set_mode((LENGTH,HEIGHT))
pygame.display.set_caption("we are on the box")

pygame.display.set_icon(ICON)


world=Background(screen,(69,69,69),"background/SKY.png")
#world=Background(screen,(69,69,69),None)
""" object=pygame.Rect(300,400,32,32)
    pygame.draw.rect(screen,(0,250,250),object,0,1,100,-50,90,1110)
    test code to undersatnt Rect and rect
"""
gameloop=True
object=pygame.Rect(300,400,32,32)

#define player and objects(for now object and plaer both by player class)
tom=Player(screen,PLAYER_X,PLAYER_Y,PLAYER_FAT,PLAYER_HEIGHT,"enemies\CatBasket.png",1)
jerry=Stuff(screen,150,0,64,64,None,(100,200,200))
ground=Stuff(screen,0,536,1000,64,None,(100,255,200))

while gameloop==True:
        
    
    
    world.draw() 
    jerry.draw() 
    ground.draw()
    tom.draw()

    for event in pygame.event.get():#pygame.event.get gives  all events happned in a [list] every frame (60 frame per sec) 
        if event.type == pygame.QUIT : #pygame.QUIT gives  1 if cross red is pressed 
            
            pygame.quit() #closes pygame (can do gameloop= False also dude)
            exit() #closes entire code (pygame adnpython are diff so alagse close)
        if  event.type == pygame.KEYDOWN and event.key==pygame.K_ESCAPE:
            pygame.quit()
            exit()
    tom.move(PLAYER_SPEED)
    
    
        
    pygame.draw.rect(screen,(0,250,250),object,0,1,100,-50,90,1110)
    pygame.display.update() #load new screen
    clock.tick(FPS)
