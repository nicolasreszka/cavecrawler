# -*- coding: Utf-8 -*
# Written by Nicolas Reszka and Tymothé Laine in 2016

import random
import math
import pygame
from pygame.locals import *

# Constantes pour les points cardinaux
(N,E,S,W) = (0,1,2,3)

#----------Fonctions pour le jeu----------

# Permet de séparer les frames d'une bande 
def loadSpriteStripe(stripe, cycleLength, y, w, h) :
    sprite = []
    for img in range(cycleLength) :
        sprite.append(stripe.subsurface(img*w,y,w,h).convert_alpha())
    return sprite

# Permet de colorer tout les pixels d'un sprite avec une nouvelle couleur unique
def colorize(image, newColor):
    image = image.copy()
    image.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
    image.fill(newColor[0:3] + (0,), None, pygame.BLEND_RGBA_ADD)
    return image

#----------Fonctions mathématiques----------

# Permet de verouiller une valeur entre deux valeurs
def clamp(n, smallest, largest): 
    return max(smallest, min(n, largest))

# Permet d'approcher progressivement d'une valeur
def approachValues(start, end, shift) :
    if start < end :
        return min(start + shift, end)
    else :
        return max(start - shift, end)

# Permet de récupérer le x d'un point grace à sa distance et son angle
def lengthDirX(length, angle) :
    return math.cos(angle)*length

# Permet de récupérer le y d'un point grace à sa distance et son angle
def lengthDirY(length, angle) :
    return math.sin(angle)*length

# Permet de récuperer l'angle formé par deux points
def pointDirection(a,b) :
    return math.atan2(b[1]-a[1],b[0]-a[0])%(2*math.pi)

# Permet de récuperer la distance entre deux points
def pointDistance(a,b) :
    return math.sqrt((b[1]-a[1])**2+(b[0]-a[0])**2)

#----------Fonctions pour la generation du donjon----------

# Permet d'avoir toutes les possibilites de coordonnees
def listOfCouples(l) :
    coupleList = []
    for y in range(l) :
        for x in range(l) :
            coupleList.append([y,x])
    return coupleList

# Permet de recuperer les coordonnees de la salle adjacente
def adjacentDirection(x, y, d):
    if d == N:
        return (x, y-1)
    if d == E:
        return (x+1, y)
    if d == S:
        return (x, y+1)
    if d == W:
        return (x-1, y)

# Donne la direction opposee
def oppositeDirection(d):
    if d == N: 
    	return S
    if d == E: 
    	return W
    if d == S: 
    	return N
    if d == W: 
    	return E

# def displayMap(self) :
#     s = 64 # Size 
#     t = int(s/16) # Thickness
#     l = s/2 - s/8 # Left
#     r = s/2 + s/8 # Right
#     white  = (255,255,255)
#     blue   = (55 ,150,240)
#     cyan   = (110,230,230)
#     green  = (90 ,235, 60)
#     yellow = (250,230, 30)
#     purple = (230,30 ,235)
#     red    = (235,50 ,105)
#     mauve  = (195,110,230)
#     lime   = (110,230,110)

#     y = 0
#     for row in self.Map :
#         x = 0
#         for cell in row :
#             if cell != 0 :  
#                 # Dessiner les countours

#                 # Au nord
#                 pygame.draw.line(screen, white, [x*s,y*s], [x*s+l,y*s], t)
#                 pygame.draw.line(screen, white, [x*s+r,y*s], [(x+1)*s,y*s], t)
#                 # A l'est
#                 pygame.draw.line(screen, white, [x*s,(y+1)*s], [x*s+l,(y+1)*s], t)
#                 pygame.draw.line(screen, white, [x*s+r,(y+1)*s], [(x+1)*s,(y+1)*s], t)
#                 # Au sud
#                 pygame.draw.line(screen, white, [x*s,y*s], [x*s,y*s+l], t)
#                 pygame.draw.line(screen, white, [x*s,y*s+r], [x*s,(y+1)*s], t)
#                 # A l'ouest
#                 pygame.draw.line(screen, white, [(x+1)*s,y*s], [(x+1)*s,y*s+l], t)
#                 pygame.draw.line(screen, white, [(x+1)*s,y*s+r], [(x+1)*s,(y+1)*s], t)

#                 # Pour chaques directions
#                 for d in range(4) : 

#                     # Si il n'y a pas de sortie ou s'il y a une serrure pour cette direction 
#                     if not d in cell.exits or cell.exitType[d] != "normal" :    
#                         if cell.exitType[d] == "bossLock" :
#                             doorColor = yellow
#                         elif cell.exitType[d] == "itemLock" :
#                             doorColor = purple
#                         elif cell.exitType[d] == "sacrificeDoor" :
#                             doorColor = mauve
#                         elif cell.exitType[d] == "hiddenDoor" :
#                             doorColor = lime
#                         elif cell.exitType[d] == "shopDoor" :
#                             doorColor = cyan
#                         else :
#                             doorColor = white

#                         if d == N:
#                             pygame.draw.line(screen, doorColor, [x*s+l, y*s], [x*s+r, y*s], t)
#                         if d == E:
#                             pygame.draw.line(screen, doorColor, [(x+1)*s, y*s+l], [(x+1)*s, y*s+r], t)
#                         if d == S:
#                             pygame.draw.line(screen, doorColor, [x*s+l, (y+1)*s], [x*s+r, (y+1)*s], t)
#                         if d == W:
#                             pygame.draw.line(screen, doorColor, [x*s, y*s+l], [x*s, y*s+r], t)
                

#                 if cell.roomType == "start" :
#                     text = font.render("Start", 3, green)
#                     screen.blit(text, (x*s+8, y*s+16))

#                 if cell.roomType == "boss" :
#                     text = font.render("Boss", 3, yellow)
#                     screen.blit(text, (x*s+8, y*s+16))

#                 if cell.roomType == "item" :
#                     text = font.render("Item", 3, purple)
#                     screen.blit(text, (x*s+8, y*s+16))

#                 if cell.roomType == "miniBoss" :
#                     text = font.render("Mini", 3, red)
#                     screen.blit(text, (x*s+8, y*s+8))
#                     text = font.render("Boss", 3, red)
#                     screen.blit(text, (x*s+8, y*s+32))

#                 if cell.roomType == "bossKey" :
#                     text = font.render("Boss", 3, blue)
#                     screen.blit(text, (x*s+8, y*s+8))
#                     text = font.render("Key", 3, blue)
#                     screen.blit(text, (x*s+8, y*s+32))

#                 if cell.roomType == "bonus" :
#                     text = font24.render("Bonus", 3, lime)
#                     screen.blit(text, (x*s+8, y*s+16))

#                 if cell.roomType == "sacrifice" :
#                     text = font18.render("Sacrifice", 3, mauve)
#                     screen.blit(text, (x*s+8, y*s+16))

#                 if cell.roomType == "shop" :
#                     text = font.render("Shop", 3, cyan)
#                     screen.blit(text, (x*s+8, y*s+16))
#             x += 1
#         y += 1



