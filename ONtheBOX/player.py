import pygame

GRAVITY = 1
PLAYER_VEL = -15

class Player(pygame.Rect):
    #pygame.draw.rect(screen, color, rect)and pygame.Rect diffrece todo->dynamically find size of image and 
    # put accodingly even option toscale
    def __init__(self,gamewindow,startx,starty,fat,tall,image,RATIO,tiles):
        self.gamewindow=gamewindow
        self.tiles=tiles
        #self.startx=startx
        #self.starty=starty))
        player_L=pygame.image.load(image)
        self.player_L=pygame.transform.scale(player_L,(fat,tall))
        self.player_R = pygame.transform.flip(player_L, True, False)
        self.direction = "left"
        self.vel_x = 0
        self.vel_y = 0
        pygame.Rect.__init__(self,startx,starty,fat,tall)

        self.image=player_L

        if RATIO !=None:
            self.image=pygame.transform.scale_by(self.image,RATIO) 

    def jump(self):
        # Only jump if standing on a tile or ground
        on_ground = self.bottom >= self.gamewindow.get_height()
        for tile in self.tiles:
            if self.bottom == tile.top and self.right > tile.left and self.left < tile.right:
                on_ground = True
        if on_ground:
            self.vel_y = PLAYER_VEL    

    def collision(self):
        # horizontal
        self.x += self.vel_x
        for tile in self.tiles:
            if self.colliderect(tile):
                if self.vel_x > 0:  # moving right
                    self.right = tile.left
                elif self.vel_x < 0:  # moving left
                    self.left = tile.right
                self.vel_x = 0

        # vertical
        self.y += self.vel_y
        for tile in self.tiles:
            if self.colliderect(tile):
                if self.vel_y > 0:  # falling
                    self.bottom = tile.top
                elif self.vel_y < 0:  # jumping
                    self.top = tile.bottom
                self.vel_y = 0



        
    def move(self,speed):


        if self.direction == "right":
            self.image = self.player_R
        elif self.direction == "left":
            self.image = self.player_L


        keys=pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.direction = "right"
            self.x=max(0,self.x-speed)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.y=min(self.y+speed,self.gamewindow.get_height()-self.height)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.direction = "left"
            self.x=min(self.x+speed,self.gamewindow.get_width()-self.width)
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.jump()
#swarnim part        
        self.vel_y += GRAVITY
        self.y += self.vel_y

        self.collision()

        # ground collision for now later blocks too
        if self.bottom >= self.gamewindow.get_height():
            self.bottom = self.gamewindow.get_height()
            self.vel = 0
    def draw(self):
        self.gamewindow.blit(self.image,(self.topleft))
"""must find some way to find x and y position to update it and 
 in rect it was as simple as rect.x nad rect.y to find x and y
 lol turns out sisnce i inherted rect so i can directly call rect.x lol 
 yahooooooo"""


       
      
