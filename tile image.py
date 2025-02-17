


from pygame.locals import *
import pygame as pg

pg.init()




 
class Player:
    x = 10
    y = 10
    speed = 1
 
    def moveRight(self):
        self.x = self.x + self.speed
 
    def moveLeft(self):
        self.x = self.x - self.speed
 
    def moveUp(self):
        self.y = self.y - self.speed
 
    def moveDown(self):
        self.y = self.y + self.speed
class Maze:
    def __init__(self):
       self.M = 30
       self.N = 8
       self.maze = [ 1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                     1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,1,
                     1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,
                     1,0,1,1,1,1,1,1,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,1,1,
                     1,0,1,0,0,0,0,0,0,1,1,0,1,0,1,1,1,1,0,1,0,1,0,1,1,1,1,0,1,1,
                     1,0,1,0,1,1,1,1,0,1,1,0,1,0,1,1,1,1,0,1,0,1,0,1,1,1,1,0,1,1,
                     1,0,0,0,0,0,0,0,0,1,1,0,1,0,1,1,1,1,0,1,0,1,0,1,1,1,1,0,1,1,
                     1,1,1,1,1,1,1,1,1,1,1,0,1,0,1,1,1,1,0,1,0,1,0,1,1,1,1,0,1,1]

    def draw(self,display_surf,image_surf):
       bx = 0
       by = 0
       for i in range(0,self.M*self.N):
           if self.maze[ bx + (by*self.M) ] == 1:
               display_surf.blit(self.img,( bx * 44 , by * 44))
      
           bx = bx + 1
           if bx > self.M-1:
               bx = 0 
               by = by + 1

 
class App:
 
    windowWidth = 800
    windowHeight = 600
    player = 0
 
    def __init__(self):
        self._running = True
        self._display_surf = None
        self._image_surf = None
        self.player = Player()
 
    def on_init(self):
        pg.init()
        self._display_surf = pg.display.set_mode((self.windowWidth,self.windowHeight), pg.HWSURFACE)
        
        self._running = True
        self._image_surf = pg.image.load("wall1.png").convert()
 
    def on_event(self, event):
        if event.type == QUIT:
            self._running = False
 
    def on_loop(self):
        pass
    
    def on_render(self):
        self._display_surf.fill((0,0,0))
        self._display_surf.blit(self._image_surf,(self.player.x,self.player.y))
        pg.display.flip()
 
    def on_cleanup(self):
        pg.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while( self._running ):
            pg.event.pump()
            keys = pg.key.get_pressed()
            
            if (keys[K_RIGHT]):
                self.player.moveRight()
 
            if (keys[K_LEFT]):
                self.player.moveLeft()
 
            if (keys[K_UP]):
                self.player.moveUp()
 
            if (keys[K_DOWN]):
                self.player.moveDown()
 
            if (keys[K_ESCAPE]):
                self._running = False
 
            self.on_loop()
            self.on_render()
        self.on_cleanup()
 
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()

