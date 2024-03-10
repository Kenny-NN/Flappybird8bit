import pygame
from pygame.locals import *
import random

pygame.init()

clock = pygame.time.Clock()

Vindu_Bredde = 650 
Vindu_Hoyde = 850
vindu = pygame.display.set_mode((Vindu_Bredde, Vindu_Hoyde))
pygame.display.set_caption('Super City')


#Definere spill variabler
bakke_scroll = 0
scroll_speed = 4
fly = False
game_over = False
byggning_gap = 200
byggning_freq = 1500 #millisekunder
siste_byggning = pygame.time.get_ticks() - byggning_freq
score = 0

#Laste inn bilder
bg = pygame.image.load("Bilder_og_Sprite/BGG.png")
bakke_bg = pygame.image.load("Bilder_og_Sprite/BakkeForSpillet.png")
linje_bg = pygame.image.load("Bilder_og_Sprite/Rulle.png")

def restart_spillet():
    byggning_gruppe.empty()
    spiller.rect.x = 50
    spiller.rect.y = int(Vindu_Bredde / 2)
    score = 0
    return score

class Superman():
    def __init__(self, x, y):
        img = pygame.image.load("Bilder_og_Sprite/Supermanflying1.png")
        self.image = pygame.transform.scale(img, (100, 25))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel = 0
        self.hoppe = False
        self.poengteller = False


    def update(self):

        #gravitasjon
        if fly == True:
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.y < 660: 
                self.rect.y += int(self.vel)

        #hoppe funksjon
        key = pygame.key.get_pressed()

        if key[pygame.K_SPACE] and self.hoppe == False and game_over == False:
            self.vel = -10
       
            
        #rotere superman
        if not game_over:
            rotated_image = pygame.transform.rotate(self.image, self.vel * -2)
            self.rect = rotated_image.get_rect(center=self.rect.center)
            vindu.blit(rotated_image, self.rect) 
        else:
            rotated_image = pygame.transform.rotate(self.image, -90)
            vindu.blit(rotated_image, self.rect) 

class Byggning(pygame.sprite.Sprite):
    def __init__(self, x, y, posisjon):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load("Bilder_og_Sprite/Byggning.png")  
        self.image = pygame.transform.scale(img, (100, 450))
        self.rect = self.image.get_rect()
        self.kollisjon = False 
        
        if posisjon == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(byggning_gap / 2)]
        if posisjon == -1:
            self.rect.topleft = [x, y + int(byggning_gap / 2)]
        
    def update(self):
        if not self.kollisjon:  #Hvis det ikke har kollidert så kjører den
            self.rect.x -= scroll_speed

        if self.rect.right < 0:
            self.kill()

class Knapp():
    def __init__(self, x, y):
        img = pygame.image.load("Bilder_og_Sprite/Reset1.png")
        self.image = pygame.transform.scale(img, (100, 50))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
    
    def tegne(self):

        action = False

        #Mus posisjon
        posisjon = pygame.mouse.get_pos()

        #Sjekke om mus er over knappen
        if self.rect.collidepoint(posisjon):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True

        #Tegne knapp
        vindu.blit(self.image, (self.rect.x, self.rect.y))

        return action

byggning_gruppe = pygame.sprite.Group()
spiller = Superman(50, int(Vindu_Bredde / 2))
knapp = Knapp(Vindu_Bredde // 2 - 50, 350)

fortsett = True
while fortsett:
    
    clock.tick(60)

    #Bakgrunn
    vindu.blit(bg, (0,0))

    byggning_gruppe.draw(vindu)
    byggning_gruppe.update()

    #Spiller
    spiller.update()

    #Bakke
    vindu.blit(bakke_bg, (0,750))

    #linje
    vindu.blit(linje_bg, (bakke_scroll, 730))

    #Tegner poeng
    font = pygame.font.SysFont(None, 60)
    score_text = font.render(str(score), True, (255, 255, 255))
    vindu.blit(score_text, (int(Vindu_Bredde/ 2), 20))

    #Sjekker hvis spiller har truffet linje
    if spiller.rect.bottom >= 710:
        game_over = True
        fly = False

        for building in byggning_gruppe:
            building.kollisjon = True   
            
    
    if not game_over:
        #Sjekker kollisjon mellom spiller og hinder
        if pygame.sprite.spritecollide(spiller, byggning_gruppe, False):
            game_over = True

            for building in byggning_gruppe:
                building.kollisjon = True
        
        if len(byggning_gruppe) > 0 and spiller.rect.right > byggning_gruppe.sprites()[0].rect.right:
        #Går opp dersom spilleren ikke har passert byggningen
            if not spiller.poengteller:
                score += 1
                spiller.poengteller = True
        else:
            spiller.poengteller = False

    if game_over == False and fly == True:
        #Generere ny byggning
        tiden_nu = pygame.time.get_ticks()
        if tiden_nu - siste_byggning > byggning_freq:
            byggning_hoyde = random.randint(-100, 100)
            Nederste_byggning = Byggning(Vindu_Bredde, int(Vindu_Hoyde / 2) + byggning_hoyde, -1)
            Oppe_byggning = Byggning(Vindu_Bredde, int(Vindu_Hoyde / 2) + byggning_hoyde, 1)
            byggning_gruppe.add(Nederste_byggning)
            byggning_gruppe.add(Oppe_byggning)
            siste_byggning = tiden_nu

        #Ruller bakken
        bakke_scroll -= scroll_speed
        if abs(bakke_scroll) > 220 :
            bakke_scroll = 0
        
    #Knapp
    if game_over == True:
        if knapp.tegne() == True:
            game_over = False    
            score = restart_spillet()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            fortsett = False
            
        #Sørger for at spillet ikke starter før brukeren har trykket på mellomromtasten
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and fly == False and game_over == False:
                fly = True
        


    pygame.display.update()
    

pygame.quit()