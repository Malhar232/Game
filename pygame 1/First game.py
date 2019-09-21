import pygame
pygame.init()
win=pygame.display.set_mode((520,480))
pygame.display.set_caption("First game")
walkRight=[pygame.image.load("R1.png"),pygame.image.load("R2.png"),
           pygame.image.load("R3.png"),pygame.image.load("R4.png"),
           pygame.image.load("R5.png"),pygame.image.load("R6.png"),
           pygame.image.load("R7.png"),pygame.image.load("R8.png"),
           pygame.image.load("R9.png")]

walkLeft=[pygame.image.load("L1.png"),pygame.image.load("L2.png"),
           pygame.image.load("L3.png"),pygame.image.load("L4.png"),
           pygame.image.load("L5.png"),pygame.image.load("L6.png"),
           pygame.image.load("L7.png"),pygame.image.load("L8.png"),
           pygame.image.load("L9.png")]
bg=pygame.image.load("bg.jpg")
char=pygame.image.load("standing.png")
clock=pygame.time.Clock()
music=pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play(-1)
score=0

class player(object):
    def __init__(self,x,y,width,height):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.vel=5
        self.isjump=False
        self.jumpcount=10
        self.left=False
        self.right=False
        self.walkCount=0
        self.standing=True
        self.hitbox=(self.x+20,self.y,28,60)
        

    def draw(self,win):
        if self.walkCount+1>27:
            self.walkCount=0
        if not(self.standing):
            if self.left:
                win.blit(walkLeft[self.walkCount//3],(self.x,self.y))
                self.walkCount+=1
            elif self.right:
                win.blit(walkRight[self.walkCount//3],(self.x,self.y))
                self.walkCount+=1
        else:
            if self.right:
                win.blit(walkRight[0],(self.x,self.y))
            else:
                win.blit(walkLeft[0],(self.x,self.y))
        self.hitbox=(self.x+17,self.y+11,29,52)
        #pygame.draw.rect(win,(255,0,0),self.hitbox,2)
    def hit(self):
        self.isjump=False
        self.jumpcount=10
        self.x=60
        self.y=410
        self.walkcount=0
        font1=pygame.font.SysFont("comicsans",100)
        text=font1.render("-5",1,(255,0,0))
        win.blit(text,(250-(text.get_width()/2),200))
        pygame.display.update()
        i=0
        while i<=300:
            pygame.time.delay(10)
            i+=1
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    i=301
                    pygame.quit()
class projectile(object):
    def __init__(self,x,y,radius,color,facing):
        self.x=x
        self.y=y
        self.radius=radius
        self.color=color
        self.facing=facing
        self.vel=8*facing
    def draw(self,win):
        pygame.draw.circle(win,self.color,(self.x,self.y),self.radius)

class goblin(object):
    walkRight=[pygame.image.load("R1E.png"),pygame.image.load("R2E.png"),
           pygame.image.load("R3E.png"),pygame.image.load("R4E.png"),
           pygame.image.load("R5E.png"),pygame.image.load("R6E.png"),
           pygame.image.load("R7E.png"),pygame.image.load("R8E.png"),
           pygame.image.load("R9E.png"),pygame.image.load("R10E.png"),pygame.image.load("R11E.png")]
    walkLeft=[pygame.image.load("L1E.png"),pygame.image.load("L2E.png"),
           pygame.image.load("L3E.png"),pygame.image.load("L4E.png"),
           pygame.image.load("L5E.png"),pygame.image.load("L6E.png"),
           pygame.image.load("L7E.png"),pygame.image.load("L8E.png"),
           pygame.image.load("L9E.png"),pygame.image.load("L10E.png"),pygame.image.load("L11E.png")]
    def __init__(self,x,y,width,height,end):
         self.x=x
         self.y=y
         self.width=width
         self.height=height
         self.end=end
         self.path=[self.x,self.end]
         self.walkCount=0
         self.vel=3
         self.hitbox=(self.x+17,self.y+2,31,57)
         self.health=10
         self.visible=True
    def draw(self,win):
         self.move()
         if self.visible:
             if self.walkCount +1 >=33:
                 self.walkCount=0
             if self.vel>0:
                 win.blit(self.walkRight[self.walkCount//3],(self.x,self.y))
                 self.walkCount+=1
             else:
                 win.blit(self.walkLeft[self.walkCount//3],(self.x,self.y))
                 self.walkCount+=1
             self.hitbox=(self.x+17,self.y+2,31,57)
             pygame.draw.rect(win,(255,0,0),(self.hitbox[0],self.hitbox[1]-20,50,10))
             pygame.draw.rect(win,(0,128,0),(self.hitbox[0],self.hitbox[1]-20,50-(5*(10-self.health)),10))
             #pygame.draw.rect(win,(255,0,0),self.hitbox,2)
    
    def move(self):
         if self.vel>0:
            if self.x+self.vel<self.path[1]:
                self.x+=self.vel
            else:
                self.vel=self.vel*-1
                self.walkCount=0
         else:
                if self.x-self.vel>self.path[0]:
                    self.x+=self.vel
                else:
                    self.vel=self.vel*-1
                    self.walkCount=0
    def hit(self):
        if self.health>0:
            self.health-=1
        else:
            self.visible=False
        print("hit")
                
        
def newWin():
    win.blit(bg,(0,0))
    hero.draw(win)
    text=font.render("Score:"+str(score),1,(0,0,0))
    win.blit(text,(350,10))
    enemy.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    pygame.display.update()
    
enemy=goblin(100,415,64,64,300)    
hero= player(0,410,64,64)
font=pygame.font.SysFont("comicsans",30,True)
shootLoop=0
bullets=[]
run=True
while run:
    clock.tick(27)
    if enemy.visible==True:
        if hero.hitbox[1]<enemy.hitbox[1]+enemy.hitbox[3] and hero.hitbox[1]+hero.hitbox[3]>enemy.hitbox[1]:
            if hero.hitbox[0] <enemy.hitbox[0]+enemy.hitbox[2] and hero.hitbox[0]+hero.hitbox[2]>enemy.hitbox[0]:
                hero.hit()
                score-=5
    if shootLoop>0:
        shootLoop+=1
    if shootLoop>3:
        shootLoop=0
    keys=pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and shootLoop==0:
        if hero.left:
            facing=-1
        else:
            facing=1
        if len(bullets)<5:
            bullets.append(projectile(round(hero.x +hero.width//2),round(hero.y+hero.height//2),6,(0,0,0),facing))
        shootLoop=1
    if keys[pygame.K_LEFT] and hero.x>hero.vel:
        hero.x-=hero.vel
        hero.left=True
        hero.right=False
        hero.standing=False
    elif keys[pygame.K_RIGHT] and hero.x<500-hero.width-hero.vel:
        hero.x+=hero.vel
        hero.left=False
        hero.right=True
        hero.standing=False
    else:
        hero.standing=True
        hero.walkCount=0
    if not(hero.isjump):
        if keys[pygame.K_UP]:
            hero.isjump=True
            hero.left=False
            hero.right=False
            hero.walkCount=0
    else:
        if hero.jumpcount>=-10:
            neg=1
            if hero.jumpcount<0:
                neg=-1
            hero.y-=(hero.jumpcount**2)*0.5*neg
            hero.jumpcount-=1
        else:
            hero.isjump=False
            hero.jumpcount=10
    newWin()
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False
    for bullet in bullets:
        if bullet.y-bullet.radius<enemy.hitbox[1]+enemy.hitbox[3] and bullet.y+bullet.radius>enemy.hitbox[1]:
            if bullet.x-bullet.radius<enemy.hitbox[0]+enemy.hitbox[2] and bullet.x+bullet.radius>enemy.hitbox[0]:
                enemy.hit()
                score+=1
                bullets.pop(bullets.index(bullet))
                
        if bullet.x < 500 and bullet.x>0:
            bullet.x +=bullet.vel
        else:
            bullets.pop(bullets.index(bullet))
pygame.quit()

