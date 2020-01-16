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
