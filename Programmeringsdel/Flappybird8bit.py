import pygame
from pygame.locals import *

hei = 221212121

pygame.init()

Vindu_Bredde = 700
Vindu_Hoyde = 700
vindu = pygame.display.set_mode((Vindu_Bredde, Vindu_Hoyde))
pygame.display.set_caption('Hoppe spill')

clock = pygame.time.Clock()


class Rektangel:
    def __init__(self, x, y, fart, farge, vindusobjekt, bredde, hoyde):
        self.x = x
        self.y = y
        self.fart = fart
        self.farge = farge
        self.vindusobjekt = vindusobjekt
        self.bredde = bredde
        self.hoyde = hoyde
        self.Hoppe = False
        self.Y_gravity = 1
        self.Hoppe_Hoyde = 20
        self.Y_velocity = self.Hoppe_Hoyde

    def tegn(self):
        pygame.draw.rect(self.vindusobjekt, self.farge, (self.x, self.y, self.bredde, self.hoyde))


    def hopp(self):
        if self.Hoppe:
            self.y -= self.Y_velocity
            self.Y_velocity -= self.Y_gravity
            if self.y > 500:
                self.Hoppe = False
                self.y = 500
                self.Y_velocity = self.Hoppe_Hoyde

    def update(self):
        key = pygame.key.get_pressed()

        if key[pygame.K_SPACE]:
            self.Hoppe = True

        if key[pygame.K_LEFT]:
            self.x -= self.fart
        if key[pygame.K_RIGHT]:
            self.x += self.fart


        self.hopp()


spiller = Rektangel(325, 500, 5, (255, 255, 255), vindu, 50, 50)
Bakke = Rektangel(0, 550, 5, (0, 0, 0), vindu, 700, 500)

fortsett = True
while fortsett:
    vindu.fill((0, 0, 255))

    spiller.tegn()
    spiller.update()

    Bakke.tegn()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            fortsett = False

    pygame.display.update()
    clock.tick(60)

pygame.quit()