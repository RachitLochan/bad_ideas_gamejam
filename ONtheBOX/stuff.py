import pygame

class Stuff(pygame.Rect):
    def __init__(self,gamewindow,startx,starty,fat,tall,image=None,RATIO=None,colour=None):
        pygame.Rect.__init__(self,startx,starty,fat,tall)
        self.gamewindow=gamewindow
        if image!=None:
            playerimage=pygame.image.load(image)
            playerimage=pygame.transform.scale(playerimage,(fat,tall))
            self.image=playerimage

        if RATIO !=None:
            self.image=pygame.transform.scale_by(self.image,RATIO) 

    
    def draw(self):
        if self.image==None:
            pygame.draw.rect(self.gamewindow,self.colour,self.caracter)
        else:
            self.gamewindow.blit(self.image,(self.topleft))

    
