import pygame
class Background:
    """simple add color/none(tuple or string) and image/none done then todo -> make dynamic bg scaling for diff size windows?"""
    def __init__(self,gamewindow=None,color=None,pictureofbackground=None):
        
        
        self.color=color
        self.gamewindow=gamewindow
        self.image=None
        if gamewindow== None:
            self.gamewindow=pygame.display.set_mode((1000,1))
            pygame.display.set_caption("no screen object given to the background class lol what to do")
        
        # if pictureofbackground == None:
        #     if color== None:
        #         self.gamewindow.fill((0,0,0))
        #     elif color!= None:
        #         self.gamewindow.fill(color)

        if pictureofbackground != None:
              self.image=pygame.image.load(pictureofbackground)
              self.image=pygame.transform.scale(self.image,self.gamewindow.get_size())
        
    def draw(self):
        if self.image !=None:
            self.gamewindow.blit(self.image,(0,0))
        elif self.color != None:
            self.gamewindow.fill(self.color)
        else:
            self.gamewindow.fill((255,255,255))
