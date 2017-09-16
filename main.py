# -*- coding: Utf-8 -*
# Written by Nicolas Reszka and Tymothé Laine in 2016

# Importer les librairies
import random
import math
import pygame
from pygame.locals import *
from lib import *
from constants import *

#----------Le joueur----------		

class Player :
	def __init__(self, x, y) :
		self.objectType = "player"
		self.x = x
		self.y = y
		self.originX = 0
		self.originY = 16
		self.speed = 4
		self.bbox = pygame.Rect(self.x, self.y, 32, 16) 
		self.direction = 2
		self.imageIndex = 0
		self.imageSpeed = 0.1
		self.attacking = False
		self.maxHealth = 6
		self.health = self.maxHealth
		self.hit = False
		self.invincibilityFrames = 0

	def update(self) :
		# Récuperer les variables globales pour pouvoir les modifier
		global transition, transitionDirection
		global roomX, roomY, xCell, yCell 
		global keyAttack, keyItem, keyBomb
		global bigKey, smallKey, playerDamage, playerBow, playerArrows, playerBombs, playerMoney
		global playerX, playerY

		# Mourir
		if self.health <= 0 :
			instances.remove(self)
			global gameOver 
			gameOver = True
			return

		# Frames d'invincibilité
		if self.hit :
			self.invincibilityFrames -= 1
			if self.invincibilityFrames <= 0 :
				self.hit = False

		arrowCheck = False

		if not transition :

			# Réuperer les objets
			for obj in instances :
				# Ouvrir les portes
				if obj.objectType == "bossLock" and bigKey > 0 :
					if self.bbox.colliderect(obj.bbox) :
						instances.remove(obj)
						bigKey -= 1
				if obj.objectType == "itemLock" and smallKey > 0 :
					if self.bbox.colliderect(obj.bbox) :
						instances.remove(obj)
				# Récuperer les clés
				if obj.objectType == "bigKey" :
					if self.bbox.colliderect(obj.bbox) :
						instances.remove(obj)
						bigKey += 1
						aKey.play()
				if obj.objectType == "smallKey" :
					if self.bbox.colliderect(obj.bbox) :
						instances.remove(obj)
						smallKey += 1
						aKey.play()
				# Récuperer les items
				if obj.objectType == "bow" :
					if self.bbox.colliderect(obj.bbox) :
						instances.remove(obj)
						playerBow = True
						playerArrows += 4
				if obj.objectType == "arrowItem" :
					arrowCheck = True
					if self.bbox.colliderect(obj.bbox) :
						instances.remove(obj)
						playerArrows += 1
				if obj.objectType == "heartItem" :
					if self.bbox.colliderect(obj.bbox) :
						instances.remove(obj)
						self.health = approachValues(self.health, self.maxHealth, 2)
						aHeart.play()
				if obj.objectType == "bigHeartItem" :
					if self.bbox.colliderect(obj.bbox) :
						instances.remove(obj)
						self.maxHealth += 2
						self.health = self.maxHealth 
						aBigHeart.play()
				if obj.objectType == "bombItem" :
					if self.bbox.colliderect(obj.bbox) :
						instances.remove(obj)
						playerBombs += 1
				if obj.objectType == "swordItem" :
					if self.bbox.colliderect(obj.bbox) :
						instances.remove(obj)
						playerDamage += 1
				if obj.objectType == "coinItem" :
					if self.bbox.colliderect(obj.bbox) :
						instances.remove(obj)
						playerMoney += 1
				if obj.objectType == "staircase" :
					if self.bbox.colliderect(obj.bbox) :
						global ROOM_GAME, ROOM_CREDIT
						ROOM_GAME = False
						ROOM_CREDIT = True


			if not self.attacking :
				# Vérifier si la touche est pressée pour l'axe x
				if xMove != 0 :
					# Bouger le personnage et la boite de collision
					self.x += self.speed * xMove
					self.bbox.x = self.x
					for obj in instances :
						# Verifier si l'instance est un objet solide
						solidCheck = obj.objectType == "wall" or obj.objectType == "block" or obj.objectType == "eyeBlock"
						doorCheck = (obj.objectType == "bossLock" and bigKey == 0) or (obj.objectType == "itemLock" and smallKey == 0)
						if solidCheck or doorCheck or obj.objectType == "doorLock" or (obj.objectType == "spikes" and not obj.open) :
							if self.bbox.colliderect(obj.bbox) :
								# Replacer le carre de collision au bord du mur
								if xMove > 0 :
									self.bbox.right = obj.bbox.left
								if xMove < 0 :
									self.bbox.left = obj.bbox.right
								# Replacer le joueur sur sa collision
								self.x = self.bbox.x

				# De même pour l'axe y
				if yMove != 0 :
					self.y += self.speed * yMove
					self.bbox.y = self.y
					for obj in instances :
						solidCheck = obj.objectType == "wall" or obj.objectType == "block" or obj.objectType == "eyeBlock"
						doorCheck = (obj.objectType == "bossLock" and bigKey == 0) or (obj.objectType == "itemLock" and smallKey == 0)
						if solidCheck or doorCheck or obj.objectType == "doorLock" or (obj.objectType == "spikes" and not obj.open) :
							if self.bbox.colliderect(obj.bbox) :
								if yMove > 0 :
									self.bbox.bottom = obj.bbox.top
								if yMove < 0 :
									self.bbox.top = obj.bbox.bottom
								self.y = self.bbox.y

				# Choisir la direction 
				if xMove > 0 :
					self.direction = E
				elif xMove < 0 :
					self.direction = W
				elif yMove > 0 :
					self.direction = S
				elif yMove < 0 :
					self.direction = N

				# Attaquer
				if keyAttack :
					self.attacking = True
					self.imageIndex = 0
					self.imageSpeed = 0.2
					keyAttack = False
					if self.direction == W :
						self.originX = 28
					elif self.direction == N :
						self.originY = 48
					aSword.play()

				# Utiliser l'arc
				if keyItem and playerBow and playerArrows > 0:
					keyItem = False
					if self.direction == N:
						instances.append(Arrow(self.x,self.y-48,self.direction))
					if self.direction == E:
						instances.append(Arrow(self.x+32,self.y-8,self.direction))
					if self.direction == S:
						instances.append(Arrow(self.x,self.y+16,self.direction))
					if self.direction == W:
						instances.append(Arrow(self.x-32,self.y-8,self.direction))
					playerArrows -= 1
					aBow.play()

				if playerArrows == 0 and playerBow :
					if dungeon.Map[yCell][xCell].roomType == "boss" and not dungeon.Map[yCell][xCell].cleared :
						if not arrowCheck and dungeon.Map[yCell][xCell].enemyCounter == 1:
							instances.append(Spider(roomX+192,roomY+96))
							instances.append(Spider(roomX+288,roomY+96))
							dungeon.Map[yCell][xCell].enemyCounter += 2
					if dungeon.Map[yCell][xCell].roomType == "bossKey" and switches > 0 and dungeon.Map[yCell][xCell].cleared :
						if self.x in range(roomX+64, roomX+448) and self.y in range(roomY+64,roomY+288) :
							if not arrowCheck :
								instances.append(Spider(roomX+192,roomY+96))
								instances.append(Spider(roomX+288,roomY+96))
								dungeon.Map[yCell][xCell].enemyCounter += 2
								dungeon.Map[yCell][xCell].cleared = False
								for d in range(4) : 
									if d == N:
										dx = roomX+224
										dy = roomY
									if d == E:
										dx = roomX+448
										dy = roomY+144
									if d == S:
										dx = roomX+224
										dy = roomY+288
									if d == W:
										dx = roomX
										dy = roomY+144

									if d in dungeon.Map[yCell][xCell].exits :
										instances.append(DoorLock(dx,dy,d))

				# Poser une bombe
				if keyBomb and playerBombs > 0:
					keyBomb = False
					instances.append(Bomb(self.x,self.y-16))
					playerBombs -= 1

			else :
				# Créer la zone de contact de l'épée
				if self.direction == N:
					enemyCheck = pygame.Rect(self.x, self.y-48, 32, 48) 
				if self.direction == E:
					enemyCheck = pygame.Rect(self.x+32, self.y-16, 32, 32) 
				if self.direction == S:
					enemyCheck = pygame.Rect(self.x, self.y+16, 32, 32) 
				if self.direction == W:
					enemyCheck = pygame.Rect(self.x-32, self.y-16, 32, 32)

				# Vérifier si l'épée à touchée un ennemi
				for obj in instances :
					if obj.objectType == "enemy" :
						# Affliger les dégats à l'ennemi
						if enemyCheck.colliderect(obj.bbox) :
							if not obj.hit :
								obj.health -= playerDamage
								obj.invincibilityFrames = 30
								obj.hit = True

				# Dessiner la zone de contact de l'épée
				if debugMode :
					pygame.draw.rect(screen, (250,45,45), (enemyCheck.x-camera.x,enemyCheck.y-camera.y,enemyCheck.w,enemyCheck.h))

			# Effectuer une transition lorsque le joueur sort de la salle
			if self.x < roomX :
				transition = True
				transitionDirection = W # A l'Ouest
				xCell -= 1 
				roomX -= windowWidth
				self.x = roomX+windowWidth-96
				self.bbox.x = self.x
			elif self.y < roomY :
				transition = True
				transitionDirection = N # Au Nord
				yCell -= 1
				roomY -= windowHeight
				self.y = roomY+windowHeight-80
				self.bbox.y = self.y
			elif self.x > roomX+windowWidth :
				transition = True
				transitionDirection = E # A l'Est
				xCell += 1
				roomX += windowWidth
				self.x = roomX+64
				self.bbox.x = self.x
			elif self.y > roomY+windowHeight :
				transition = True
				transitionDirection = S # Au Sud
				yCell += 1
				roomY += windowHeight
				self.y = roomY+64
				self.bbox.y = self.y
		else :
			# Bouger la camera dans la direction
			if transitionDirection == N or transitionDirection == S :
				camera.y = approachValues(camera.y, roomY, 24)
			elif transitionDirection == E or transitionDirection == W :
				camera.x = approachValues(camera.x, roomX, 24)

			# Lorsque la camera est arrivée au point arreter la transition
			if camera.x == roomX and camera.y == roomY :
				transition = False

				# Mettre à jour la grille de pathfinding
				aStar.createGrid()

				if not dungeon.Map[yCell][xCell].cleared :
					# Faire spawner les ennemis
					if dungeon.Map[yCell][xCell].roomType == "" :
						spawnList = getSpawnPoints(dungeon.Map[yCell][xCell].structure)
						dungeon.Map[yCell][xCell].enemyCounter = 0
						for spawn in spawnList :
							if dungeon.Map[yCell][xCell].mobs == "enemy" :
								instances.append(Enemy(roomX+spawn[0],roomY+spawn[1]))
								dungeon.Map[yCell][xCell].enemyCounter += 1
					elif dungeon.Map[yCell][xCell].roomType == "bossKey" :
						instances.append(Spider(roomX+192,roomY+96))
						instances.append(Spider(roomX+288,roomY+96))
						dungeon.Map[yCell][xCell].enemyCounter = 2
					# Faire spawner les boss
					elif dungeon.Map[yCell][xCell].roomType == "miniBoss" :
						instances.append(MiniBoss(roomX+240,roomY+160))
						dungeon.Map[yCell][xCell].enemyCounter = 1
					elif dungeon.Map[yCell][xCell].roomType == "boss" :
						instances.append(Boss(roomX+240,roomY+160))
						dungeon.Map[yCell][xCell].enemyCounter = 1

					# Fermer les portes de la salle
					for d in range(4) : 
						if d == N:
							dx = roomX+224
							dy = roomY
						if d == E:
							dx = roomX+448
							dy = roomY+144
						if d == S:
							dx = roomX+224
							dy = roomY+288
						if d == W:
							dx = roomX
							dy = roomY+144

						if d in dungeon.Map[yCell][xCell].exits :
							instances.append(DoorLock(dx,dy,d))
		
		# Choisir le sprite 
		if self.attacking :
			self.sprite = sPlayerAttack
		elif xMove != 0 or yMove != 0 :
			self.sprite = sPlayerMove # Si le joueur est en mouvement 
		else :
			self.sprite = sPlayerIdle # Si le joueur ne bouge pas
		
		# Animer le sprite
		self.imageIndex += self.imageSpeed
		if self.imageIndex > len(self.sprite[self.direction])-1 :
			self.imageIndex = 0
			if self.attacking :
				self.attacking = False
				self.imageSpeed = 0.1
				self.originX = 0
				self.originY = 16
				self.sprite = sPlayerIdle

		# Dessiner le sprite a l'ecran
		if self.hit :
			screen.blit(colorize(self.sprite[self.direction][round(self.imageIndex)], (255,0,0)), (self.x-camera.x-self.originX,self.y-camera.y-self.originY))
		else :
			screen.blit(self.sprite[self.direction][round(self.imageIndex)], (self.x-camera.x-self.originX,self.y-camera.y-self.originY))

		# Dessiner la boite de collision
		if debugMode :
			pygame.draw.rect(screen, (125,230,150), (self.bbox.x-camera.x,self.bbox.y-camera.y,32,16))

		# Dessiner les coeurs pleins
		heart = 0
		for i in range(self.health//2) :
			screen.blit(sHeartUI[0], (18+i*20,18))
			heart += 1 

		# Dessiner les moitiés de coeurs
		if self.health % 2 > 0 :
			screen.blit(sHeartUI[1], (18+heart*20,18))
			heart += 1

		# Dessiner les coeurs vides
		for i in range(math.floor(self.maxHealth/2 - self.health/2)) :
			screen.blit(sHeartUI[2], (18+heart*20,18))
			heart += 1


		moneyCount = font16.render(str(playerMoney), 0, (255,255,255))
		screen.blit(sCoinUI, (18,48))
		screen.blit(moneyCount, (48,48))

		bombCount = font16.render(str(playerBombs), 0, (255,255,255))
		screen.blit(sBombUI, (18,72))
		screen.blit(bombCount, (48,72))

		arrowCount = font16.render(str(playerArrows), 0, (255,255,255))
		screen.blit(sArrowUI, (18,96))
		screen.blit(arrowCount, (48,96))

		damageCount = font16.render(str(playerDamage), 0, (255,255,255))
		screen.blit(sSwordUI, (18,120))
		screen.blit(damageCount, (48,120))

		playerX, playerY = self.x, self.y

#----------Le marchand fantome----------	

class Shop :
	def __init__(self, x, y) :
		self.objectType = "wall"
		self.x = x
		self.y = y		
		self.bbox = pygame.Rect(x, y, 32, 32)

		# Boites de collision des objets
		self.heart = pygame.Rect(x-64, y+64, 32, 32)
		self.bomb = pygame.Rect(x, y+64, 32, 32)
		self.arrow = pygame.Rect(x+64, y+64, 32, 32)

		self.sprite = sShopKeeper
		self.imageIndex = 0
		self.imageSpeed = 0.05

		self.buying = False
		self.buyAlarm = 0

		# le prix des objects
		self.hPrice = 3 #Coeur
		self.bPrice = 7 #Bombe
		self.aPrice = 5 #Fleches

	def update(self) :
		global playerArrows, playerBombs, playerMoney

		# Acheter les objets
		if not self.buying :
			for obj in instances :
				if obj.objectType == "player" :
					if self.heart.colliderect(obj.bbox) and playerMoney >= self.hPrice:
						if obj.health < obj.maxHealth :
							obj.health = approachValues(obj.health, obj.maxHealth, 2)
							playerMoney -= self.hPrice
							self.buying = True
							self.buyAlarm = 60
					if self.bomb.colliderect(obj.bbox) and playerMoney >= self.bPrice :
						playerBombs += 1
						playerMoney -= self.bPrice
						self.buying = True
						self.buyAlarm = 60
					if self.arrow.colliderect(obj.bbox) and playerMoney >= self.aPrice :
						playerArrows += 5
						playerMoney -= self.aPrice
						self.buying = True
						self.buyAlarm = 60
		else :
			self.buyAlarm -= 1
			if self.buyAlarm <= 0 :
				self.buying = False

		# Animer le sprite
		self.imageIndex += self.imageSpeed
		if self.imageIndex > len(self.sprite)-1 :
			self.imageIndex = 0

		# Dessiner les sprites
		screen.blit(self.sprite[round(self.imageIndex)], (self.x-camera.x,self.y-camera.y)) #le marchand
		screen.blit(sHeart, (self.x-camera.x-64,self.y-camera.y+64)) #Le coeur
		screen.blit(sBomb[0], (self.x-camera.x,self.y-camera.y+64)) #la bombe
		screen.blit(sArrow[0], (self.x-camera.x+64,self.y-camera.y+64)) #la fleche
		arrows = font16.render("5", 0, (255,255,255))
		screen.blit(arrows, (self.x-camera.x+86,self.y-camera.y+84)) #le nombre de fleches vendues

		# Dessiner les prix
		heartPrice = font16.render(str(self.hPrice), 0, (255,255,255))
		bombPrice = font16.render(str(self.bPrice), 0, (255,255,255))
		arrowPrice = font16.render(str(self.aPrice), 0, (255,255,255))
		screen.blit(heartPrice, (self.x-camera.x-48,self.y-camera.y+100))
		screen.blit(bombPrice, (self.x-camera.x+8,self.y-camera.y+100))
		screen.blit(arrowPrice, (self.x-camera.x+64,self.y-camera.y+100))


#----------Les ennemis----------		

class Enemy :
	def __init__(self, x, y) :
		self.objectType = "enemy"
		self.x = x
		self.y = y
		self.speed = 2
		self.bbox = pygame.Rect(self.x, self.y, 32, 16) 
		self.direction = 2
		self.sprite = sEnemy
		self.imageIndex = 0
		self.imageSpeed = 0.1
		self.health = 2
		self.hit = False
		self.invincibilityFrames = 0
		self.awake = False

	def update(self) :
		if not self.awake and pointDistance((self.x,self.y), (playerX,playerY)) < 144:
			self.awake = True

		for obj in instances :
			if obj.objectType == "player" :
				if self.bbox.colliderect(obj.bbox) :
					if not obj.hit:
						obj.health -= 1
						obj.invincibilityFrames = 30
						obj.hit = True

		if self.hit :
			self.invincibilityFrames -= 1
			if self.invincibilityFrames <= 0 :
				self.hit = False

		# Mourir
		if self.health <= 0 :
			# Lacher un item
			choice = random.randint(0,12)
			if choice == 7 :
				instances.append(BombItem(self.x,self.y))
			elif choice%3 == 0 :
				instances.append(CoinItem(self.x,self.y))
			elif choice == 2 :
				instances.append(HeartItem(self.x,self.y))
			instances.remove(self)
			dungeon.Map[yCell][xCell].enemyCounter -= 1
			return

		path = []
		targetX, targetY = 0, 0

		# Trouver le chemin vers le joueur
		path = aStar.findPath((self.x,self.y), (playerX,playerY))
		
		if path and self.awake and not self.hit:
			# Suivre le chemin
			targetX = roomX + 64 + (path[len(path)-1][0] * 32)
			targetY = roomY + 64 + (path[len(path)-1][1] * 32)

			# Choisir la direction 
			if targetX > self.x :
				self.direction = E
			elif targetX < self.x :
				self.direction = W
			elif targetY > self.y :
				self.direction = S
			elif targetY < self.y :
				self.direction = N

			self.x = approachValues(self.x,targetX,self.speed)
			self.y = approachValues(self.y,targetY,self.speed)
			self.bbox.x, self.bbox.y = self.x, self.y
			aStar.createGrid()
			
			
		# Animer le sprite
		self.imageIndex += self.imageSpeed
		if self.imageIndex > len(self.sprite[self.direction])-1 :
			self.imageIndex = 0

		# Dessiner le sprite a l'ecran
		if self.hit :
			screen.blit(colorize(self.sprite[self.direction][round(self.imageIndex)], (255,0,0)), (self.x-camera.x,self.y-camera.y-16))
		else :
			screen.blit(self.sprite[self.direction][round(self.imageIndex)], (self.x-camera.x,self.y-camera.y-16))

		# Dessiner la hitbox
		if debugMode :
			pygame.draw.rect(screen, (125,230,150), (self.x-camera.x,self.y-camera.y,32,16))

			# Dessiner le chemin
			if path :
				for node in path :
					pygame.draw.rect(screen, (200,250,70), (64+(node[0]*32),64+(node[1]*32),32,32))

class Spider :
	def __init__(self, x, y) :
		self.objectType = "enemy"
		self.x = x
		self.y = y
		self.speed = 2
		self.bbox = pygame.Rect(self.x, self.y, 32, 16) 
		self.sprite = sSpider
		self.imageIndex = 0
		self.imageSpeed = 0.1
		self.health = 1
		self.hit = False
		self.invincibilityFrames = 0

	def update(self) :
		for obj in instances :
			if obj.objectType == "player" :
				if self.bbox.colliderect(obj.bbox) :
					if not obj.hit:
						obj.health -= 1
						obj.invincibilityFrames = 30
						obj.hit = True

		if self.hit :
			self.invincibilityFrames -= 1
			if self.invincibilityFrames <= 0 :
				self.hit = False

		if self.health <= 0 :
			instances.remove(self)
			dungeon.Map[yCell][xCell].enemyCounter -= 1
			instances.append(ArrowItem(self.x,self.y))
			return

		path = []
		targetX, targetY = 0, 0

		# Trouver le chemin vers le joueur
		path = aStar.findPath((self.x,self.y), (playerX,playerY))
		
		if path and not self.hit:
			# Suivre le chemin
			targetX = roomX + 64 + (path[len(path)-1][0] * 32)
			targetY = roomY + 64 + (path[len(path)-1][1] * 32)

			self.x = approachValues(self.x,targetX,self.speed)
			self.y = approachValues(self.y,targetY,self.speed)
			self.bbox.x, self.bbox.y = self.x, self.y
			aStar.createGrid()
			
		# Animer le sprite
		self.imageIndex += self.imageSpeed
		if self.imageIndex > len(self.sprite)-1 :
			self.imageIndex = 0

		# Dessiner le sprite a l'ecran
		screen.blit(self.sprite[round(self.imageIndex)], (self.x-camera.x,self.y-camera.y-16))

		if debugMode :
			pygame.draw.rect(screen, (125,230,150), (self.x-camera.x,self.y-camera.y,32,16))

			# Dessiner le chemin
			if path :
				for node in path :
					pygame.draw.rect(screen, (200,250,70), (64+(node[0]*32),64+(node[1]*32),32,32))

class MiniBoss :
	def __init__(self, x, y) :
		self.objectType = "enemy"
		self.x = x
		self.y = y
		self.speed = 3
		self.bbox = pygame.Rect(self.x, self.y, 32, 16) 
		self.direction = 0
		self.sprite = sMiniBoss
		self.imageIndex = 0
		self.imageSpeed = 0.1
		self.health = 6
		self.hit = False
		self.invincibilityFrames = 0
		self.awake = False

	def update(self) :
		playerAngle = pointDirection((self.x+16,self.y),(playerX+16,playerY))

		if not self.awake and pointDistance((self.x,self.y), (playerX,playerY)) < 128:
			self.awake = True

		for obj in instances :
			if obj.objectType == "player" :
				if self.bbox.colliderect(obj.bbox) :
					if not obj.hit:
						obj.health -= 1
						obj.invincibilityFrames = 30
						obj.hit = True

		if self.hit :
			self.invincibilityFrames -= 2
			if self.invincibilityFrames <= 0 :
				self.hit = False
				
		if self.health <= 0 :
			instances.append(SmallKey(self.x,self.y))
			instances.remove(self)
			dungeon.Map[yCell][xCell].enemyCounter -= 1
			return

		path = []
		targetX, targetY = 0, 0

		# Trouver le chemin vers le joueur
		path = aStar.findPath((self.x,self.y), (playerX,playerY))
		
		if path and self.awake and not self.hit:
			# Suivre le chemin
			targetX = roomX + 64 + (path[len(path)-1][0] * 32)
			targetY = roomY + 64 + (path[len(path)-1][1] * 32)

			# Choisir la direction 
			if targetY < self.y :
				self.direction = 1
			elif targetY > self.y :
				self.direction = 0

			self.x = approachValues(self.x,targetX,self.speed)
			self.y = approachValues(self.y,targetY,self.speed)
			self.bbox.x, self.bbox.y = self.x, self.y
			aStar.createGrid()
			
		# Animer le sprite
		self.imageIndex += self.imageSpeed
		if self.imageIndex > len(self.sprite[self.direction])-1 :
			self.imageIndex = 0

		# Dessiner le sprite a l'ecran
		if self.hit :
			screen.blit(colorize(self.sprite[self.direction][round(self.imageIndex)], (255,0,0)), (self.x-camera.x,self.y-camera.y-16))
		else :
			screen.blit(self.sprite[self.direction][round(self.imageIndex)], (self.x-camera.x,self.y-camera.y-16))

		# Dessiner la hitbox
		if debugMode :
			pygame.draw.rect(screen, (125,230,150), (self.x-camera.x,self.y-camera.y,32,16))

			# Dessiner le chemin
			if path :
				for node in path :
					pygame.draw.rect(screen, (200,250,70), (64+(node[0]*32),64+(node[1]*32),32,32))

class BossShoot :
	def __init__(self, x, y, a) :
		self.objectType = "bossShoot"
		self.x = x
		self.y = y
		self.bbox = pygame.Rect(self.x, self.y, 16, 16) 
		self.angle = a
		self.sprite = sSpiderBossShoot
		self.imageIndex = 0
		self.imageSpeed = 0.2
		self.life = 90
		self.speed = 4

	def update(self) :
		# Se désintégrer
		if self.life > 0 :
			self.life -= 1
		elif self.life <= 0 :
			instances.remove(self)
			return

		for obj in instances :
			solidCheck = obj.objectType == "wall" or obj.objectType == "block" or obj.objectType == "eyeBlock" 
			doorCheck = obj.objectType == "bossLock" or obj.objectType == "itemLock" or obj.objectType == "doorLock" 
			if solidCheck or doorCheck :
				if self.bbox.colliderect(obj.bbox) :
					instances.remove(self)
					return

			if obj.objectType == "player" :
				# Affliger les dégats à l'ennemi
				if self.bbox.colliderect(obj.bbox) :
					if not obj.hit:
						obj.health -= 1
						obj.invincibilityFrames = 30
						obj.hit = True
					instances.remove(self)
					return

		# Se déplacer
		self.x += lengthDirX(self.speed, self.angle)
		self.y += lengthDirY(self.speed, self.angle)
		self.bbox.x, self.bbox.y = self.x, self.y

		# Animer le sprite
		self.imageIndex += self.imageSpeed
		if self.imageIndex > len(self.sprite)-1 :
			self.imageIndex = 0

		# Dessiner le sprite a l'ecran
		screen.blit(self.sprite[round(self.imageIndex)], (self.x-camera.x,self.y-camera.y))

class Boss :
	def __init__(self, x, y) :
		self.objectType = "boss"
		self.x = x
		self.y = y
		self.bbox = pygame.Rect(self.x+34, self.y+42, 32, 32) 
		self.sprite = sSpiderBossOpen
		self.imageIndex = 0
		self.imageSpeed = 0.1
		self.health = 3
		self.hit = False
		self.invincibilityFrames = 0
		self.speed = 2
		self.d = random.randint(0,3)
		self.moveAlarm = random.randint(10,45)
		self.shootAlarm = random.randint(25,80)

	def update(self) :
		# Calculer la direction du joueur
		playerAngle = pointDirection((self.x+44,self.y+52),(playerX+16,playerY))

		# Changer de direction pour bouger
		if self.moveAlarm > 0 :
			self.moveAlarm -= 1
		elif self.moveAlarm <= 0 :
			self.moveAlarm = random.randint(10,45)
			self.d = random.randint(0,3)

		# Tirer des projectiles dans la direction du joueur
		if self.shootAlarm > 0 :
			self.shootAlarm -= 1
		elif self.shootAlarm <= 0 :
			self.shootAlarm = random.randint(25,80)
			instances.append(BossShoot(int(self.x+40+lengthDirX(6,playerAngle)), int(self.y+48+lengthDirY(6,playerAngle)), playerAngle))

		# Se déplacer dans la direction choisie
		if self.d == N:
			self.y -= self.speed
			if self.y <= roomY+64:
				self.d = S
		if self.d == E:
			self.x += self.speed
			if self.x >= roomX+352 :
				self.d = W
		if self.d == S:
			self.y += self.speed
			if self.y >= roomY+192:
				self.d = N
		if self.d == W:
			self.x -= self.speed
			if self.x <= roomX+64 :
				self.d = E

		self.x = clamp(self.x,roomX+64,roomX+352)
		self.y = clamp(self.y,roomY+64,roomY+192)
		self.bbox.x, self.bbox.y = self.x+34, self.y+42

		# Prendre des dégats
		if self.hit :
			self.sprite = sSpiderBossClosed
			self.invincibilityFrames -= 1
			if self.invincibilityFrames <= 0 :
				self.hit = False
				self.sprite = sSpiderBossOpen

		# Mourir
		if self.health <= 0 :
			instances.remove(self)
			dungeon.Map[yCell][xCell].enemyCounter -= 1
			return

		# Animer le sprite
		self.imageIndex += self.imageSpeed
		if self.imageIndex > len(self.sprite)-1 :
			self.imageIndex = 0

		# Dessiner le sprite a l'ecran
		screen.blit(self.sprite[round(self.imageIndex)], (self.x-camera.x,self.y-camera.y))

		# Dessiner l'oeil du boss de façon à ce qu'il regarde toujours le joueur
		if not self.hit :
			screen.blit(sSpiderBossEye, (int(self.x+40+lengthDirX(6,playerAngle)-camera.x),int(self.y+48+lengthDirY(6,playerAngle)-camera.y)))
		
		if debugMode :
			pygame.draw.rect(screen, (150,150,150), (self.bbox.x-camera.x,self.bbox.y-camera.y-1,32,32))

#----------Inventaire du joueur----------

class Bomb :
	def __init__(self, x, y) :
		self.objectType = "bomb"
		self.x = x
		self.y = y
		self.sprite = sBomb
		self.originX = 0
		self.originY = 0
		self.imageIndex = 0
		self.imageSpeed = 0.1
		self.tick = 0
		self.exploded = False

	def update(self) :
		# Compter le temps avant l'explosion
		if not self.exploded :
			self.tick += 1
			# Exploser au bout d'une seconde
			if self.tick >= 60 :
				self.exploded = True
				self.sprite = sBombExplosion
				self.originX = 48
				self.originY = 48
				self.imageSpeed = 0.2
				aExplosion.play()

		elif self.imageIndex < 4 :
			# Detruire les objets qui se trouvent dans la deflagration
			for obj in instances :
				if obj.objectType == "block" or obj.objectType == "enemy" or obj.objectType == "player":
					explosionRange = pointDistance((obj.x,obj.y),(self.x+16,self.y+16))
					if explosionRange <= 64 :
						if obj.objectType == "block" :
							instances.remove(obj)
						else :
							if not obj.hit :
								obj.health -= 2
								obj.invincibilityFrames = 30
								obj.hit = True
						aStar.createGrid()

		# Animer le sprite
		self.imageIndex += self.imageSpeed
		if self.imageIndex > len(self.sprite)-1 :
			self.imageIndex = 0
			if self.exploded :
				instances.remove(self)
				return

		# Dessiner le sprite a l'ecran
		screen.blit(self.sprite[round(self.imageIndex)], (self.x-camera.x-self.originX,self.y-camera.y-self.originY))

		if debugMode :
			pygame.draw.circle(screen, (255,0,0), (self.x-camera.x+16,self.y-camera.y+16), 64, 1)

class Arrow :
	def __init__(self, x, y, d) :
		self.objectType = "arrow"
		self.x = x
		self.y = y
		self.d = d
		self.speed = 4
		if self.d == N or self.d == S :
			self.bbox = pygame.Rect(x+8, y, 16, 32)
		if self.d == E or self.d == W:
			self.bbox = pygame.Rect(x, y+8, 32, 16)
	
	def update(self) :
		global switches

		# Aller dans la direction
		if self.d == N:
			self.y -= self.speed
		if self.d == E:
			self.x += self.speed
		if self.d == S:
			self.y += self.speed
		if self.d == W:
			self.x -= self.speed
			
		if self.d == N or self.d == S :
			self.bbox.x, self.bbox.y = self.x+8, self.y
		if self.d == E or self.d == W:
			self.bbox.x, self.bbox.y = self.x, self.y+8
		

		# Se casser 
		for obj in instances :
			# Contre un mur
			solidCheck = obj.objectType == "wall" or obj.objectType == "block" or obj.objectType == "eyeBlock" 
			doorCheck = obj.objectType == "bossLock" or obj.objectType == "itemLock" or obj.objectType == "doorLock" 
			if solidCheck or doorCheck :
				if self.bbox.colliderect(obj.bbox) :
					# Activer les interrupteurs
					if self.d == N and obj.objectType == "eyeBlock" and not obj.open :
						obj.open = 1
						switches -= 1
					instances.remove(self)
					return

			# Contre un ennemi
			if obj.objectType == "boss" or  obj.objectType == "enemy":
				# Affliger les dégats à l'ennemi
				if self.bbox.colliderect(obj.bbox) :
					if not obj.hit:
						obj.health -= 1
						obj.invincibilityFrames = 30
						obj.hit = True
					instances.remove(self)
					return

		# Dessiner le sprite
		screen.blit(sArrow[self.d], (self.x-camera.x,self.y-camera.y))

		if debugMode :
			pygame.draw.rect(screen, (150,88,150), (self.bbox.x-camera.x,self.bbox.y-camera.y,self.bbox.w,self.bbox.h))

#----------Murs et blocs destructibles----------
class Wall :
	def __init__(self, x, y, w, h) :
		self.objectType = "wall"
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.bbox = pygame.Rect(x, y, w, h)

	def update(self) :
		if debugMode :
			pygame.draw.rect(screen, (150,88,150), (self.x-camera.x,self.y-camera.y,self.w,self.h))

class Crack :
	def __init__(self, x, y, d) :
		self.objectType = "block"
		self.x = x+32
		self.y = y+32
		self.d = d
		self.bbox = pygame.Rect(x, y, 64, 64)

	def update(self) :
		# Dessiner le sprite a l'ecran
		screen.blit(sCrack[self.d], (self.x-camera.x-32,self.y-camera.y-33))
		
		if debugMode :
			pygame.draw.rect(screen, (150,150,150), (self.bbox.x-camera.x,self.bbox.y-camera.y-1,64,64))

class Block :
	def __init__(self, x, y) :
		self.objectType = "block"
		self.x = x
		self.y = y
		self.bbox = pygame.Rect(x, y, 32, 32)

	def update(self) :
		# Dessiner le sprite a l'ecran
		screen.blit(sBlock, (self.x-camera.x,self.y-camera.y))

#----------Blocs interactifs----------

class EyeBlock :
	def __init__(self, x, y) :
		self.objectType = "eyeBlock"
		self.x = x
		self.y = y
		self.bbox = pygame.Rect(x, y, 32, 32)
		self.open = 0

	def update(self) :
		# Dessiner le sprite a l'ecran
		screen.blit(sEyeBlock[self.open], (self.x-camera.x,self.y-camera.y))

class Spikes :
	def __init__(self, x, y) :
		self.objectType = "spikes"
		self.x = x
		self.y = y
		self.bbox = pygame.Rect(x, y, 32, 32)
		self.open = 0

	def update(self) :
		# S'ouvrir lorque tout les interrupteurs sont activés
		if switches == 0 :
			self.open = 1

		# Dessiner le sprite a l'ecran
		screen.blit(sSpikes[self.open], (self.x-camera.x,self.y-camera.y))

#----------Objets à récupérer----------

class Bow :
	def __init__(self, x, y) :
		self.objectType = "bow"
		self.x = x
		self.y = y
		self.bbox = pygame.Rect(x, y, 32, 32)

	def update(self) :
		# Dessiner le sprite a l'ecran
		screen.blit(sBow, (self.x-camera.x,self.y-camera.y))

class CoinItem :
	def __init__(self, x, y) :
		self.objectType = "coinItem"
		self.x = x
		self.y = y
		self.bbox = pygame.Rect(x, y, 32, 32)

	def update(self) :
		# Dessiner le sprite a l'ecran
		screen.blit(sCoin, (self.x-camera.x,self.y-camera.y))

class BigHeartItem :
	def __init__(self, x, y) :
		self.objectType = "bigHeartItem"
		self.x = x
		self.y = y
		self.bbox = pygame.Rect(x, y, 32, 32)

	def update(self) :
		# Dessiner le sprite a l'ecran
		screen.blit(sBigHeart, (self.x-camera.x,self.y-camera.y))

class SwordItem :
	def __init__(self, x, y) :
		self.objectType = "swordItem"
		self.x = x
		self.y = y
		self.bbox = pygame.Rect(x, y, 32, 32)

	def update(self) :
		# Dessiner le sprite a l'ecran
		screen.blit(sSword, (self.x-camera.x,self.y-camera.y))

class HeartItem :
	def __init__(self, x, y) :
		self.objectType = "heartItem"
		self.x = x
		self.y = y
		self.bbox = pygame.Rect(x, y, 32, 32)

	def update(self) :
		# Dessiner le sprite a l'ecran
		screen.blit(sHeart, (self.x-camera.x,self.y-camera.y))

class BombItem :
	def __init__(self, x, y) :
		self.objectType = "bombItem"
		self.x = x
		self.y = y
		self.bbox = pygame.Rect(x, y, 32, 32)

	def update(self) :
		# Dessiner le sprite a l'ecran
		screen.blit(sBomb[0], (self.x-camera.x,self.y-camera.y))

class ArrowItem :
	def __init__(self, x, y) :
		self.objectType = "arrowItem"
		self.x = x
		self.y = y
		self.bbox = pygame.Rect(x, y, 32, 32)

	def update(self) :
		# Dessiner le sprite a l'ecran
		screen.blit(sArrow[0], (self.x-camera.x,self.y-camera.y))

class SmallKey :
	def __init__(self, x, y) :
		self.objectType = "smallKey"
		self.x = x
		self.y = y
		self.bbox = pygame.Rect(x, y, 32, 32)

	def update(self) :
		# Dessiner le sprite a l'ecran
		screen.blit(sSmallKey, (self.x-camera.x,self.y-camera.y))

class BigKey :
	def __init__(self, x, y) :
		self.objectType = "bigKey"
		self.x = x
		self.y = y
		self.bbox = pygame.Rect(x, y, 32, 32)

	def update(self) :
		# Dessiner le sprite a l'ecran
		screen.blit(sBigKey, (self.x-camera.x,self.y-camera.y))

class Staircase :
	def __init__(self, x, y) :
		self.objectType = "staircase"
		self.x = x
		self.y = y
		self.bbox = pygame.Rect(x, y, 32, 32)

	def update(self) :
		# Dessiner le sprite a l'ecran
		screen.blit(sStaircase, (self.x-camera.x,self.y-camera.y))

#----------Portes----------

class DoorLock :
	def __init__(self, x, y, d) :
		self.objectType = "doorLock"
		self.x = x
		self.y = y
		self.direction = d
		self.bbox = pygame.Rect(x, y, 64, 64)

	def update(self) :
		if debugMode :
			pygame.draw.rect(screen, (250,230,30), (self.x-camera.x,self.y-camera.y,64,64))

	def draw(self) :
		# Dessiner le sprite à l'écran
		screen.blit(sDoorLock[self.direction], (self.x-camera.x,self.y-camera.y))
		
class SacrificeDoor :
	def __init__(self, x, y, d) :
		self.objectType = "sacrficieDoor"
		self.x = x
		self.y = y
		self.direction = d
		self.bbox = pygame.Rect(x, y, 64, 64)

	def update(self) :
		for obj in instances :
			if obj.objectType == "player" :
				# Affliger les dégats au joueur
				if self.bbox.colliderect(obj.bbox) :
					if not obj.hit:
						obj.health -= 1
						obj.invincibilityFrames = 30
						obj.hit = True

		# Dessiner le sprite à l'écran
		screen.blit(sSacrificeDoor[self.direction], (self.x-camera.x,self.y-camera.y))

class BossLock :
	def __init__(self, x, y, d) :
		self.objectType = "bossLock"
		self.x = x
		self.y = y
		self.direction = d
		self.bbox = pygame.Rect(x, y, 64, 64)

	def update(self) :
		# Dessiner le sprite à l'écran
		screen.blit(sBossLock[self.direction], (self.x-camera.x,self.y-camera.y))
		if debugMode :
			pygame.draw.rect(screen, (250,230,30), (self.x-camera.x,self.y-camera.y,64,64))

class ItemLock :
	def __init__(self, x, y, d) :
		self.objectType = "itemLock"
		self.x = x
		self.y = y
		self.direction = d
		self.bbox = pygame.Rect(x, y, 64, 64)

	def update(self) :
		# Dessiner le sprite à l'écran
		screen.blit(sItemLock[self.direction], (self.x-camera.x,self.y-camera.y))
		if debugMode :
			pygame.draw.rect(screen, (230,230,230), (self.x-camera.x,self.y-camera.y,64,64))

#----------Generation de donjon----------

class Room :
	def __init__(self, exits, roomType) :
	    self.exits = exits # Liste des sorties
	    self.roomType = roomType # Type de salle
	    self.exitType = [] # Types de sorties
	    for i in range(4) :
	    	self.exitType.append("normal")

	    self.structure = ""
	    self.mobs = []
	    self.enemyCounter = -1
	    self.cleared = True

class Dungeon :
	def generate(self) :
		# Choisir la case depart et la taille du donjon
		self.xStart = 4
		self.yStart = 4
		self.dungeonSize = 8 + chapter
		numberOfRooms = 6 + chapter + random.randint(2,3+chapter)

		xCell = self.xStart
		yCell = self.yStart

		# Creer une carte vide
		self.Map = []
		for h in range(self.dungeonSize) :
			self.Map.append([])
			for w in range(self.dungeonSize) :
				self.Map[h].append(0)

		# Placer la premiere salle
		self.Map[yCell][xCell] = Room([], "start")
		roomCounter = 1

		while roomCounter < numberOfRooms :
			foundRoom = False
			while not foundRoom :
				# Choisir une cellule au hazard
				if roomCounter < 3 :
					xCell = self.xStart
					yCell = self.yStart
				else :
					yCell = random.randint(0,self.dungeonSize-1)
					xCell = random.randint(0,self.dungeonSize-1)
				cell = self.Map[yCell][xCell]

				# Verifier si la cellule est une salle
				if cell != 0 :
					# Creer une liste des directions possibles
					exitList = [N,E,S,W]

					# Enlever les directions deja existantes
					for d in cell.exits :
						exitList.remove(d)

					# Choisir les directions favorables
					for d in exitList :
						adj = adjacentDirection(xCell, yCell, d)
						outside = not (adj[0] in range(self.dungeonSize) and adj[1] in range(self.dungeonSize))
						if outside or self.Map[adj[1]][adj[0]] != 0 :
							exitList.remove(d)

					# Si il y a au moins une direction favorable choisir la salle
					if exitList :
						foundRoom = True

			# Choisir une direction au hazard dans la liste
			direction = random.choice(exitList)
			self.Map[yCell][xCell].exits.append(direction)

			# Creer la salle dans cette direction
			adj = adjacentDirection(xCell, yCell, direction)
			self.Map[adj[1]][adj[0]] = Room([oppositeDirection(direction)], "")
			roomCounter += 1 

		cellTypes = ["boss", "item", "shop", "miniBoss", "bossKey"]
		cellTypes.append(random.choice(["bonus", "sacrifice"]))
		lockTypes = ["bossLock", "itemLock", "shopDoor", "normal", "normal"]
		if "bonus" in cellTypes :
			lockTypes.append("hiddenDoor")
		elif "sacrifice" in cellTypes :
			lockTypes.append("sacrificeDoor")

		index = 0
		for cellType in cellTypes :
			foundRoom = False 
			coupleList = listOfCouples(self.dungeonSize)
			while not foundRoom :
				if not coupleList :
					# Creer une nouvelle salle
					trying = True
					while trying :
						yCell = random.randint(0,self.dungeonSize-1)
						xCell = random.randint(0,self.dungeonSize-1)
						cell = self.Map[yCell][xCell]
						if cell != 0 and (cell.roomType == "" or cell.roomType == "miniBoss" or cell.roomType == "bossKey"): 
							# Creer une liste des directions possibles
							exitList = [N,E,S,W]

							# Enlever les directions deja existantes
							for d in cell.exits :
								exitList.remove(d)

							# Choisir les directions favorables
							for d in exitList :
								adj = adjacentDirection(xCell, yCell, d)
								outside = not (adj[0] in range(self.dungeonSize) and adj[1] in range(self.dungeonSize))
								if outside or self.Map[adj[1]][adj[0]] != 0 :
									exitList.remove(d)

							# Si il y a au moins une direction favorable choisir la salle
							if exitList :
								trying = False

					# Choisir une direction au hazard dans la liste
					direction = random.choice(exitList)
					self.Map[yCell][xCell].exits.append(direction)
					self.Map[yCell][xCell].exitType[direction] = lockTypes[index]

					# Creer la salle dans cette direction
					adj = adjacentDirection(xCell, yCell, direction)
					self.Map[adj[1]][adj[0]] = Room([oppositeDirection(direction)], cellType)
					foundRoom = True
				else :
					# Choisir une cellule au hazard
					couple = random.choice(coupleList)
					coupleList.remove(couple)
					yCell = couple[0]
					xCell = couple[1]
					cell = self.Map[yCell][xCell]

					if cellType == "miniBoss" or cellType == "bossKey" :
						# Prendre une salle vide
						if cell != 0 and cell.roomType == "":
							self.Map[yCell][xCell].roomType = cellType
							foundRoom = True
					else :
						# Verifier si la cellule est une salle avec une seule sortie
						if cell != 0 and len(cell.exits) == 1 and cell.roomType == "" :
							self.Map[yCell][xCell].roomType = cellType
							# Verouiller l'entree depuis la salle adjacente
							direction = cell.exits[0]
							adj = adjacentDirection(xCell, yCell, direction)
							self.Map[adj[1]][adj[0]].exitType[oppositeDirection(direction)] = lockTypes[index]
							foundRoom = True
			index += 1

		#b = arrangement de blocs, x = nombre d'arrangements, d = diamant, t = triangle, c = cercle
		structureList = ["b1x2","b1x4","b2x5","b6x1","b6x2","d","t4","t2N","t2S","c"]
		enemyList = ["enemy"]
		for h in range(self.dungeonSize) :
			for w in range(self.dungeonSize) :
				if self.Map[h][w] != 0 :
					if self.Map[h][w].roomType == "" :
						self.Map[h][w].structure = random.choice(structureList)
						self.Map[h][w].mobs  = random.choice(enemyList)
						self.Map[h][w].cleared = False
						structureList.remove(self.Map[h][w].structure)
					elif self.Map[h][w].roomType == "miniBoss" or self.Map[h][w].roomType == "boss" or self.Map[h][w].roomType == "bossKey":
						self.Map[h][w].cleared = False

	def build(self) : 
		global background, foreground, switches
		for h in range(self.dungeonSize) :
			for w in range(self.dungeonSize) :
				if self.Map[h][w] != 0 :
					x = w*512
					y = h*352

					if self.Map[h][w].roomType == "shop" :
						background.blit(sBackgroundShop,(x,y))
					else :
						background.blit(sBackground,(x,y))

					# Créer les murs en haut et en bas
					instances.append(Wall(x+64,y,160,64)) #Haut-Gauche
					instances.append(Wall(x+288,y,160,64)) #Haut-Droite
					instances.append(Wall(x+64,y+288,160,64)) #Bas-Gauche
					instances.append(Wall(x+288,y+288,160,64)) #Bas-Droite

					# Créer les murs sur les cotés
					instances.append(Wall(x,y+64,64,96)) #Haut-Gauche
					instances.append(Wall(x,y+192,64,96)) #Bas-Droite
					instances.append(Wall(x+448,y+64,64,96)) #Haut-Droite
					instances.append(Wall(x+448,y+192,64,96)) #Bas-Gauche

					# Pour chaque directions
					for d in range(4) : 
						if d == N:
							dx = x+224
							dy = y
						if d == E:
							dx = x+448
							dy = y+144
						if d == S:
							dx = x+224
							dy = y+288
						if d == W:
							dx = x
							dy = y+144

						# Créer les murs la ou il n'y a pas de portes
						if not d in self.Map[h][w].exits :
							instances.append(Wall(dx,dy,64,64))
							background.blit(sWall[d],(dx,dy-1))
						# Créer les portes 
						elif self.Map[h][w].exitType[d] == "bossLock" :
							instances.append(BossLock(dx,dy,d)) 
						elif self.Map[h][w].exitType[d] == "itemLock" :
							instances.append(ItemLock(dx,dy,d)) 
						elif self.Map[h][w].exitType[d] == "sacrificeDoor" :
							instances.append(SacrificeDoor(dx,dy,d)) 
							foreground.blit(sSacrificeDoorForeground[d],(dx,dy-1))
						elif self.Map[h][w].exitType[d] == "hiddenDoor" :
							background.blit(sHiddenDoor[d],(dx,dy-1))
							foreground.blit(sHiddenDoorForeground[d],(dx,dy))
							instances.append(Crack(dx,dy,d)) 

						if d in self.Map[h][w].exits and self.Map[h][w].exitType[d] != "hiddenDoor":
							foreground.blit(sForeground[d],(dx,dy))

					# Placer les blocs dans la salle
					blockList = getBlockList(self.Map[h][w].structure)
					if blockList :
						for block in blockList :
							instances.append(Block(x+block[0],y+block[1]))

					if self.Map[h][w].roomType == "bossKey" :
						instances.append(BigKey(x+240,y+160))
						if chapter == 1 :
							instances.append(EyeBlock(x+192,y+128))
							instances.append(EyeBlock(x+288,y+128))
							switches = 2
						blockList = getBlockList("bossKey" + str(chapter))
						for block in blockList :
							instances.append(Spikes(x+block[0],y+block[1]))
					elif self.Map[h][w].roomType == "item" :
						instances.append(Bow(x+240,y+160)) 
					elif self.Map[h][w].roomType == "bonus" :
						instances.append(BigHeartItem(x+240,y+160)) 
					elif self.Map[h][w].roomType == "sacrifice" :
						instances.append(SwordItem(x+240,y+160)) 
					elif self.Map[h][w].roomType == "shop" :
						instances.append(Shop(x+240,y+96)) 


#----------Recherche de chemin pour l'IA ----------

class Node :
	def __init__(self, x, y) :
		self.walkable = True
		self.x = x
		self.y = y
		self.gCost = -1
		self.hCost = 0
		self.fCost = self.gCost + self.hCost
		self.parent = 0

class aStarGrid :
	def createGrid(self) :
		self.gridHeight = 7  # Hauteur de la grille
		self.gridWidth = 12 # Largeur de la grille
		# Créer une grille vide
		self.grid = [] 
		for h in range(self.gridHeight) :
			self.grid.append([])
			for w in range(self.gridWidth) :
				self.grid[h].append(Node(w,h))

		# Ajouter les obstacles
		for obj in instances :
			typeCheck = (obj.objectType == "block" or obj.objectType == "enemy" or obj.objectType == "spikes" or obj.objectType == "eyeBlock")
			if typeCheck and obj.x in range(roomX+64, roomX+448) and obj.y in range(roomY+64,roomY+288):
				h = (obj.y-roomY-64)//32
				w = (obj.x-roomX-64)//32
				self.grid[h][w].walkable = False

	# Recupere les noeuds voisins
	def getNeighbours(self, node) :
		neighbours = []

		directions = [(0,1),(0,-1),(1,0),(-1,0)]
		for d in directions :
			checkX = node.x + d[0]
			checkY = node.y + d[1]

			if checkX in range(0,self.gridWidth) and checkY in range(0,self.gridHeight) :
				neighbours.append(self.grid[checkY][checkX])
		return neighbours

	# Recupere la distance entre deux noeuds
	def getDistance(self, a, b) :
		distX = abs(a.x - b.x)
		distY = abs(a.y - b.y)

		if distX > distY :
			return 14*distY + 10*(distX-distY)
		else :
			return 14*distX + 10*(distY-distX)

	# Retrace le chemin grace aux parents
	def retracePath(self, startNode, targetNode) :
		path = []
		currentNode = targetNode

		while (currentNode != startNode) :
			path.append((currentNode.x,currentNode.y))
			currentNode = currentNode.parent

		return path

	def findPath(self, a, b) :
		# Recuperer la position dans la grille
		aX = int((a[0]-roomX-64)//32)
		aY = int((a[1]-roomY-64)//32)
		bX = int((b[0]-roomX-64)//32)
		bY = int((b[1]-roomY-64)//32)
  		
  		# Definir le premier noeud
		startNode = self.grid[aY][aX]
		# Le premier noeud possede un cout de 0
		startNode.gCost = 0 
		# Definir le dernier noeud
		targetNode = self.grid[bY][bX]

		# La liste des noeuds qui n'ont pas encore été évalués
		openList = [] 
		# La liste des noeuds déjà évalués
		closedList = []

		# Ajouter le premier noeud à la liste d'attente
		openList.append(startNode)

		while len(openList) > 0 :
			currentNode = openList[0]
			i = 1
			while i < len(openList) : 
				# Récuperer le noeud avec le cout le plus faible
				if openList[i].fCost < currentNode.fCost or openList[i].fCost == currentNode.fCost and openList[i].hCost < currentNode.hCost :
					currentNode = openList[i]
				i += 1

			# Retirer le noeud actuel de la liste d'attente
			openList.remove(currentNode)
			closedList.append(currentNode)

			# Si le noeud actuel est le noeud recherché
			if currentNode == targetNode :
				# Retracer le chemin
				return self.retracePath(startNode,targetNode)

			# Récuperer les voisins du noeud actuel
			neighbours = self.getNeighbours(currentNode)

			for neighbour in neighbours :
				# Si le voisin peut etre traversé et si il est dans la liste d'attente
				if neighbour.walkable and not neighbour in closedList :

					# Calculer le cout de déplacement vers ce voisin
					newMovementCostToNeighbour = currentNode.gCost + self.getDistance(currentNode,neighbour)

					# Si le nouveau chemin vers ce voisin est plus court
					if newMovementCostToNeighbour < neighbour.gCost or not neighbour in openList :
						# Réassigner les couts heurisitque et les couts de déplacement
						neighbour.gCost = newMovementCostToNeighbour
						neighbour.hCost = self.getDistance(neighbour,targetNode)
						neighbour.fCost = neighbour.gCost + neighbour.hCost
						# Assigner le noeud actuel comme etant parent de son voisin
						neighbour.parent = currentNode 

						if not neighbour in openList :
							openList.append(neighbour)

#----------Initialiser le jeu----------

# Initialiser pygame
pygame.init()
clock = pygame.time.Clock()
pygame.mixer.init()

# Charger les police d'écriture
font48 = pygame.font.Font("font.ttf", 48) 
font32 = pygame.font.Font("font.ttf", 32) 
font16 = pygame.font.Font("font.ttf", 16)

# Configuer la fenetre
windowWidth = 512 # Largeur
windowHeight = 352 # Hauteur
windowSize = [windowWidth, windowHeight] # Taille de la fenetre
window = pygame.display.set_mode(windowSize, HWSURFACE|DOUBLEBUF|RESIZABLE) # Surface qui va être affichée
screen = window.convert() # Surface sur laquelle tout va être dessiné
appSize = windowSize.copy() # Taille de la surface

# Titre de la fenetre
pygame.display.set_caption("The Cave Crawler")

# Modes
debugMode = False
pause = False
gameOver = False

# Initialiser les états
ROOM_MENU = True
ROOM_GAME = False
ROOM_CREDIT = False
ROOM_OPTIONS = False

# Tant que le joueur n aura pas quitte le jeu :
running = True
while running :

	# generation des options
	
	menu = ["Play","How To Play","Quit"]
	menuSpace = 54
	menuX = 96
	menuY = 96

	# couleurs

	textColor = (0,255,0)
	boxColor  = (100,0,0)
	boxColorFocus = (200,0,0)

	# détection du clic

	mouseX = 0
	mouseY = 0
	mouseClick = False

	# creation des rectangle autour des options

	menuBoxes = []
	index = 0
	for option in menu:
		menuBoxes.append(Rect(menuX-16,menuY+menuSpace*index-2,256,36))
		index += 1

	menuPosition = 0

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
				mouseX = (event.pos[0] - (windowSize[0]/2-appSize[0]/2))//(appSize[0]/windowWidth)
				mouseY = (event.pos[1] - (windowSize[1]/2-appSize[1]/2))//(appSize[0]/windowWidth)

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

				# Activer/desactiver le mode debug
				if event.key == pygame.K_KP_MULTIPLY:
					debugMode = not debugMode

		# Rafraichir l'écran avec du gris
		screen.fill((25,25,25))

		# si la souris est sur une option
		index = 0
		mouseInBox = False

		# verification de la position de la souris
		for option in menu:
			
			# verification de l'option choisie
			backColor = boxColor
			if menuBoxes[index].collidepoint((mouseX,mouseY)) :
				backColor = boxColorFocus
				menuPosition = index
				mouseInBox = True

			pygame.draw.rect(screen, backColor, menuBoxes[index])

			# affichage du nom de l'option
			text = font32.render(option, 3, textColor)
			screen.blit(text,(menuX,menuY+menuSpace*index))
			index += 1

		if mouseClick and mouseInBox:

			# option play
			if menuPosition == 0 :
				ROOM_MENU = False
				ROOM_GAME = True

			# option option
			if menuPosition == 1 :
				ROOM_MENU = False
				ROOM_OPTIONS = True
				
			# option exit
			if menuPosition == 2 :
				ROOM_MENU = False
				running = False

		# Dessiner le titre
		text = font48.render("The Cave Crawler", 3, (255,255,255))
		screen.blit(text,(64,32))

		# Dessiner les credits
		text = font16.render("By Nicolas Reszka & Tymothe Laine", 0, (255,255,255))
		screen.blit(text,(64,288))

		# Afficher la surface de dessin au centre de la fenetre
		window.blit(pygame.transform.scale(screen, appSize).convert(), (windowSize[0]/2-appSize[0]/2,windowSize[1]/2-appSize[1]/2))

		# Mettre à jour l'écrans
		pygame.display.flip()

	if ROOM_OPTIONS :
		backToMenu = Rect(menuX-16,menuY+menuSpace*3-2,256,36)
		instructions = ["Up/Down/Left/Right : move", "W : bomb", "X : use item","C : attack"]

	while ROOM_OPTIONS :	
		mouseClick = False

		# Repeter les actions 60 fois par secondes
		clock.tick(60)

		# Parcourir la liste des evenements
		for event in pygame.event.get():

			# Quitter le jeu
			if event.type == pygame.QUIT:
				ROOM_OPTIONS = False
				running = False

			# Récupérer la position de la souris
			if event.type == pygame.MOUSEMOTION:
				mouseX = (event.pos[0] - (windowSize[0]/2-appSize[0]/2))//(appSize[0]/windowWidth)
				mouseY = (event.pos[1] - (windowSize[1]/2-appSize[1]/2))//(appSize[0]/windowWidth)

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
				# Activer/desactiver le mode debug
				if event.key == pygame.K_KP_MULTIPLY:
					debugMode = not debugMode

		# Rafraichir l'écran avec du gris
		screen.fill((25,25,25))

		# verification de l'option choisie
		backColor = boxColor
		if backToMenu.collidepoint((mouseX,mouseY)) :
			backColor = boxColorFocus
			if mouseClick :
				ROOM_MENU = True
				ROOM_OPTIONS = False

		pygame.draw.rect(screen, backColor, backToMenu)

		# affichage du nom de l'option
		text = font32.render("Back To Menu", 3, textColor)
		screen.blit(text,(menuX,menuY+menuSpace*3))

		# Dessiner le titre
		text = font48.render("How to play", 3, (255,255,255))
		screen.blit(text,(72,32))

		# Dessiner les instructions
		index = 0
		for instruction in instructions :
			text = font16.render(instruction, 0, (255,255,255))
			screen.blit(text,(menuX,menuY+menuSpace/2*index))
			index += 1

		# Afficher la surface de dessin au centre de la fenetre
		window.blit(pygame.transform.scale(screen, appSize).convert(), (windowSize[0]/2-appSize[0]/2,windowSize[1]/2-appSize[1]/2))

		# Mettre à jour l'écrans
		pygame.display.flip()

	while ROOM_CREDIT :	
		# Repeter les actions 60 fois par secondes
		clock.tick(60)

		# Parcourir la liste des evenements
		for event in pygame.event.get():

			# Quitter le jeu
			if event.type == pygame.QUIT:
				ROOM_CREDIT = False
				running = False

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
				# Activer/desactiver le mode debug
				if event.key == pygame.K_KP_MULTIPLY:
					debugMode = not debugMode

		# Rafraichir l'écran avec du gris
		screen.fill((0,0,0))

		# Dessiner les remerciements
		text = font32.render("Cette demo est terminee !", 3, (255,255,255))
		screen.blit(text,(72,32))
		text = font32.render("Merci d'avoir participe !", 3, (255,255,255))
		screen.blit(text,(80,64))

		# Dessiner les crédits
		text = font16.render("Un jeu de Nicolas Reszka & Tymothe Laine", 0, (255,255,255))
		screen.blit(text,(64,288))

		# Afficher la surface de dessin au centre de la fenetre
		window.blit(pygame.transform.scale(screen, appSize).convert(), (windowSize[0]/2-appSize[0]/2,windowSize[1]/2-appSize[1]/2))

		# Mettre à jour l'écrans
		pygame.display.flip()

 	# Rejouer
	if gameOver :
		gameOver = False
		ROOM_GAME = True

	# Ne pas charger les sprites
	if not ROOM_GAME:
	 	continue

	chapter = 1

	#----------Charger les sprites----------

	sPlayerIdle = []
	sPlayerMove = []
	sPlayerAttack = []
	sEnemy = []
	for d in range(4) :
		sPlayerIdle.append(loadSpriteStripe(pygame.image.load("sprites/characters/playerIdle.png"), 1, d*32,32,32))
		sPlayerMove.append(loadSpriteStripe(pygame.image.load("sprites/characters/playerMove.png"), 2, d*32,32,32))
		sPlayerAttack.append(loadSpriteStripe(pygame.image.load("sprites/characters/playerAttack.png"), 4, d*64,64,64))
		sEnemy.append(loadSpriteStripe(pygame.image.load("sprites/characters/enemy.png"), 2, d*32,32,32))

	sShopKeeper = loadSpriteStripe(pygame.image.load("sprites/characters/shopKeeper.png"), 2, 0,32,32)

	sSpider = loadSpriteStripe(pygame.image.load("sprites/characters/spider.png"), 2, 0,32,32)

	sMiniBoss = [] 
	for d in range(2) :
		sMiniBoss.append(loadSpriteStripe(pygame.image.load("sprites/characters/miniBoss.png"), 2, 32*d,32,32))

	sSpiderBossOpen = loadSpriteStripe(pygame.image.load("sprites/characters/boss.png"), 2, 0,96,96)
	sSpiderBossClosed = loadSpriteStripe(pygame.image.load("sprites/characters/boss.png"), 2, 96,96,96)
	sSpiderBossEye = pygame.image.load("sprites/characters/bossEye.png").convert_alpha()
	sSpiderBossShoot = loadSpriteStripe(pygame.image.load("sprites/characters/bossShoot.png"), 4, 0,16,16)

	sCoin = pygame.image.load("sprites/items/coin.png").convert_alpha()
	sSword = pygame.image.load("sprites/items/sword.png").convert_alpha()
	sHeart = pygame.image.load("sprites/items/heart.png").convert_alpha()
	sBigHeart = pygame.image.load("sprites/items/bigHeart.png").convert_alpha()
	sArrow = loadSpriteStripe(pygame.image.load("sprites/items/arrow.png"), 4, 0,32,32)
	sBomb = loadSpriteStripe(pygame.image.load("sprites/items/bomb.png"), 2, 0,32,32)
	sBombExplosion = loadSpriteStripe(pygame.image.load("sprites/items/bombExplosion.png"), 11, 0,128,128)

	sBlock = pygame.image.load("sprites/level" + str(chapter) + "/block.png").convert()
	sSpikes = loadSpriteStripe(pygame.image.load("sprites/level" + str(chapter) + "/spikes.png"), 2,0,32,32)
	sEyeBlock = loadSpriteStripe(pygame.image.load("sprites/level" + str(chapter) + "/eyeBlock.png"), 2,0,32,32)

	sBackground = pygame.image.load("sprites/level" + str(chapter) + "/background.png").convert()
	sBackgroundShop = pygame.image.load("sprites/level" + str(chapter) + "/backgroundShop.png").convert()
	sForeground = loadSpriteStripe(pygame.image.load("sprites/level" + str(chapter) + "/foreground.png"), 4,0,64,64)
	sWall = loadSpriteStripe(pygame.image.load("sprites/level" + str(chapter) + "/wall.png"), 4,0,64,64)

	sCrack = loadSpriteStripe(pygame.image.load("sprites/level" + str(chapter) + "/crack.png"), 4,0,64,64)
	sHiddenDoor = loadSpriteStripe(pygame.image.load("sprites/level" + str(chapter) + "/hiddenDoor.png"), 4,0,64,64)
	sHiddenDoorForeground = loadSpriteStripe(pygame.image.load("sprites/level" + str(chapter) + "/hiddenDoorForeground.png"), 4,0,64,64)

	sBow = pygame.image.load("sprites/items/bow.png").convert_alpha()
	sSmallKey = pygame.image.load("sprites/items/smallKey.png").convert_alpha()
	sBigKey = pygame.image.load("sprites/items/bigKey.png").convert_alpha()

	sSacrificeDoor = loadSpriteStripe(pygame.image.load("sprites/level" + str(chapter) + "/sacrificeDoor.png"), 4,0,64,64)
	sSacrificeDoorForeground = loadSpriteStripe(pygame.image.load("sprites/level" + str(chapter) + "/sacrificeDoorForeground.png"), 4,0,64,64)

	sDoorLock = loadSpriteStripe(pygame.image.load("sprites/level" + str(chapter) + "/doorLock.png"), 4,0,64,64)
	sItemLock = loadSpriteStripe(pygame.image.load("sprites/level" + str(chapter) + "/itemLock.png"), 4,0,64,64)
	sBossLock = loadSpriteStripe(pygame.image.load("sprites/level" + str(chapter) + "/bossLock.png"), 4,0,64,64)

	sStaircase = pygame.image.load("sprites/level" + str(chapter) + "/staircase.png").convert_alpha()

	sHeartUI = loadSpriteStripe(pygame.image.load("sprites/userInterface/uiHeart.png"), 3,0,18,18)
	sArrowUI = pygame.image.load("sprites/userInterface/uiArrow.png").convert_alpha()
	sBombUI = pygame.image.load("sprites/userInterface/uiBomb.png").convert_alpha()
	sSwordUI = pygame.image.load("sprites/userInterface/uiSword.png").convert_alpha()
	sCoinUI = pygame.image.load("sprites/userInterface/uiCoin.png").convert_alpha()

	defaultSurface = pygame.image.load("sprites/defaultSurface.png").convert_alpha()

	#----------Charger les sons----------
	aExplosion = pygame.mixer.Sound("audio/explosion.wav")
	aBow = pygame.mixer.Sound("audio/bow.wav")
	aSword = pygame.mixer.Sound("audio/sword.wav")
	aKey = pygame.mixer.Sound("audio/key.wav")
	aHeart = pygame.mixer.Sound("audio/heart.wav")
	aBigHeart = pygame.mixer.Sound("audio/bigHeart.wav")

	#----------Fin du chargement----------

	dungeon = Dungeon()
	dungeon.generate()

	# Se placer dans la cellule de départ
	xCell = dungeon.xStart
	yCell = dungeon.yStart

	# Calculer la largeur et la hauteur du donjon entier
	roomWidth  = windowWidth  * dungeon.dungeonSize
	roomHeight = windowHeight * dungeon.dungeonSize

	# Créer la surface de l'arrière plan
	background = defaultSurface.copy()
	background = pygame.transform.scale(background, (roomWidth,roomHeight))

	# Créer la surface du premier plan
	foreground = defaultSurface.copy()
	foreground = pygame.transform.scale(foreground, (roomWidth,roomHeight))

	# Definir le x et le y de la cellule actuelle
	roomX = xCell * windowWidth
	roomY = yCell * windowHeight

	# Initialiser la liste d'instances
	instances = []

	# Initialiser les interrupteurs
	switches = 0

	# Creer tout les objets du donjon
	dungeon.build()

	# Initialiser la camera
	camera = pygame.rect.Rect(roomX, roomY, windowWidth, windowHeight)
	transition = False
	transitionDirection = 0

	#instances.append(Boss(roomX+176,roomY+102))
	#instances.append(MiniBoss(roomX+240,roomY+128))

	# Placer le joueur
	xMove = 0
	yMove = 0
	keyAttack = False
	keyItem = False
	keyBomb = False
	bigKey = 0
	smallKey = 0
	playerDamage = 1
	playerMoney = 0
	playerArrows = 0
	playerBombs = 1
	playerBow = False
	playerX = roomX+256-16
	playerY = roomY+176-16
	instances.append(Player(playerX, playerY))
	
	# Créer la grille de pathfinding
	aStar = aStarGrid()
	aStar.createGrid()

	# Afficher le menu
	while ROOM_GAME :	

		# Repeter les actions 60 fois par secondes
		clock.tick(60)

		# Parcourir la liste des evenements
		for event in pygame.event.get():

			# Quitter le jeu
			if event.type == pygame.QUIT:
				ROOM_GAME = False
				running = False

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
				# Attaquer
				if event.key == pygame.K_c:
					keyAttack = True
				# Utiliser un item
				if event.key == pygame.K_x:
					keyItem = True
				# Poser une bombe
				if event.key == pygame.K_z:
					keyBomb = True

				# Activer/desactiver le mode debug
				if event.key == pygame.K_KP_MULTIPLY:
					debugMode = not debugMode

				# Activer/desactiver la pause
				if event.key == pygame.K_ESCAPE :
					pause = not pause

				# Rejouer
				if gameOver and (event.key == pygame.K_RETURN or event.key == pygame.K_SPACE) :
					ROOM_GAME = False

			# Verifier si les touches ne sont plus pressées
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT and xMove == -1 or event.key == pygame.K_RIGHT and xMove == 1:
					xMove = 0
				if event.key == pygame.K_UP and yMove == -1 or event.key == pygame.K_DOWN and yMove == 1:
					yMove = 0
				if event.key == pygame.K_c:
					keyAttack = False
				if event.key == pygame.K_x:
					keyItem = False
				if event.key == pygame.K_z:
					keyBomb = False

		if not pause :
			# Rafraichir l'écran avec du noir
			screen.fill((0,0,0))

			# Dessiner l'arrière plan
			screen.blit(background, (0-camera.x,0-camera.y))

			# Dessiner les portes avant les autres instances
			for instance in instances :
				if instance.objectType == "doorLock" :
					instance.draw()

			# Effectuer le code de toutes les instances
			for instance in instances :
				instance.update()

			# Ouvrir les portes lorsque tout les ennemis dans la piece sont morts
			if not dungeon.Map[yCell][xCell].cleared :
				if dungeon.Map[yCell][xCell].enemyCounter == 0 :
					dungeon.Map[yCell][xCell].cleared = True
					for d in range(4) :
						for obj in instances :
							if obj.objectType == "doorLock" :
								instances.remove(obj)
					if dungeon.Map[yCell][xCell].roomType == "boss" : 
						instances.append(Staircase(roomX+256,roomY+128))

			# Dessiner le premier plan
			screen.blit(foreground, (0-camera.x,0-camera.y))

			# Dessiner le "Game Over"
			if gameOver :
				gameOverText = font32.render("Game Over", 3, (255,255,255))
				screen.blit(colorize(gameOverText,(0,0,0)),(178,98))
				screen.blit(gameOverText,(176,96))
				gameOverText2 = font16.render("Press ENTER to try again", 0, (255,255,255))
				gameOverTextShadow = font16.render("Press ENTER to try again", 0, (0,0,0))
				screen.blit(gameOverTextShadow,(166,130))
				screen.blit(gameOverText2,(164,128))

		# Afficher la surface de dessin au centre de la fenetre
		window.blit(pygame.transform.scale(screen, appSize).convert(), (windowSize[0]/2-appSize[0]/2,windowSize[1]/2-appSize[1]/2))

		# Mettre à jour l'écrans
		pygame.display.flip()

# Finir le programme
pygame.quit()
