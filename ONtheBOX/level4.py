import pygame
from sys import exit
from player import Player
from backgd import Background
from stuff import Stuff
from enemy import Enemy
from buttons4 import Button, RunawayButton, SpecialObject
import os

BASE_DIR = os.path.dirname(__file__)

HEIGHT = 608
LENGTH = 1024
FPS = 24
PLAYER_FAT = 20
PLAYER_HEIGHT = 30
PLAYER_X = 150
PLAYER_Y = 150
PLAYER_SPEED = 20
BLOCKSIZE = 32
GRAVITY = 0.5
PLAYER_VEL = -10
class Level4:
    def play(self):
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.init()

        screen = pygame.display.set_mode((LENGTH, HEIGHT))
        pygame.display.set_caption("we are on the box")

        ICON = pygame.image.load(os.path.join(BASE_DIR, "enemies", "CatBasket.png"))
        pygame.display.set_icon(ICON)

        clock = pygame.time.Clock()

        # ---- music helper ----
        def music_file(*parts):
            primary = os.path.join(BASE_DIR, "Music", *parts)
            if os.path.exists(primary):
                return primary
            alternate = os.path.join(BASE_DIR, "Music", "Music", *parts)
            if os.path.exists(alternate):
                return alternate
            raise FileNotFoundError(f"Missing music file: {parts[0]}")

        pygame.mixer.music.load(music_file("Backgroundsound.wav"))
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1) # loop the background music indefinitely

        cute_cat_sound   = pygame.mixer.Sound(music_file("cat_crying.mp3")) #this one is the crying cat sound that plays when the player gets close to the cat
        cat_crying_sound = pygame.mixer.Sound(music_file("scary_cat.mp3"))
        cute_sound = pygame.mixer.Sound(music_file("cute_cat.mp3"))
        cat_gate_sound = pygame.mixer.Sound(music_file("EnteTheGatesound.wav"))
        cute_cat_sound.set_volume(0.6)
        cat_crying_sound.set_volume(0.6)
        cute_sound.set_volume(0.6)
        cat_gate_sound.set_volume(0.6)
        cute_cat_sound.play(-1)

        dead_sound = pygame.mixer.Sound(os.path.join(BASE_DIR, "Music", "Deadsound.wav"))
        down_sound = pygame.mixer.Sound(os.path.join(BASE_DIR, "Music", "Downsound.wav"))
        up_sound   = pygame.mixer.Sound(os.path.join(BASE_DIR, "Music", "Upsound.wav"))

        CAT_PROXIMITY = 150
        current_track = "normal"

        # ---- world ----
        world = Background(screen, (69, 69, 69), os.path.join(BASE_DIR, "background", "realbg.jpeg"))

        gameloop      = True
        object        = pygame.Rect(300, 400, 32, 32)
        cat           = Enemy(screen, LENGTH - ((BLOCKSIZE) * 6), HEIGHT - (BLOCKSIZE + BLOCKSIZE + 25), BLOCKSIZE, BLOCKSIZE, 2, None)

        hit_cooldown  = 0
        game_over     = False
        sound_on      = True
        level_complete = False
        menu_state    = "game"

        # ---- floor ----
        floor = []
        for i in range(0, LENGTH, BLOCKSIZE):
            jerry = Stuff(screen, i, HEIGHT - BLOCKSIZE, 32, 32, os.path.join(BASE_DIR, "lands", "forestland.jpeg"), 1, None)
            floor.append(jerry)

        # ---- platforms ----
        platform_layout = [
            (6,  10, 14),
            (13, 17, 11),
            (20, 25, 13),
            (28, 31,  9),
            (3,   6, 10),
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

        tom = Player(screen, PLAYER_X, PLAYER_Y, PLAYER_FAT, PLAYER_HEIGHT, all_blocks)

        # ---- fonts ----
        warn_font = pygame.font.SysFont("arialblack", 36)
        hud_font  = pygame.font.Font(None, 32)

        # ---- menu buttons ----
        resume_btn   = Button(screen, "Resume",       LENGTH//2, HEIGHT//2 - 60)
        settings_btn = Button(screen, "Settings",     LENGTH//2, HEIGHT//2)
        quit_btn     = Button(screen, "Quit",         LENGTH//2, HEIGHT//2 + 60)
        audio_btn    = Button(screen, "Audio",        LENGTH//2, HEIGHT//2 - 30)
        sback_btn    = Button(screen, "Back",         LENGTH//2, HEIGHT//2 + 40)
        toggle_btn   = Button(screen, "Toggle Sound", LENGTH//2, HEIGHT//2 - 30)
        aback_btn    = Button(screen, "Back",         LENGTH//2, HEIGHT//2 + 40)
        restart_btn  = Button(screen, "Restart",      LENGTH//2, HEIGHT//2)
        mainmenu_btn = Button(screen, "Main Menu",    LENGTH//2, HEIGHT//2 + 60)

        # ---- runaway sound button ----
        sound_btn = RunawayButton(screen, LENGTH//2, HEIGHT//2,image_path=os.path.join(BASE_DIR, "caracter", "mute.png"))
        # this is the mute button that runs away from the player, forcing them to turn off the sound to win

        # how long (in frames) to show the opening hint — 5 seconds at 24 FPS
        HINT_DURATION = 24 * 5
        hint_timer    = HINT_DURATION
        hint_font     = pygame.font.SysFont("arialblack", 28)

        # ---- special object (girl.png) - player must stand near her to freeze the runaway button ----
        speaker = SpecialObject( 
            screen,
            x=(28 + 31) // 2 * BLOCKSIZE,# placing her on the high platform on the right
            y=9 * BLOCKSIZE - 30, # adjusting y to be on top of the platform and not collide with it
            image_path=os.path.join(BASE_DIR, "caracter", "girl.png"),
            size=60
        ) 

        # ---- game loop ----
        while gameloop == True:

            world.draw()

            lives_text = hud_font.render(f"Lives: {tom.health}", True, (255, 255, 255))
            screen.blit(lives_text, (10, 10))

            # ---- active game ----
            if menu_state == "game" and not game_over and not level_complete: # moved the level_complete check here so the win screen doesn't show the player and cat in the background

                tom.update_direction(5) # moved the movement logic into an update_direction method in player.py to make it cleaner
                tom.movement(PLAYER_SPEED) # this just updates the player's velocity based on input and gravity, the actual position update happens in tom.move() to make collision handling easier
                tom.move() # this applies the velocity to the player's position and handles collisions with the blocks
                tom.draw()# draw the player after moving to ensure he's on top of the blocks

                cat.draw() # draw the cat before updating it so that it appears behind the player (since it can go under the platforms)
                cat.update(tom) # this just updates the cat's position based on the player's position, the actual drawing happens in cat.draw() to make it easier to manage layering

                for i in all_blocks:
                    i.draw()

                # draw girl special object
                speaker.draw() 

                # update and draw the runaway button
                sound_btn.update(tom, speaker) # this checks the distance to the player
                sound_btn.draw() # this draws the button, whether it's frozen or running away

                # opening hint — shown for 5 seconds at the start
                if hint_timer > 0:
                    hint_timer -= 1 # count down the timer
                    hint_surf = hint_font.render("Turn off the audio to win!", True, (150, 0, 0)) # render the hint text
                    screen.blit(hint_surf, (LENGTH//2 - hint_surf.get_width()//2, 60))# draw the hint centered at the top of the screen

                if hit_cooldown > 0:# count down the hit cooldown if it's active
                    hit_cooldown -= 1 # this prevents the player from losing multiple lives in quick succession

                if tom.colliderect(cat) and hit_cooldown <= 0: # if the player collides with the cat and isn't currently invulnerable from a recent hit
                    tom.health -= 1
                    hit_cooldown = int(FPS * 2.5)
                    if tom.health <= 0:
                        game_over = True
                        menu_state = "end"
                        dead_sound.play()

                dist = ((tom.x - cat.x)**2 + (tom.y - cat.y)**2) ** 0.5
                if dist < CAT_PROXIMITY and current_track != "crying":
                    cute_cat_sound.stop()
                    cat_crying_sound.play(-1)
                    current_track = "crying"
                elif dist >= CAT_PROXIMITY and current_track != "normal":
                    cat_crying_sound.stop()
                    cute_cat_sound.play(-1)
                    current_track = "normal"

            # ---- win screen ----
            elif menu_state == "win": # moved the win screen to its own menu state so we can hide the player and cat in the background and just show the win message and buttons
                world.draw() # redraw the world to cover up the player and cat
                win1 = hud_font.render("YOU WIN! Sound is OFF!", True, (100, 255, 100)) # this is the win message that shows when the player successfully clicks the runaway button to turn off the sound, it's a bit more celebratory than the original "The cat is finally at peace." message
                win2 = hud_font.render("The cat is finally at peace.", True, (255, 255, 255)) # this is the original win message that shows when the player successfully clicks the runaway button to turn off the sound, it's a bit more subdued than the new "YOU WIN!" message but still gives a sense of accomplishment and relief for the cat
                screen.blit(win1, win1.get_rect(center=(LENGTH//2, HEIGHT//2 - 120)))
                screen.blit(win2, win2.get_rect(center=(LENGTH//2, HEIGHT//2 - 75)))
                restart_btn.draw()
                mainmenu_btn.draw()

            # ---- pause menu ----
            elif menu_state == "pause":
                world.draw()
                paused_text = hud_font.render("PAUSED", True, (255, 255, 0))
                screen.blit(paused_text, paused_text.get_rect(center=(LENGTH//2, HEIGHT//2 - 120)))
                resume_btn.draw()
                settings_btn.draw()
                quit_btn.draw()

            # ---- settings menu ----
            elif menu_state == "settings":
                world.draw()
                stitle = hud_font.render("SETTINGS", True, (255, 255, 0))
                screen.blit(stitle, stitle.get_rect(center=(LENGTH//2, HEIGHT//2 - 100)))
                audio_btn.draw()
                sback_btn.draw()

            # ---- audio menu ----
            elif menu_state == "audio":
                world.draw()
                atitle = hud_font.render("AUDIO", True, (255, 255, 0)) 
                screen.blit(atitle, atitle.get_rect(center=(LENGTH//2, HEIGHT//2 - 100)))
                status = hud_font.render(f"Sound: {'ON' if sound_on else 'OFF'}", True, (255, 255, 255)) # this shows the current sound status in the audio settings menu, so the player can see whether the sound is currently on or off and toggle it accordingly
                screen.blit(status, status.get_rect(center=(LENGTH//2, HEIGHT//2 - 60)))
                toggle_btn.draw()
                aback_btn.draw()

            # ---- end / game over screen ----
            elif menu_state == "end":
                world.draw()
                etitle = hud_font.render("lil BRO you down bad", True, (255, 0, 0))
                screen.blit(etitle, etitle.get_rect(center=(LENGTH//2, HEIGHT//2 - 80)))
                elabel = hud_font.render("LoL FAILED", True, (255, 255, 255))
                screen.blit(elabel, elabel.get_rect(center=(LENGTH//2, HEIGHT//2 - 40)))
                restart_btn.draw()
                mainmenu_btn.draw()

            # ---- events ----
            for event in pygame.event.get(): # pygame.event.get() gives all events happened in a [list] every frame (60 frame per sec)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: 
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    if menu_state == "game":
                        menu_state = "pause"
                    elif menu_state == "pause":
                        menu_state = "game"

                if event.type == pygame.MOUSEBUTTONDOWN: # check for mouse clicks to interact with buttons
                    mouse_pos = pygame.mouse.get_pos()

                    if menu_state == "game" and sound_btn.is_clicked(mouse_pos): # if the player clicks the runaway button during the game, it toggles the sound and checks for a win condition
                        sound_on = False # turn off the sound
                        pygame.mixer.music.stop() # stop the background music immediately
                        cute_cat_sound.stop() # stop the cute cat sound if it's playing
                        cat_crying_sound.stop() # stop the crying cat sound if it's playing
                        pygame.mixer.stop() # stop all sounds to ensure everything is silent
                        level_complete = True # set the level complete flag to true to prevent the player from moving and show the win screen
                        menu_state = "win" # switch to the win menu state to show the win message and buttons

                    elif menu_state == "pause":
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
            

                        if restart_btn.is_clicked(mouse_pos):
                            tom           = Player(screen, PLAYER_X, PLAYER_Y, PLAYER_FAT, PLAYER_HEIGHT, all_blocks)
                            game_over     = False
                            level_complete = False
                            hit_cooldown  = 0
                            sound_on      = True
                            current_track = "normal"
                            cute_cat_sound.stop()
                            cute_cat_sound.play(-1)
                            pygame.mixer.unpause()
                            sound_btn     = RunawayButton(screen, LENGTH//2, HEIGHT//2,
                                                        image_path=os.path.join(BASE_DIR, "mute.png"))
                            hint_timer    = HINT_DURATION
                            menu_state    = "game"
                        elif mainmenu_btn.is_clicked(mouse_pos):
                            pygame.quit()
                            exit()

            pygame.draw.rect(screen, (0, 250, 250), object, 0, 1, 100, -50, 90, 1110)
            pygame.display.update()
            clock.tick(FPS)
