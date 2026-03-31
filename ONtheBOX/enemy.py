import pygame
import os
# from player import Player
BASE_DIR = os.path.dirname(__file__)
img = pygame.image.load(os.path.join(BASE_DIR, "door", "still_door.png"))
class Enemy(pygame.Rect):
    
    def loadspritesheet(self,path,framefat,frameheight, scale=1):
        sheet=pygame.image.load(path).convert_alpha()
        frames=[]

        fulllen= sheet.get_width()
        fullheight=sheet.get_height()
        for i in range(0,fulllen,framefat):
            if i + framefat <= fulllen:  #stupid condition for overflow
                frame = sheet.subsurface((i, 0, framefat, frameheight))
                
                if scale != 1:
                    frame = pygame.transform.scale(
                        frame,
                        (int(framefat * scale), int(frameheight * scale))
                    )
                frames.append(frame)
                  
        return frames
    def __init__(self,gamewindow,startx,starty,fat,tall,RATIO=None,colour=None):
        pygame.Rect.__init__(self,startx,starty,fat,tall)

        self.gamewindow = gamewindow
        self.image = None
        self.colour = None
        self.scale = 1
        # in __init__ add:
        self.confused = False
        self.confused_timer = 0
        self.confused_frame = self.loadspritesheet(os.path.join(BASE_DIR, "enemies", "confuse-sprite.png"),32,32,scale = 2)

        

        # 🔹 Enemy animations
        self.idle_frames = self.loadspritesheet(
            os.path.join(BASE_DIR, "enemies", "meow.png"), 32, 28, scale=2
        )

        self.scratch_frames = self.loadspritesheet(
            os.path.join(BASE_DIR, "enemies", "monster.png"), 32, 28, scale=2
        )

        self.state = "idle"
        self.anim_index = 0
        self.animation_speed = 0.4
        self.image = self.idle_frames[0]

        self.vel_x = 0
        self.vel_y = 0

        # 🔹 Door animation (flattened)
        self.door_frames = []

        self.door_frames += self.loadspritesheet(
            os.path.join(BASE_DIR, "enemies", "hide.png"), 32, 28, scale=2
        )

        self.door_frames += self.loadspritesheet(
            os.path.join(BASE_DIR, "door", "door.png"), 40, 64, scale=1
        )

        self.door_frames += self.loadspritesheet(
            os.path.join(BASE_DIR, "door", "door-sprite.png"), 40, 64, scale=1
        )

        # 🔹 Door animation control
        self.door_index = 0
        self.showing_door = False
        self.frame_timer = 0
        self.frame_delay = 10
       
    def update(self, player):
        
        if self.confused:
            self.confused_timer -= 1
            if self.confused_timer <= 0:
                self.confused = False
            return  # skip normal state logic while confused and even swarnim did this in main code
        if self.colliderect(player):
            self.state = "scratch"
        else:
            self.state = "idle"
    def show_door(self, player):
        if abs(self.right - player.left) < 15: #advance python funtion but just see how near is player
            self.showing_door = True

            self.frame_timer += 1

            if self.frame_timer >= self.frame_delay:
                self.frame_timer = 0
                self.door_index += 1

                if self.door_index >= len(self.door_frames):
                    self.door_index = len(self.door_frames) - 1
        
    def draw(self):

        if self.confused:
            self.gamewindow.blit(self.confused_frame[0], self.topleft)
            return

        if self.showing_door:
            image = self.door_frames[self.door_index]
            self.gamewindow.blit(image, self.topleft)
            return

        if self.state == "idle":
            frames = self.idle_frames
        else:
            frames = self.scratch_frames

        self.anim_index += self.animation_speed
        if self.anim_index >= len(frames):
            self.anim_index = 0

        self.image = frames[int(self.anim_index)]
        self.gamewindow.blit(self.image, self.topleft)
            
