# Vul hier de namen van je duo in (of enkel je eigen naam als je alleen werkt)
# Naam 1: Zara Baltaci
# Naam 2: Jaimy van Wieringen

# Imports
import random # importeert de random module voor het gooien van een dobbelsteen
import pygame # importeert de pygame module voor het maken van een GUI

# --------------- Globale variabelen ---------------

pion_posities = [0, 0] #pion posities (index is speler nummer, waarde is vakje nummer)

#wie is er aan de beurt? (0 is speler 0, 1 is speler 1)
beurt = 0 
oude_beurt = 0 #voor bijhouden van vorige beurt

#is er een winnaar? (none als er geen winnar is, anders 0 of 1)
winnaar = None

#dobbelsteen worp waarde (0 als er nog niet is gegooid)
worp = 0
dobbelsteen1 = 0
dobbelsteen2 = 0

#coördinaten van de vakjes op het bord
vakjes = [[160, 683], [286, 683], [356, 683], [415, 683], [482, 683], [545, 683],

[618, 683], [692, 683], [758, 683], [828, 643], [895, 598], [937, 549], [965, 489],

[982, 430], [982, 353], [968, 283], [944, 220], [905, 167], [833, 111], [744, 66],

[664, 62], [597, 62], [536, 62], [464, 62], [398, 62], [335, 62], [265, 66], [198, 94],

[142, 129], [104, 174], [83, 227], [65, 283], [65, 367], [83, 435], [116, 491], [160, 535],

[216, 570], [282, 587], [342, 587], [405, 587], [468, 587], [536, 587], [615, 587],

[692, 587], [755, 578], [816, 528], [863, 458], [877, 402], [874, 335], [856, 283],

[804, 202], [737, 160], [632, 157], [545, 157], [468, 157], [394, 157], [328, 157],

[265, 167], [195, 223], [167, 325], [188, 403], [221, 454], [282, 482], [413, 456]]

speciale_tekst = "" #tekst voor op het scherm voor speciale regels

bord_afbeelding = pygame.image.load("Ganzenbord.png") #afbeelding van ganzenbord laden

# ---------- Pygame Initialisatie ----------
pygame.init()

dobbelsteen_afbeeldingen = [
    pygame.image.load("dice1.png"),
    pygame.image.load("dice2.png"),
    pygame.image.load("dice3.png"),
    pygame.image.load("dice4.png"),
    pygame.image.load("dice5.png"),
    pygame.image.load("dice6.png")
]

window_size = [1200, 800] #afmetingen van het spelscherm instellen
screen = pygame.display.set_mode(window_size) #spelscherm maken met de juiste afmetingen in "screen"

pygame.display.set_caption("Ganzenbord") #titel spelscherm instellen

done = False #laat spel oneindig doorlopen tot er op het kruisje word geklikt

# --------------- Functies ---------------
def beurt_doorgeven(beurt): #functie: beurt doorgeven naar volgende speler
    if beurt == 1: #als huidige beurt 1 is
        beurt = 0 #geeft de beurt aan speler 0
    else: #anders(als de huidige beurt 0 is)
        beurt = 1 #geeft de beurt aan speler 1
    return beurt #geeft de nieuwe beurt terug                  


def beweeg_pion(speler, aantal_stappen): #functie: pion verplaatsen
    global pion_posities 
    turn_around = False #variabele om bij te houden of we moeten teruglopen
    for stap in range(0, aantal_stappen): #herhaal voor elk stapje dat we moeten zetten
        #als we niet op de laatste vakjes zijn en niet moeten teruglopen
        if pion_posities[speler] < len(vakjes) -1 and not turn_around: 
            pion_posities[speler] += 1 #beweeg pion 1 vakje vooruit
        else: #anders, als we moeten teruglopen
            turn_around = True #zet de variabele om terug te lopen op True

        if turn_around: #als we moeten teruglopen
            pion_posities[speler] -= 1 #beweeg pion 1 vakje achteruit

        update_screen("bewegend") #tekent het scherm opnieuw tijdens de beweging

def update_screen(situatie): #functie: scherm updaten
    screen.fill((255, 255, 255)) #witte achtergrond
    #update het scherm met de nieuwe inhoud

    bord_rect = bord_afbeelding.get_rect() #vraagt afmeting van bordplaatje
    screen.blit(bord_afbeelding, bord_rect) #teken het bord bij volgende update van scherm

    #update het scherm met pionnen
    speler0_x = vakjes[pion_posities[0]][0] #x coordinaat van speler 0
    speler0_y = vakjes[pion_posities[0]][1] #y coordinaat van speler 0
    kleur_speler0 = (255, 0, 0) #kleur van speler 0 (rood)
    pygame.draw.circle(screen, kleur_speler0, (speler0_x, speler0_y), 10) #tekent pion van speler 0
    speler1_x = vakjes[pion_posities[1]][0] +5 #x coordinaat van speler 1
    speler1_y = vakjes[pion_posities[1]][1] +5 #y coordinaat van speler 1
    kleur_speler1 = (0, 0, 255) #kleur van speler 1 (blauw)
    pygame.draw.circle(screen, kleur_speler1, (speler1_x, speler1_y), 10) #tekent pion van speler 1 

    myfont = pygame.font.SysFont(None, 30) #maakt een font object aan voor de tekst

    if situatie == "bewegend": #tijdens bewegen laten we de huidige beurt zien
        beurt_display = beurt
    else: #anders de vorige beurt (na het bewegen)
        beurt_display = oude_beurt

    if pion_posities == [0, 0]: #als het spel nog moet beginnen
        tekst = "druk op spatie om speler 1 te laten beginnen"
        label = myfont.render(tekst, 1, (0, 0, 0))
        screen.blit(label, (330, 470))

    elif winnaar == None: #tijdens het spel
        
        dobbelsteen_img1 = dobbelsteen_afbeeldingen[dobbelsteen1 - 1]
        dobbelsteen_img2 = dobbelsteen_afbeeldingen[dobbelsteen2 - 1]
        screen.blit(dobbelsteen_img1, (500, 300))  # eerste dobbelsteen
        screen.blit(dobbelsteen_img2, (580, 300))  # tweede dobbelsteen

        #tekent de laatste worp op het scherm
        tekst = "speler" + str(beurt_display + 1) + " gooide: " + str(worp)
        label = myfont.render(tekst, 1, (0, 0, 0))
        screen.blit(label, (400, 470))

        #tekent wie er aan de beurt is op het scherm
        tekst = "speler" + str(beurt + 1) + " is aan de beurt "
        label = myfont.render(tekst, 1, (0, 0, 0))
        screen.blit(label, (400, 495))

        #tekent de regel die net is uitgevoerd op het scherm
        label = myfont.render(speciale_tekst, 1, (0, 0, 0))
        screen.blit(label, (250, 260))

    else: #einde van het spel
        tekst = "speler" + str(winnaar + 1) + " heeft gewonnen! "
        label = myfont.render(tekst, 1, (0, 0, 0))
        screen.blit(label, (370, 470))
        tekst = "druk op backspace voor een rematch!"
        label = myfont.render(tekst, 1, (0, 0, 0))
        screen.blit(label, (370, 495))


    pygame.display.flip() #ververst beeldscherm met nieuwe graphics
    pygame.time.wait(120) #wacht 120 ms voor animatie-effect

# --------------- Hoofdloop van het spel ---------------
while not done:


    for event in pygame.event.get(): #loop door alle gebeurtenissen die pygame heeft geregistreerd
       if event.type == pygame.QUIT: #als er op het kruisje is geklikt
          done = True #zet done op True, zodat we de hoofdloop kunnen verlaten
       elif event.type == pygame.KEYDOWN: #als er een toets is ingedrukt
            if event.key == pygame.K_SPACE and winnaar == None: #spatie ingedrukt en geen winnaar
                print("spatiebalk ingedrukt - hier komt dobbelsteenworp en pionverplaatsing")

                speciale_tekst = "" #reset speciale tekst
 
                dobbelsteen1 = random.randint(1, 6) 
                dobbelsteen2 = random.randint(1, 6) #tweede dobbelsteen dus worp (1-12)
                worp = dobbelsteen1 + dobbelsteen2

                beweeg_pion(beurt, worp) #verplaatst de pion van de speler die aan de beurt is

                vak = pion_posities[speler]

                if vak == [545, 683]:
                    pion_posities[speler] = [937, 549]
                    speciale_tekst = "Beland op vak 6, je mag naar vak 12!"

                elif vak == [536, 587]:
                    pion_posities[speler] = [104, 174]
                    speciale_tekst = "Beland op vak 42, helaas, terug naar vak 30."

                elif vak == [737, 160]:
                    speciale_tekst = "Beland op vak 52, je zit in de gevangenis dus je beurt wordt overgeslagen."
                    beurt = beurt_doorgeven(beurt)

                if pion_posities[beurt] == 63: #als de speler op vakje 63 komt
                    winnaar = beurt #deze speler is de winnaar
                elif vak in [[944, 220], [142, 129], [877, 402], [83, 435]]:
                    speciale_tekst = "Beland op gansvakje, je mag nog een keer gooien!"
                    oude_beurt = beurt
                else: #als de speler niet op vakje 63 komt
                    oude_beurt = beurt #slaat de huidige beurt op als oude_beurt
                    beurt = beurt_doorgeven(beurt) #geeft de beurt aan de volgende speler

            elif event.key == pygame.K_BACKSPACE:
                print("backspace ingedrukt - reset het spel")
                pion_posities = [0, 0] #zet pion positie terug naar start
                beurt = 0 #zet de beurt terug naar speler 0
                oude_beurt = 0 #zet oude_beurt terug naar speler 0
                winnaar = None #zet winnaar terug naar None
                worp = 0 #zet worp terug naar 0


    update_screen("normaal") #update het scherm na elke actie


# --------------- Afsluiten van Pygame ---------------
pygame.quit() # sluit Pygame en het spel netjes af