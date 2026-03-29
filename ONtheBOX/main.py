import pygame
from sys import exit #exit() funtion to close game(properly #1)
from player import Player
from backgd import Background
from stuff import Stuff
from enemy import Enemy
from buttons import Button
import os 
BASE_DIR = os.path.dirname(__file__)

HEIGHT=608
LENGTH=1024
FPS=24
PLAYER_FAT=20
PLAYER_HEIGHT=30
PLAYER_X=150
PLAYER_Y=150
PLAYER_SPEED=20
BLOCKSIZE=32
GRAVITY = 0.5
PLAYER_VEL = -10

pygame.mixer.pre_init(44100, -16, 2, 512) # audio settings for better performance
pygame.init()

screen = pygame.display.set_mode((LENGTH,HEIGHT))
pygame.display.set_caption("we are on the box")

ICON = pygame.image.load(os.path.join(BASE_DIR, "enemies", "CatBasket.png"))
pygame.display.set_icon(ICON)

clock = pygame.time.Clock()

# ---- music helper ----
# checks Music/ folder first then Music/Music/ so it works regardless of folder structure
def music_file(*parts):
    primary = os.path.join(BASE_DIR, "Music", *parts)
    if os.path.exists(primary):
        return primary
    alternate = os.path.join(BASE_DIR, "Music", "Music", *parts)
    if os.path.exists(alternate):
        return alternate
    raise FileNotFoundError(f"Missing music file: {parts[0]}")

# background music loops forever underneath everything
pygame.mixer.music.load(music_file("Backgroundsound.wav"))
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# cat sounds play on top of background music using Sound objects
cute_cat_sound  = pygame.mixer.Sound(music_file("cat_crying.mp3"))
cat_crying_sound = pygame.mixer.Sound(music_file("scary_cat.mp3"))
cute_cat_sound.set_volume(0.6)
cat_crying_sound.set_volume(0.6)
cute_cat_sound.play(-1)

# sound effects
dead_sound = pygame.mixer.Sound(os.path.join(BASE_DIR, "Music", "Deadsound.wav"))
down_sound = pygame.mixer.Sound(os.path.join(BASE_DIR, "Music", "Downsound.wav"))
up_sound   = pygame.mixer.Sound(os.path.join(BASE_DIR, "Music", "Upsound.wav"))

CAT_PROXIMITY = 150
current_track = "normal"

# ---- world ----
world = Background(screen,(69,69,69),os.path.join(BASE_DIR, "background", "realbg.jpeg"))

gameloop    = True
object      = pygame.Rect(300,400,32,32)
cat         = Enemy(screen,LENGTH-((BLOCKSIZE)*6),HEIGHT-(BLOCKSIZE+BLOCKSIZE+25),BLOCKSIZE,BLOCKSIZE,2,None)

# game state
hit_cooldown = 0
game_over    = False
sound_on     = True
menu_state   = "game"  # "game" | "pause" | "settings" | "audio" | "end"

# ---- floor ----
floor = []
for i in range(0,LENGTH,BLOCKSIZE):
    jerry = Stuff(screen,i,HEIGHT-BLOCKSIZE,32,32,os.path.join(BASE_DIR, "lands","forestland.jpeg"),1,None)
    floor.append(jerry)

# ---- platforms ----
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

all_blocks = floor + platforms

tom = Player(screen,PLAYER_X,PLAYER_Y,PLAYER_FAT,PLAYER_HEIGHT,all_blocks)

# ---- fonts ----
warn_font = pygame.font.SysFont("arialblack", 36)
hud_font  = pygame.font.Font(None, 32)

menu_state = "game"
sound_on = True
font = pygame.font.Font(None, 32)
resume_btn   = Button(screen, "Resume",       LENGTH//2, HEIGHT//2 - 60)
settings_btn = Button(screen, "Settings",     LENGTH//2, HEIGHT//2)
quit_btn     = Button(screen, "Quit",         LENGTH//2, HEIGHT//2 + 60)
audio_btn    = Button(screen, "Audio",        LENGTH//2, HEIGHT//2 - 30)
sback_btn    = Button(screen, "Back",         LENGTH//2, HEIGHT//2 + 40)
toggle_btn   = Button(screen, "Toggle Sound", LENGTH//2, HEIGHT//2 - 30)
aback_btn    = Button(screen, "Back",         LENGTH//2, HEIGHT//2 + 40)
restart_btn  = Button(screen, "Restart",      LENGTH//2, HEIGHT//2 - 25)
mainmenu_btn = Button(screen, "Main Menu",    LENGTH//2, HEIGHT//2 + 25)

# ---- spike class ----
class Spike:
    def __init__(self, x, y, w, h, screen, spawn_x, spawn_y):
        self.rect = pygame.Rect(x, y, w, h)
        self.screen = screen
        self.warn_distance = 100
        self.spawn_x = spawn_x
        self.spawn_y = spawn_y
        self.near_spike_jumped = False
        self.cleared_spike = False

    def draw(self):
        tip   = (self.rect.centerx, self.rect.top)
        left  = (self.rect.left,    self.rect.bottom)
        right = (self.rect.right,   self.rect.bottom)
        pygame.draw.polygon(self.screen, (34, 54, 28), [tip, left, right])
        pygame.draw.polygon(self.screen, (22, 38, 18), [tip, left, right], 2)

    def show_warning(self, player, font, LENGTH, HEIGHT):
        if abs(player.x - self.rect.x) < self.warn_distance:
            line1 = font.render("TRAP AHEAD !!  BE CAREFUL !!", True, (220, 20, 20))
            line2 = font.render("JUMP TO AVOID", True, (220, 20, 20))
            self.screen.blit(line1, (LENGTH//2 - line1.get_width()//2, HEIGHT//2 - 50))
            self.screen.blit(line2, (LENGTH//2 - line2.get_width()//2, HEIGHT//2 + 10))
            return True
        return False

    def update(self, player):
        near_spike = abs(player.x - self.rect.x) < self.warn_distance
        if near_spike:
            if player.vel_y < 0:
                self.near_spike_jumped = True
            if (self.near_spike_jumped and
                player.x <= self.rect.x + self.rect.width and
                player.vel_y >= 0):
                self.cleared_spike = True

        # walked into spike without jumping = respawn
        if player.colliderect(self.rect) and player.vel_y >= 0:
            player.x = self.spawn_x
            player.y = self.spawn_y
            self.near_spike_jumped = False
            self.cleared_spike = False

    def teleport(self, player, teleport_x, teleport_y):
        if self.cleared_spike and player.vel_y == 0:
            player.x = teleport_x
            player.y = teleport_y
            self.cleared_spike = False
            self.near_spike_jumped = False

spike = Spike(-300, HEIGHT - BLOCKSIZE - 16, 16, 16, screen, PLAYER_X, PLAYER_Y)

TELEPORT_X = cat.x + cat.width + 20
TELEPORT_Y = cat.y



while gameloop==True:

    world.draw()

    # HUD - always drawn on top of background regardless of menu state
    lives_text = hud_font.render(f"Lives: {tom.health}", True, (255, 255, 255))
    screen.blit(lives_text, (10, 10))

    if not game_over:
        tom.movement(PLAYER_SPEED)   #  moved up here (for some)
        tom.move()
        tom.draw()

        cat.draw()
        cat.update(tom)
        cat.show_door(tom)
        for i in all_blocks:
            i.draw()

        spike.draw()
        spike.show_warning(tom, warn_font, LENGTH, HEIGHT)

        # hit cooldown counts down so player gets recovery time after being hit
        if hit_cooldown > 0:
            hit_cooldown -= 1

        # cat collision - only triggers when cooldown has expired
        if tom.colliderect(cat) and hit_cooldown <= 0:
            tom.health -= 1
            hit_cooldown = int(FPS * 2.5)  # 2.5 seconds recovery time
            if tom.health <= 0:
                game_over = True
                menu_state = "end"   # go straight to end screen
                dead_sound.play()

        spike.update(tom)
        spike.teleport(tom, TELEPORT_X, TELEPORT_Y)

        # proximity sound swap
        dist = ((tom.x - cat.x)**2 + (tom.y - cat.y)**2) ** 0.5
        if dist < CAT_PROXIMITY and current_track != "crying":
            cute_cat_sound.stop()
            cat_crying_sound.play(-1)
            current_track = "crying"
        elif dist >= CAT_PROXIMITY and current_track != "normal":
            cat_crying_sound.stop()
            cute_cat_sound.play(-1)
            current_track = "normal"
    
#this is first part of code for menu
    if menu_state == "pause":
        world.draw()
        paused_text = font.render("PAUSED", True, (255, 255, 0))
        screen.blit(paused_text, paused_text.get_rect(center=(LENGTH//2, HEIGHT//2 - 120)))
        resume_btn.draw()
        settings_btn.draw()
        quit_btn.draw()

    elif menu_state == "settings":
        world.draw()
        stitle = font.render("SETTINGS", True, (255, 255, 0))
        screen.blit(stitle, stitle.get_rect(center=(LENGTH//2, HEIGHT//2 - 100)))
        audio_btn.draw()
        sback_btn.draw()

    elif menu_state == "audio":
        world.draw()
        atitle = font.render("AUDIO", True, (255, 255, 0))
        screen.blit(atitle, atitle.get_rect(center=(LENGTH//2, HEIGHT//2 - 100)))
        status = font.render(f"Sound: {'ON' if sound_on else 'OFF'}", True, (255, 255, 255))
        screen.blit(status, status.get_rect(center=(LENGTH//2, HEIGHT//2 - 60)))
        toggle_btn.draw()
        aback_btn.draw()

    elif menu_state == "end":
        world.draw()
        etitle = font.render("LoL FAILED", True, (255, 0, 0))
        screen.blit(etitle, etitle.get_rect(center=(LENGTH//2, HEIGHT//2 - 80)))
        restart_btn.draw()
        mainmenu_btn.draw()
#this is first part ends here

    # ---- events ----
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            exit()

        # P key toggles pause
            
#code for menu starts here
        if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            if menu_state == "game":
                menu_state = "pause"
            elif menu_state == "pause":
                menu_state = "game"

        if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            menu_state = "end"

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if menu_state == "pause":
                if resume_btn.is_clicked(mouse_pos):
                    menu_state = "game"
                elif settings_btn.is_clicked(mouse_pos):
                    menu_state = "settings"
                elif quit_btn.is_clicked(mouse_pos):
                    pygame.quit()
                    exit()
            elif menu_state == "settings":
                if audio_btn.is_clicked(mouse_pos):
                    menu_state = "audio"
                elif sback_btn.is_clicked(mouse_pos):
                    menu_state = "pause"
            elif menu_state == "audio":
                if toggle_btn.is_clicked(mouse_pos):
                    sound_on = not sound_on
                    if sound_on:
                        pygame.mixer.unpause()
                    else:
                        pygame.mixer.pause()
                elif aback_btn.is_clicked(mouse_pos):
                    menu_state = "settings"

            elif menu_state == "end":
                if restart_btn.is_clicked(mouse_pos):
                    # reset everything back to starting state
                    tom = Player(screen, PLAYER_X, PLAYER_Y, PLAYER_FAT, PLAYER_HEIGHT, all_blocks)
                    game_over    = False
                    hit_cooldown = 0
                    current_track = "normal"
                    cute_cat_sound.stop()
                    cute_cat_sound.play(-1)
                    menu_state = "game"
                elif mainmenu_btn.is_clicked(mouse_pos):
                    pygame.quit()
                    exit()

#code for menu ends here
    #tom.movement(PLAYER_SPEED) someone make me undersatne why a diff move nad movemet is needed its so hard af to debug
    
        
    pygame.draw.rect(screen,(0,250,250),object,0,1,100,-50,90,1110)
    pygame.display.update()
    clock.tick(FPS)




            

    
        

        
