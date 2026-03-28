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
PLAYER_FAT=20
PLAYER_HEIGHT=30
PLAYER_X=150
PLAYER_Y=150
PLAYER_SPEED=20
BLOCKSIZE=32 #must take h and w if make non square blocks
GRAVITY = 0.5
PLAYER_VEL = -10
ICON = pygame.image.load(os.path.join(BASE_DIR, "enemies", "CatBasket.png"))
"""we made them constant for easy to use"""

pygame.mixer.pre_init(44100, -16, 2, 512) # audio settings for better performance

# Load sounds
dead_sound = pygame.mixer.Sound(os.path.join(BASE_DIR, "Music", "Deadsound.wav"))
down_sound = pygame.mixer.Sound(os.path.join(BASE_DIR, "Music", "Downsound.wav"))
up_sound = pygame.mixer.Sound(os.path.join(BASE_DIR, "Music", "Upsound.wav"))

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

# score/lives/game state
lives = 5
hit_cooldown = 0  # frames before another cat hit can reduce a life
game_over = False

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

    #Ye HUD ko draw karta hai 
    # yeh HUD hai jo lives dikhata hai, isko alag function mein daalna chahiye tha but abhi ke liye theek hai
    font = pygame.font.Font(None, 32)
    lives_text = font.render(f"Lives: {lives}", True, (255, 255, 255))
    screen.blit(lives_text, (10, 10))

    if not game_over:
        tom.update_direction(5) # Update player direction based on movement input
        tom.move()
        tom.draw()
        cat.draw()
        for i in all_blocks:
            i.draw()

        if hit_cooldown > 0:
            hit_cooldown -= 1

        if tom.colliderect(cat) and hit_cooldown <= 0:
            lives -= 1
            hit_cooldown = FPS  # ek sec ke liye buffer de dete hai taaki player ko ek hit ke baad thoda time mile recover karne ke liye

            if lives <= 0:
                game_over = True
                dead_sound.play()  # play death sound when game is over
    else:
        # game over screen
        game_over_text = font.render("Game Over", True, (255, 0, 0))
        go_rect = game_over_text.get_rect(center=(LENGTH//2, HEIGHT//2 - 20))
        screen.blit(game_over_text, go_rect)

        died_text = font.render("You died", True, (255, 255, 255))
        died_rect = died_text.get_rect(center=(LENGTH//2, HEIGHT//2 + 20))
        screen.blit(died_text, died_rect)


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

