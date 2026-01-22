import pygame,random,time,pyautogui
pygame.init()
font1=pygame.font.SysFont("Impact",25)
font2=pygame.font.SysFont("Impact",50)
Gamestate="start"
w,h=pyautogui.size()
sc=pygame.display.set_mode((w,h))
pygame.display.set_caption("2 Player Games")
bck=pygame.transform.scale(pygame.image.load("pygame/spacebackground.jpg"),(w,h))
shipw,shiph=80,80
rship=pygame.transform.scale(pygame.image.load("pygame/redspaceship.png"),(shipw,shiph))
bship=pygame.transform.scale(pygame.image.load("pygame/bluespaceship.png"),(shipw,shiph))
p1,p2=rship,bship
p1=pygame.transform.rotate(p1,90)
p2=pygame.transform.rotate(p2,-90)
rship1=pygame.transform.scale(pygame.image.load("pygame/spaceship2.png"),(150,150))
bship1=pygame.transform.scale(pygame.image.load("pygame/spaceship1.png"),(150,150))
rship1=pygame.transform.rotate(rship,-145)
bship1=pygame.transform.rotate(bship,145)
#rhealth,bhealth=10,10



def handleships(rrect,brect,keypressed):
    if keypressed[pygame.K_DOWN] and rrect.y+rrect.height<h:
        rrect.y+=15
    if keypressed[pygame.K_UP] and rrect.y>0:
        rrect.y-=15
    if keypressed[pygame.K_RIGHT] and rrect.x+rrect.width<w:
        rrect.x+=15
    if keypressed[pygame.K_LEFT] and rrect.x>0:
        rrect.x-=15
    if keypressed[pygame.K_s] and brect.y+brect.height<h:
        brect.y+=15
    if keypressed[pygame.K_w] and brect.y>0:
        brect.y-=15
    if keypressed[pygame.K_d] and brect.x+brect.width<w:
        brect.x+=15
    if keypressed[pygame.K_a] and brect.x>0:
        brect.x-=15




def handlebullets(rbullets,rrect,bbullets,brect,rhealth,bhealth):
    for i in rbullets:
        i.x-=10
        if i.x<0:
            rbullets.remove(i)
        if i.colliderect(brect):
            rbullets.remove(i)
            bhealth-=1
            print(bhealth)
            continue
        for o in bbullets:
            if i.colliderect(o):
                rbullets.remove(i)
                bbullets.remove(o)
                break
    for o in bbullets:
        o.x+=10
        if o.x>w:
            bbullets.remove(o)
        if o.colliderect(rrect):
            bbullets.remove(o)
            rhealth-=1

    if rrect.colliderect(brect):
        rrect.x=w-100
        rrect.y=h/2
        brect.x=50
        brect.y=h/2
        rhealth-1
        bhealth-1




    

def output(rrect,brect,rbullets,bbullets,rhealth,bhealth,winner):
    if Gamestate=="start":
        sc.blit(bck,(0,0))
        sc.blit(rship1,(100,100))
        sc.blit(bship1,(w-200,h-200))
        text1=font1.render("This is two player games",True,"White")
        text2=font2.render("For the red player use the arrow keys to control the ship and the right shift key to shoot",True,"Red")
        text3=font2.render("For the blue player use the WASD keys to control the ship and the left shift key to shoot",True,"Blue")
        text4=font1.render("Good Luck",True,"Green")
        sc.blit(text1,(0,h/3))
        sc.blit(text2,(0,h/3+100))
        sc.blit(text3,(0,h/3+200))
        sc.blit(text4,(0,h/3+300))
    
    elif Gamestate=="play":
        sc.blit(bck,(0,0))
        sc.blit(p1,(rrect.x,rrect.y))
        sc.blit(p2,(brect.x,brect.y))
        for i in rbullets:
            pygame.draw.rect(sc,"red",i)
        for a in bbullets:
            pygame.draw.rect(sc,"blue",a)
        rtext=font1.render(f"health->{rhealth}",True,"Red")
        btext=font1.render(f"health->{bhealth}",True,"Blue")
        sc.blit(rtext,(w-200,20))
        sc.blit(btext,(20,20))
        # pygame.draw.rect(sc,"RED",rrect)
        # pygame.draw.rect(sc,"BLUE",brect)
    
    elif Gamestate=="end":
        winnertext=font2.render(f"THE WINNER IS {winner}",True,"White")
        sc.blit(winnertext,(w/3,h/2))
        text5=font1.render("press the space bar to restart the game",True,"Light Blue")
        sc.blit(text5,(0,h/3))
        pygame.display.update()
def m():
    global Gamestate
    rrect=pygame.Rect(w-100,h/2,shipw,shiph)
    brect=pygame.Rect(50,h/2,shipw,shiph)
    rbullets,bbullets=[],[]
    rhealth,bhealth=10,10
    winner=None
    while 1:
        print(Gamestate)
        for e in pygame.event.get():
            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_RSHIFT and Gamestate=="play":
                    bullet1=pygame.Rect(rrect.x,rrect.y+rrect.height/2,20,10)
                    rbullets.append(bullet1)
                if e.key==pygame.K_LSHIFT and Gamestate=="play":
                    bullet2=pygame.Rect(brect.x+rrect.width,brect.y+brect.height/2,20,10)
                    bbullets.append(bullet2)
                if e.key==pygame.K_SPACE and (Gamestate=="end" or Gamestate=="start"):
                    Gamestate="play"
                    rhealth,bhealth=10,10
        
        if Gamestate=="play":
            if rhealth<=0:
                winner="Yellow wins"

            if bhealth<=0:
                winner="Red wins the game"

            if winner:
                Gamestate="end"
        output(rrect,brect,rbullets,bbullets,rhealth,bhealth,winner)
        keypressed=pygame.key.get_pressed()
        handleships(rrect,brect,keypressed)
        handlebullets(rbullets,rrect,bbullets,brect,rhealth,bhealth)
        pygame.display.update()

m()