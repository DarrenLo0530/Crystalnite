# Work on potion description screens
# Work on attack display and damage
# Work on run
# Work on mob health
# Combine code

from random import randint
import pygame

pygame.init()
gameWindow = pygame.display.set_mode((800, 600))

#### Player Buttons ####
class playerButton:
    def __init__(self, buttonX, buttonY, buttonLength, buttonWidth, buttonColor, buttonTextFontSize, buttonTextColor, buttonMessage, buttonText, buttonTextX,
                 buttonTextY, status=False):

        self.buttonX = buttonX
        self.buttonY = buttonY 
        self.buttonLength = buttonLength
        self.buttonWidth = buttonWidth
        self.buttonColor = buttonColor
        
        self.buttonTextFontSize = pygame.font.SysFont(None, 40)
        self.buttonTextColor = buttonTextColor
        self.buttonMessage = buttonMessage
        self.buttonText = self.buttonTextFontSize.render(buttonMessage, 1, self.buttonTextColor)
        self.buttonTextX = buttonTextX
        self.buttonTextY = buttonTextY

        self.status = False
 
    def createButton(self):
        pygame.draw.rect(gameWindow, self.buttonColor, (self.buttonX, self.buttonY, self.buttonLength, self.buttonWidth), 0)
        gameWindow.blit(self.buttonText, (self.buttonTextX, self.buttonTextY))

    def ifClicked(self):
        click = pygame.mouse.get_pressed()
        mouseX, mouseY = pygame.mouse.get_pos()
        if (self.buttonX <= mouseX <= self.buttonX + self.buttonLength) and (self.buttonY <= mouseY <= self.buttonY + self.buttonWidth) and (click[0] == 1):
            return True
        return False

### Inventory Buttons ###
class inventoryButton:
    def __init__(self, buttonX, buttonY, buttonLength, buttonWidth, buttonColor, picture, pictureLoad, pictureResizeX, pictureResizeY, pictureTransform,
                 pictureX, pictureY, generateFont, number, display, numberX, numberY):
        
        self.buttonX = buttonX
        self.buttonY = buttonY
        self.buttonLength = buttonLength
        self.buttonWidth = buttonWidth
        self.buttonColor = buttonColor

        self.picture = picture
        self.pictureLoad = pygame.image.load(self.picture)
        self.pictureResizeX = pictureResizeX
        self.pictureResizeY = pictureResizeY
        self.pictureTransform = pygame.transform.scale(self.pictureLoad, (self.pictureResizeX, self.pictureResizeY))
        self.pictureX = pictureX
        self.pictureY = pictureY

        self.generateFont = pygame.font.SysFont(None, 20)
        self.number = number
        self.display = self.generateFont.render(str(self.number), 1, black)
        self.numberX = numberX
        self.numberY = numberY

    def createNewButton(self):
        pygame.draw.rect(gameWindow, self.buttonColor, (self.buttonX, self.buttonY, self.buttonLength, self.buttonWidth), 0)
        gameWindow.blit(self.pictureTransform, (self.pictureX, self.pictureY))

    def ifClicked(self):
        click = pygame.mouse.get_pressed()
        mouseX, mouseY = pygame.mouse.get_pos()
        if (self.buttonX <= mouseX <= self.buttonX + self.buttonLength) and (self.buttonY <= mouseY <= self.buttonY + self.buttonWidth) and (click[0] == 1) and (self.number > 0):
            return True            
        return False

#### Health Bar Function ####
    
def getHealth(totalHealth, damage, heal, backBarX, backBarY, backBarLength, backBarWidth, backBarColor, barColor):
    pygame.draw.rect(gameWindow, backBarColor, (backBarX, backBarY, backBarLength, backBarWidth), 0) # Back Bar
    newHealth = totalHealth + heal - damage
    if newHealth >= 100:
        newHealth = 100
    pygame.draw.rect(gameWindow, barColor, (backBarX, backBarY, newHealth * 3, backBarWidth), 0) # Front Bar
    totalHealth = newHealth
    
    font = pygame.font.SysFont(None, 40)
    playerDisplay = font.render(str(totalHealth) + "/100", 1, barColor)
    playerText = font.render("PLAYER HEALTH", 1, barColor)
    gameWindow.blit(playerDisplay, (160, 70))
    gameWindow.blit(playerText, (90, 20))

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
sand = (253, 228, 200)
gray = (169, 169, 169)
purple = (127, 0, 255)
brightPurple = (131, 89, 163)
darkRed = (139, 0, 0)

smallFont = pygame.font.SysFont(None, 35)
font = pygame.font.SysFont(None, 40)
largerFont = pygame.font.SysFont(None, 60)

escape = largerFont.render("YOU ESCAPED!", 1, white)
noEscape = largerFont.render("CAN'T ESCAPE!", 1, white)

tier1HealthPotionDescription = smallFont.render("TIER I HEALTH POTION - HEALS 20 POINTS OF DAMAGE", 1, white)
tier1StrengthPotionDescription = smallFont.render("TIER I STRENGTH POTION - ADDS 5 POINTS OF DAMAGE", 1, white)
tier1SpeedPotionDescription = smallFont.render("TIER I SPEED POTION - ADDS +1 MOVEMENT SPEED", 1, white)
woodShieldDescription = smallFont.render("WOOD SHIELD - ADDS 20 POINTS TO TOTAL HEALTH", 1, white)

tier2HealthPotionDescription = smallFont.render("TIER I HEALTH POTION - HEALS 50 POINTS OF DAMAGE", 1, white)
tier2StrengthPotionDescription = smallFont.render("TIER I STRENGTH POTION - ADDS 10 POINTS OF DAMAGE", 1, white)
tier2SpeedPotionDescription = smallFont.render("TIER I SPEED POTION - ADDS +3 MOVEMENT SPEED", 1, white)
ironShieldDescription = smallFont.render("IRON SHIELD - ADDS 50 POINTS TO TOTAL HEALTH", 1, white)

# Variables
playerClicked = 0

totalHealth = 100
damage = 0
heal = 0

# Class Calls
attack = playerButton(150, 500, 150, 75, red, True, black, "ATTACK", True, 170, 525)
item = playerButton(330, 500, 150, 75, blue, True, black, "ITEM", True, 370, 525)
run = playerButton(510, 500, 150, 75, green, True, black, "RUN", True, 555, 525)
back = playerButton(0, 525, 150, 75, sand, True, black, "BACK", True, 35, 550)
itemBack = playerButton(225, 300, 150, 75, sand, True, black, "BACK", True, 260, 325)
select = playerButton(425, 300, 150, 75, brightPurple, True, black, "SELECT", True, 450, 325)

tier1HealthPotion = inventoryButton(110, 130, 125, 125, white, "Potion of Vitality.png", True, 80, 100, True, 135, 142, True, 2, True, 220, 240)
tier1StrengthPotion = inventoryButton(260, 130, 125, 125, white, "Draught of Titans.png", True, 80, 100, True, 285, 142, True, 2, True, 370, 240)
tier1SpeedPotion = inventoryButton(410, 130, 125, 125, white, "Elixir of Haste.png", True, 80, 100, True, 435, 142, True, 2, True, 520, 240)
woodShield = inventoryButton(560, 130, 125, 125, white, "Wood Shield.png", True, 100, 100, True, 573, 140, True, 1, True, 670, 240)

tier2HealthPotion = inventoryButton(110, 330, 125, 125, white, "Potion of Vitality.png", True, 80, 100, True, 135, 340, True, 2, True, 220, 440)
tier2StrengthPotion = inventoryButton(260, 330, 125, 125, white, "Draught of Titans.png", True, 80, 100, True, 285, 340, True, 2, True, 370, 440)
tier2SpeedPotion = inventoryButton(410, 330, 125, 125, white, "Elixir of Haste.png", True, 80, 100, True, 435, 340, True, 2, True, 520, 440)
ironShield = inventoryButton(560, 330, 125, 125, white, "Shield.png", True, 120, 120, True, 560, 330, True, 1, True, 670, 440)

# Boolean Checks
invButton = False
description = False
inPlay = True
canRun = True
invEffect = False

# Main Program
while inPlay:
    pygame.event.clear()
    getHealth(totalHealth, damage, heal, 50, 100, 300, 10, darkRed, red)
    
    if (playerClicked == 0):
        attack.createButton()
        item.createButton()
        run.createButton()

    if (attack.ifClicked()) and (not invButton):
        gameWindow.fill(black)
        playerClicked = 1
        back.createButton()
        invButton = True

    elif (run.ifClicked()) and (not invButton) and (canRun):
        playerClicked = 3
        random = randint(0, 2)
        if random == 0:
            break
        else:
            canRun = False
            gameWindow.blit(noEscape, (225, 150))
            run.buttonColor = gray
    
    elif (item.ifClicked()) and (not invButton):
        gameWindow.fill(black)
        playerClicked = 2
        back.createButton()
        invButton = True
        
        tier1HealthPotion.createNewButton()
        tier1HealthPotion.display = tier1HealthPotion.generateFont.render(str(tier1HealthPotion.number), 1, black)
        gameWindow.blit(tier1HealthPotion.display, (tier1HealthPotion.numberX, tier1HealthPotion.numberY))
        
        tier1StrengthPotion.createNewButton()
        tier1StrengthPotion.display = tier1StrengthPotion.generateFont.render(str(tier1StrengthPotion.number), 1, black)
        gameWindow.blit(tier1StrengthPotion.display, (tier1StrengthPotion.numberX, tier1StrengthPotion.numberY))
        
        tier1SpeedPotion.createNewButton()
        tier1SpeedPotion.display = tier1SpeedPotion.generateFont.render(str(tier1SpeedPotion.number), 1, black)
        gameWindow.blit(tier1SpeedPotion.display, (tier1SpeedPotion.numberX, tier1SpeedPotion.numberY))

        woodShield.createNewButton()
        woodShield.display = woodShield.generateFont.render(str(woodShield.number), 1, black)
        gameWindow.blit(woodShield.display, (woodShield.numberX, woodShield.numberY))

        tier2HealthPotion.createNewButton()
        tier2HealthPotion.display = tier2HealthPotion.generateFont.render(str(tier2HealthPotion.number), 2, black)
        gameWindow.blit(tier2HealthPotion.display, (tier2HealthPotion.numberX, tier2HealthPotion.numberY))

        tier2StrengthPotion.createNewButton()
        tier2StrengthPotion.display = tier2StrengthPotion.generateFont.render(str(tier2StrengthPotion.number), 2, black)
        gameWindow.blit(tier2StrengthPotion.display, (tier2StrengthPotion.numberX, tier2StrengthPotion.numberY))

        tier2SpeedPotion.createNewButton()
        tier2SpeedPotion.display = tier2SpeedPotion.generateFont.render(str(tier2SpeedPotion.number), 1, black)
        gameWindow.blit(tier2SpeedPotion.display, (tier2SpeedPotion.numberX, tier2SpeedPotion.numberY))

        ironShield.createNewButton()
        ironShield.display = ironShield.generateFont.render(str(ironShield.number), 1, black)
        gameWindow.blit(ironShield.display, (ironShield.numberX, ironShield.numberY))

    # Inventory Button Actions

    # Tier 1 Health Potion
    if (tier1HealthPotion.ifClicked()) and (invButton) and (not invEffect):
        gameWindow.fill(black)
        gameWindow.blit(tier1HealthPotionDescription, (60, 200))
        itemBack.createButton()
        select.createButton()
        playerClicked = 4
        invEffect = True
        
    if (select.ifClicked()) and (playerClicked == 4) and (invEffect):
        gameWindow.fill(black)
        itemBack.createButton()
        select.createButton()
        playerClicked = 0
        heal += 20
        invButton = False
        invEffect = False
        tier1HealthPotion.number -= 1
        gameWindow.fill(black)
        
    # Tier 1 Strength Potion
    if (tier1StrengthPotion.ifClicked()) and (invButton) and (not invEffect):
        gameWindow.fill(black)
        gameWindow.blit(tier1StrengthPotionDescription, (60, 200))
        itemBack.createButton()
        select.createButton()
        playerClicked = 5
        invEffect = True

    if (select.ifClicked()) and (playerClicked == 5) and (invEffect):
        gameWindow.fill(black)
        itemBack.createButton()
        select.createButton()
        playerClicked = 0
        invButton = False
        invEffect = False
        tier1StrengthPotion.number -= 1
        gameWindow.fill(black)
        
    # Tier 1 Speed Potion
    if (tier1SpeedPotion.ifClicked()) and (invButton) and (not invEffect):
        gameWindow.fill(black)
        gameWindow.blit(tier1SpeedPotionDescription, (60, 200))
        itemBack.createButton()
        select.createButton()
        playerClicked = 6
        invEffect = True

    if (select.ifClicked()) and (playerClicked == 6) and (invEffect):
        gameWindow.fill(black)
        itemBack.createButton()
        select.createButton()
        playerClicked = 0
        invButton = False
        invEffect = False
        tier1SpeedPotion.number -= 1
        gameWindow.fill(black)
        
    # Wood Shield
    if (woodShield.ifClicked()) and (invButton) and (not invEffect):
        gameWindow.fill(black)
        gameWindow.blit(woodShieldDescription, (60, 200))
        itemBack.createButton()
        select.createButton()
        playerClicked = 7
        invEffect = True

    if (select.ifClicked()) and (playerClicked == 7) and (invEffect):
        gameWindow.fill(black)
        itemBack.createButton()
        select.createButton()
        playerClicked = 0
        invButton = False
        invEffect = False
        woodShield.number -= 1
        gameWindow.fill(black)
        
    # Tier 2 Health Potion
    if (tier2HealthPotion.ifClicked()) and (invButton) and (not invEffect):
        gameWindow.fill(black)
        gameWindow.blit(tier2HealthPotionDescription, (60, 200))
        itemBack.createButton()
        select.createButton()
        playerClicked = 8
        invEffect = True

    if (select.ifClicked()) and (playerClicked == 8) and (invEffect):
        gameWindow.fill(black)
        itemBack.createButton()
        select.createButton()
        playerClicked = 0
        heal += 50
        invButton = False
        invEffect = False
        tier2HealthPotion.number -= 1
        gameWindow.fill(black)
        
    # Tier 2 Strength Potion  
    if (tier2StrengthPotion.ifClicked()) and (invButton) and (not invEffect):
        gameWindow.fill(black)
        gameWindow.blit(tier2StrengthPotionDescription, (60, 200))
        itemBack.createButton()
        select.createButton()
        playerClicked = 9
        invEffect = True

    if (select.ifClicked()) and (playerClicked == 9) and (invEffect):
        gameWindow.fill(black)
        itemBack.createButton()
        select.createButton()
        playerClicked = 0
        invButton = False
        invEffect = False
        tier2StrengthPotion.number -= 1
        gameWindow.fill(black)
        
    # Tier 2 Speed Potion
    if (tier2SpeedPotion.ifClicked()) and (invButton) and (not invEffect):
        gameWindow.fill(black)
        gameWindow.blit(tier2SpeedPotionDescription, (60, 200))
        itemBack.createButton()
        select.createButton()
        playerClicked = 10
        invEffect = True

    if (select.ifClicked()) and (playerClicked == 10) and (invEffect):
        gameWindow.fill(black)
        itemBack.createButton()
        select.createButton()
        playerClicked = 0
        invButton = False
        invEffect = False
        tier2SpeedPotion.number -= 1
        gameWindow.fill(black)

    # Iron Shield
    if (ironShield.ifClicked()) and (invButton) and (not invEffect):
        gameWindow.fill(black)
        gameWindow.blit(ironShieldDescription, (60, 200))
        itemBack.createButton()
        select.createButton()
        playerClicked = 11
        invEffect = True

    if (select.ifClicked()) and (playerClicked == 11) and (invEffect):
        gameWindow.fill(black)
        itemBack.createButton()
        select.createButton()
        playerClicked = 0
        invButton = False
        invEffect = False
        ironShield.number -= 1
        gameWindow.fill(black)
        
    if (back.ifClicked()) and (invButton) and ((playerClicked == 1) or (playerClicked == 2) or (playerClicked == 3)):
        gameWindow.fill(black)
        playerClicked = 0
        invButton = False

    if (itemBack.ifClicked()) and (invButton) and ((playerClicked == 4) or (playerClicked == 5) or (playerClicked == 6) or (playerClicked == 7) or (playerClicked == 8) or (playerClicked == 9) or (playerClicked == 10) or (playerClicked == 11)):
        gameWindow.fill(black)
        playerClicked = 0
        invButton = False
        invEffect = False
                                     
    pygame.display.update()
pygame.quit()

