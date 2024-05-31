import pygame, os

DIR_PATH = os.path.dirname(__file__)
DIR_IMAGE = os.path.join(DIR_PATH, 'image')

#declare color
white = (255,255,255)
black = (0,0,0)
green = (51,204,0)

#declare screen size
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 960
SCORE_HEIGHT = 100

size_Grass = [32,32]
size_Player = [20,20]
size_Flame = [24,24]

clock=pygame.time.Clock()

#Font=pygame.font.SysFont("arial",30,True,False)

class SpriteSheet:
    def __init__(self, filename):
        self.baseImage = pygame.image.load(os.path.join(DIR_IMAGE, filename))
        self.spr = []

    def get_image(self,x,y,size):
        image = pygame.Surface(size)
        image.blit(self.baseImage, (0, 0), (x, y, size[0], size[1]))
        image_scaled = pygame.transform.scale(image,(size[0]*4,size[1]*4))
        image_scaled.set_colorkey(black)
        self.spr.append(image_scaled)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        self.elapsedTime = 0
        self.limitTime = 1000/20
        
        self.index=0
        self.spr = SpriteSheet('phoenix-cc0-spritesheet.png')

        for i in range(4):
            for j in range(5):
                self.spr.get_image(j*size_Player[0],i*size_Player[1],size_Player)

        self.spr_normal = [
            self.spr.spr[0],self.spr.spr[2],self.spr.spr[1],
            self.spr.spr[2],self.spr.spr[0],self.spr.spr[0],
            self.spr.spr[0],self.spr.spr[0],self.spr.spr[0]]
        self.spr_attacking = [
            self.spr.spr[5],self.spr.spr[6],self.spr.spr[7],
            self.spr.spr[8],self.spr.spr[9],self.spr.spr[10],
            self.spr.spr[11],self.spr.spr[12],self.spr.spr[13],
            self.spr.spr[14],self.spr.spr[15],self.spr.spr[16],
            self.spr.spr[17],self.spr.spr[18]]
            
        self.pos_x=SCREEN_WIDTH/2-40
        self.pos_y=SCREEN_HEIGHT/2-40

        self.attacking = False
        self.fliped = False

        self.images = self.spr_normal
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center=(self.pos_x,self.pos_y))

    def flip_image(self):
        self.images=[pygame.transform.flip(image,True,False) for image in self.images]

    def update(self):
        #check boundary
        if self.pos_x < 0:
            self.pos_x = 0
        elif self.pos_x > SCREEN_WIDTH-size_Player[0]*4:
            self.pos_x = SCREEN_WIDTH-size_Player[0]*4
        if self.pos_y < SCORE_HEIGHT:
            self.pos_y = SCORE_HEIGHT
        elif self.pos_y > SCREEN_HEIGHT-size_Player[1]*4:
            self.pos_y = SCREEN_HEIGHT-size_Player[1]*4

        if(self.attacking==True):
            self.images=self.spr_attacking
        else:
            self.images=self.spr_normal

        self.elapsedTime += clock.get_time()
        if self.elapsedTime < self.limitTime:
            pass
        else:
            self.elapsedTime = 0
            self.index+=1
            if self.index >=len(self.images):
                self.index=0
            if(self.fliped==True):
                self.image = pygame.transform.flip(self.images[self.index],True,False)
            else:
                self.image = self.images[self.index]
