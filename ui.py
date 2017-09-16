# -*- coding: Utf-8 -*
# Written by Nicolas Reszka and Tymothé Laine in 2016

# Importer les librairies
import random
import math
import pygame
from pygame.locals import *
from lib import *
from constants import *

#----------Initialiser le jeu----------

# Initialiser pygame
pygame.init()
clock = pygame.time.Clock()
font = pygame.font.Font(None, 32)

# Configuer la fenetre
windowWidth = 512 # Largeur
windowHeight = 352 # Hauteur
windowSize = [windowWidth, windowHeight] # Taille de la fenetre
window = pygame.display.set_mode(windowSize, HWSURFACE|DOUBLEBUF|RESIZABLE) # Surface qui va être affichée
screen = window.convert() # Surface sur laquelle tout va être dessiné
appSize = windowSize.copy() # Taille de la surface

# Titre de la fenetre
pygame.display.set_caption("Game")

debugMode = False
pause = False

# Tant que le joueur n aura pas quitte le jeu :
running = True
while running :

	defaultSurface = pygame.image.load("sprites/defaultSurface.png").convert_alpha()

	# generation des options
	
	menu = ["Play","option","exit"]
	space = 48
	menuX = 96
	menuY = 96

	# couleurs
	textColor = (0,255,0)
	color = (100,0,0)
	focusColor = (200,0,0)

	# détection du clic

	mouseX = 0
	mouseY = 0
	mouseClick = False

	#creation des rectangle autour des options
	menuBoxes = []
	index = 0
	for option in menu:
		menuBoxes.append(Rect(menuX-16,menuY+space*index-2,128,30))
		index += 1

	position = 0

	ROOM_MENU = True

	# Afficher le menu
	while ROOM_MENU :	
		mouseClick = False

		# Repeter les actions 60 fois par secondes
		clock.tick(60)

		# Parcourir la liste des evenements
		for event in pygame.event.get():

			# Quitter le jeu
			if event.type == pygame.QUIT:
				ROOM_MENU = False
				running = False

			# Récupérer la position de la souris
			if event.type == pygame.MOUSEMOTION:
				mouseX = event.pos[0]*(appSize[0]/windowSize[0])
				mouseY = event.pos[1]*(appSize[1]/windowSize[1])

			# Récupérer le clic de la souris
			if event.type == pygame.MOUSEBUTTONDOWN:
				mouseClick = True

			# Redimensionner la fenetre à l'échelle
			if event.type == pygame.VIDEORESIZE:
				windowSize = event.dict['size']
				window = pygame.display.set_mode(windowSize, HWSURFACE|DOUBLEBUF|RESIZABLE)
				if event.h >= int(event.w*(windowHeight/windowWidth)) :
					appSize = (event.w, int(event.w*(windowHeight/windowWidth)))
				else : 
					appSize = (int(event.h*(windowWidth/windowHeight)), event.h)

			# Verifier si les touches sont pressées
			if event.type == pygame.KEYDOWN:

				# Bouger le personnage
				if event.key == pygame.K_LEFT:
					xMove = -1
				if event.key == pygame.K_RIGHT:
					xMove = 1
				if event.key == pygame.K_UP:
					yMove = -1
				if event.key == pygame.K_DOWN:
					yMove = 1

				# Activer/desactiver le mode debug
				if event.key == pygame.K_KP_MULTIPLY:
					debugMode = not debugMode


			# Verifier si les touches ne sont plus pressées
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT and xMove == -1 or event.key == pygame.K_RIGHT and xMove == 1:
					xMove = 0
				if event.key == pygame.K_UP and yMove == -1 or event.key == pygame.K_DOWN and yMove == 1:
					yMove = 0

		
		# Rafraichir l'écran
		screen.fill((0,0,0))

		# si la souris est sur une option
		index = 0
		mouseInBox = False

		#verification de la position d la souris
		for option in menu:
			
			#verificatin de l'option choisit
			backColor = color
			if menuBoxes[index].collidepoint((mouseX,mouseY)) :
				backColor = focusColor
				position = index
				mouseInBox = True

			pygame.draw.rect(screen, backColor, menuBoxes[index])

			# affichage du nom de l'option
			text = font.render(option, 3, textColor)
			screen.blit(text,(menuX,menuY+space*index))
			index += 1

			
		if mouseClick and mouseInBox:

			# option play
			if position == 0 :
				print("Play")

			# option option
			if position == 1 :
				print("option")

			# option exit
			if position == 2 :
				ROOM_MENU = False
				running = False




		# Afficher la surface de dessin au centre de la fenetre
		window.blit(pygame.transform.scale(screen, appSize).convert(), (windowSize[0]/2-appSize[0]/2,windowSize[1]/2-appSize[1]/2))

		# Mettre à jour l'écrans
		pygame.display.flip()

# Finir le programme
pygame.quit()
