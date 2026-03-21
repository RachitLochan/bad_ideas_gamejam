import pygame

class Player(pygame.Rect):
    #pygame.draw.rect(screen, color, rect)and pygame.Rect diffrece todo->dynamically find size of image and 
    # put accodingly even option toscale
    def __init__(self,gamewindow,startx,starty,fat,tall,image,RATIO):
        self.gamewindow=gamewindow

        playerimage=pygame.image.load(image)
        playerimage=pygame.transform.scale(playerimage,(fat,tall))
        pygame.Rect.__init__(self,startx,starty,fat,tall)

        self.image=playerimage

        if RATIO !=None:
            self.image=pygame.transform.scale_by(self.image,RATIO) 

    
        
        
        
    def move(self):
        keys=pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.x-=15 #making a rect objcet of self.carcter is so so easy than getting self.startx+=5 trust me man
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.y+=15
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.x+=15
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.y-=15
        
    def draw(self):
        self.gamewindow.blit(self.image,(self.topleft))
"""must find some way to find x and y position to update it and 
 in rect it was as simple as rect.x nad rect.y to find x and y
 lol turns out sisnce i inherted rect so i can directly call rect.x lol 
 yahooooooo"""


    
