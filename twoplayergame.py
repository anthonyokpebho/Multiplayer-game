import pygame, random, time, pyautogui
pygame.init()

font1 = pygame.font.SysFont("Impact", 25)
font2 = pygame.font.SysFont("Impact", 50)

Gamestate = "start"
w, h = pyautogui.size()
sc = pygame.display.set_mode((w, h))
pygame.display.set_caption("2 Player Games")

bck = pygame.transform.scale(pygame.image.load("pygame/spacebackground.jpg"), (w, h))

shipw, shiph = 80, 80
rship = pygame.transform.scale(pygame.image.load("pygame/redspaceship.png"), (shipw, shiph))
bship = pygame.transform.scale(pygame.image.load("pygame/bluespaceship.png"), (shipw, shiph))

p1 = pygame.transform.rotate(rship, 90)
p2 = pygame.transform.rotate(bship, -90)

rship1 = pygame.transform.scale(pygame.image.load("pygame/spaceship2.png"), (150, 150))
bship1 = pygame.transform.scale(pygame.image.load("pygame/spaceship1.png"), (150, 150))


def handleships(rrect, brect, keypressed):
    if keypressed[pygame.K_DOWN] and rrect.y + rrect.height < h:
        rrect.y += 15
    if keypressed[pygame.K_UP] and rrect.y > 0:
        rrect.y -= 15
    if keypressed[pygame.K_RIGHT] and rrect.x + rrect.width < w:
        rrect.x += 15
    if keypressed[pygame.K_LEFT] and rrect.x > 0:
        rrect.x -= 15

    if keypressed[pygame.K_s] and brect.y + brect.height < h:
        brect.y += 15
    if keypressed[pygame.K_w] and brect.y > 0:
        brect.y -= 15
    if keypressed[pygame.K_d] and brect.x + brect.width < w:
        brect.x += 15
    if keypressed[pygame.K_a] and brect.x > 0:
        brect.x -= 15


# ✅ FIXED: return updated health
def handlebullets(rbullets, rrect, bbullets, brect, rhealth, bhealth):
    for bullet in rbullets[:]:
        bullet.x -= 10
        if bullet.x < 0:
            rbullets.remove(bullet)
        elif bullet.colliderect(brect):
            rbullets.remove(bullet)
            bhealth -= 1

    for bullet in bbullets[:]:
        bullet.x += 10
        if bullet.x > w:
            bbullets.remove(bullet)
        elif bullet.colliderect(rrect):
            bbullets.remove(bullet)
            rhealth -= 1

    # ship collision
    if rrect.colliderect(brect):
        rrect.x = w - 100
        rrect.y = h // 2
        brect.x = 50
        brect.y = h // 2
        rhealth -= 1
        bhealth -= 1

    return rhealth, bhealth


def output(rrect, brect, rbullets, bbullets, rhealth, bhealth, winner):
    if Gamestate == "start":
        sc.blit(bck, (0, 0))
        sc.blit(rship1, (100, 100))
        sc.blit(bship1, (w - 200, h - 200))
        text1 = font1.render("This is a two player game", True, "White")
        text2 = font1.render("Red: Arrow keys + Right Shift", True, "Red")
        text3 = font1.render("Blue: WASD + Left Shift", True, "Blue")
        text4 = font1.render("Press SPACE to start", True, "Green")
        sc.blit(text1, (0, h / 3))
        sc.blit(text2, (0, h / 3 + 50))
        sc.blit(text3, (0, h / 3 + 100))
        sc.blit(text4, (0, h / 3 + 150))

    elif Gamestate == "play":
        sc.blit(bck, (0, 0))
        sc.blit(p1, (rrect.x, rrect.y))
        sc.blit(p2, (brect.x, brect.y))

        for i in rbullets:
            pygame.draw.rect(sc, "red", i)
        for a in bbullets:
            pygame.draw.rect(sc, "blue", a)

        rtext = font1.render(f"Health: {rhealth}", True, "Red")
        btext = font1.render(f"Health: {bhealth}", True, "Blue")
        sc.blit(rtext, (w - 200, 20))
        sc.blit(btext, (20, 20))

    elif Gamestate == "end":
        winnertext = font2.render(f"{winner}", True, "White")
        sc.blit(winnertext, (w / 3, h / 2))
        text5 = font1.render("Press SPACE to restart", True, "Light Blue")
        sc.blit(text5, (w / 3, h / 2 + 60))


def m():
    global Gamestate
    rrect = pygame.Rect(w - 100, h // 2, shipw, shiph)
    brect = pygame.Rect(50, h // 2, shipw, shiph)

    rbullets, bbullets = [], []
    rhealth, bhealth = 10, 10
    winner = None

    clock = pygame.time.Clock()

    while True:
        clock.tick(60)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                exit()

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RSHIFT and Gamestate == "play":
                    rbullets.append(pygame.Rect(rrect.x, rrect.y + rrect.height // 2, 20, 10))

                if e.key == pygame.K_LSHIFT and Gamestate == "play":
                    bbullets.append(pygame.Rect(brect.x + brect.width, brect.y + brect.height // 2, 20, 10))

                if e.key == pygame.K_SPACE:
                    if Gamestate in ["start", "end"]:
                        Gamestate = "play"
                        rhealth, bhealth = 10, 10
                        rbullets.clear()
                        bbullets.clear()
                        winner = None

        if Gamestate == "play":
            rhealth, bhealth = handlebullets(
                rbullets, rrect, bbullets, brect, rhealth, bhealth
            )

            if rhealth <= 0:
                winner = "BLUE WINS"
                Gamestate = "end"
            if bhealth <= 0:
                winner = "RED WINS"
                Gamestate = "end"

        output(rrect, brect, rbullets, bbullets, rhealth, bhealth, winner)
        keypressed = pygame.key.get_pressed()
        if Gamestate == "play":
            handleships(rrect, brect, keypressed)

        pygame.display.update()


m()
