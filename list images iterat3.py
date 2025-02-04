import pygame
import os
os.chdir('C:\\Users\\Name\\Desktop\\Character Animation\\')
pygame.init()
pygame.mixer.init()

WIDTH = 1920
HEIGHT = 1080
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Game')

''' IMAGE RESIZING___________________________________________________________'''
wRight1 = pygame.image.load('row2_1.png')
wRight1 = pygame.transform.scale(wRight1, (80,80))
wRight2 = pygame.image.load('row2_2.png')
wRight2 = pygame.transform.scale(wRight2, (80,80))
wRight3 = pygame.image.load('row2_3.png')
wRight3 = pygame.transform.scale(wRight3, (80,80))
wRight4 = pygame.image.load('row2_4.png')
wRight4 = pygame.transform.scale(wRight4, (80,80))
wRight5 = pygame.image.load('row2_5.png')
wRight5 = pygame.transform.scale(wRight5, (80,80))
wRight6 = pygame.image.load('row2_6.png')
wRight6 = pygame.transform.scale(wRight6, (80,80))
wRight7 = pygame.image.load('row2_7.png')
wRight7 = pygame.transform.scale(wRight7, (80,80))``
wRight8 = pygame.image.load('row2_8.png')
wRight8 = pygame.transform.scale(wRight8, (80,80))


wLeft1 = pygame.image.load('row10_1.png')
wLeft1 = pygame.transform.scale(wLeft1, (80,80))
wLeft2 = pygame.image.load('row10_2.png')
wLeft2 = pygame.transform.scale(wLeft2, (80,80))
wLeft3 = pygame.image.load('row10_3.png')
wLeft3 = pygame.transform.scale(wLeft3, (80,80))
wLeft4 = pygame.image.load('row10_4.png')
wLeft4 = pygame.transform.scale(wLeft4, (80,80))
wLeft5 = pygame.image.load('row10_5.png')
wLeft5 = pygame.transform.scale(wLeft5, (80,80))
wLeft6 = pygame.image.load('row10_6.png')
wLeft6 = pygame.transform.scale(wLeft6, (80,80))
wLeft7 = pygame.image.load('row10_7.png')
wLeft7 = pygame.transform.scale(wLeft7, (80,80))
wLeft8 = pygame.image.load('row10_8.png')
wLeft8 = pygame.transform.scale(wLeft8, (80,80))


spinAttackR1 = pygame.image.load('spinattackright1.png')
spinAttackR1 = pygame.transform.scale(spinAttackR1, (90,90))
spinAttackR2 = pygame.image.load('spinattackright2.png')
spinAttackR2 = pygame.transform.scale(spinAttackR2, (90,90))


standStill1 = pygame.image.load('standStill1.png')
standStill1 = pygame.transform.scale(standStill1, (80,80))
standStill2 = pygame.image.load('standStill2.png')
standStill2 = pygame.transform.scale(standStill2, (80,80))
standStill3 = pygame.image.load('standStill3.png')
standStill3 = pygame.transform.scale(standStill3, (80,80))
standStill4 = pygame.image.load('standStill4.png')
standStill4 = pygame.transform.scale(standStill4, (80,80))

'''_________________________________________________________________________'''

bg = pygame.image.load('bg.png')
spinAttackList = [spinAttackR1, spinAttackR2, spinAttackR1, spinAttackR2,
                  spinAttackR1, spinAttackR2, spinAttackR1, spinAttackR2,
                  spinAttackR1, spinAttackR2, spinAttackR1, spinAttackR2,
                  spinAttackR1, spinAttackR2, spinAttackR1, spinAttackR2,
                  spinAttackR1, spinAttackR2, spinAttackR1, spinAttackR2,
                  spinAttackR1, spinAttackR2, spinAttackR1, spinAttackR2,
                  spinAttackR1, spinAttackR2, spinAttackR1, spinAttackR2,
                  spinAttackR1, spinAttackR2, spinAttackR1, spinAttackR2]
walkRight = [wRight1, wRight2,
             wRight3, wRight4,
             wRight5, wRight6,
             wRight7, wRight8]
walkLeft = [wLeft1, wLeft2,
             wLeft3, wLeft4,
             wLeft5, wLeft6,
             wLeft7, wLeft8]

#char = [standStill1, standStill2, standStill3, standStill4]

char = pygame.image.load('topDownattackRight3.png')
char = pygame.transform.scale(char, (80,80))
#R = char.get_rect()

clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

x = 50
y = 770
width = 64
height = 64
vel = 5

isJump = False
jumpCount = 10

spin = False
left = False
right = False
walkCount = 0
attackCount = 0

'''DRAWING SECTION___________________________________________________________'''
def redrawGameWindow():
    global walkCount
    global attackCount
    screen.blit(bg, (0,0))

    if walkCount + 1 >= 24:
        walkCount = 0

    if left:
        screen.blit(walkLeft[walkCount//3], (x,y))
        walkCount += 1
        attackCount += 1
    elif right:
        screen.blit(walkRight[walkCount//3], (x,y))
        walkCount += 1
        attackCount += 1
    else:
        screen.blit(char, (x,y))

    if spin:
        screen.blit(spinAttackList[attackCount//3], (x,y))

    pygame.display.update()


#mainloop
run = True
while run:
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
#_________________________________________________________________________
    if keys[pygame.K_w]:
        spin = True

    if keys[pygame.K_LEFT] and x > vel:
        x -= vel
        left = True
        right = False
    elif keys[pygame.K_RIGHT] and x < WIDTH - 40:
        x += vel
        right = True
        left = False
    else:
        right = False
        left = False
        walkCount = 0
        spin = False

    if not(isJump):
        if keys[pygame.K_SPACE]:
            isJump = True
            right = False
            left = False
            walkCount = 0
    else:
        if jumpCount >= -10:
            neg = 1
            if jumpCount < 0:
                neg = -1
            y -= (jumpCount ** 2) * 0.5 * neg
            jumpCount -= 1
        else:
            isJump = False
            jumpCount = 10

    def redrawGameWindow():
    global walkCount
    global attackCount
    screen.blit(bg, (0,0))

    if left:
        screen.blit(walkLeft[walkCount//3], (x,y))
        walkCount += 1
        walkCount %= len(walkLeft)
        attackCount += 1
        attackCount %= len(spinAttackList)

    elif right:
        screen.blit(walkRight[walkCount//3], (x,y))
        walkCount += 1
        walkCount %= len(walkRight)
        attackCount += 1
        attackCount %= len(spinAttackList)
    else:
        screen.blit(char, (x,y))

    if spin:
        screen.blit(spinAttackList[attackCount//3], (x,y))

    pygame.display.update()



    redrawGameWindow()

pygame.quit()
