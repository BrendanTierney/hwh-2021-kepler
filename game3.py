import pygame
import random
import math

width = 900
height = 700

pygame.init()
gameDisplay = pygame.display.set_mode((width,height))
pygame.display.set_caption('Game name')

white = (255, 255, 255)
black = (0,0,0)
red = (255, 0, 0)
UoEBlue = (4, 30, 66)
Logo = pygame.image.load('Uni logo blue.png')
Logo = pygame.transform.scale(Logo, (int(342*0.55), int(342*0.55)))

clock = pygame.time.Clock()

#Enter filename of picture card followed by that persons description in a jpeg
#these must be in the correct order
cardPairs = ["0.jpeg","0.jpeg","1.jpeg","1.jpeg","2.jpeg","2.jpeg","3.jpeg","3.jpeg","4.jpeg","4.jpeg","5.jpeg","5.jpeg","6.jpeg","6.jpeg","7.jpeg","7.jpeg"]

#SWAPCARDS 2D List of 16 zeros
#first part is filename, second part is the pair number x in {x; 0<=x<=8}, third part is True/False if it has been correctly matched yet
swapCards = [["",0,False],["",0,False],["",0,False],["",0,False],["",0,False],["",0,False],["",0,False],["",0,False],["",0,False],["",0,False],["",0,False],["",0,False],["",0,False],["",0,False],["",0,False],["",0,False]]


##Randomly assign cards to board positions
unfilledPositions = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
for i in range(16):
    position = random.choice(unfilledPositions)
    unfilledPositions.remove(position)

    swapCards[position][0] = cardPairs[i]       #Place the cardNumber into the randomly chosen board position
    swapCards[position][1] = math.floor(i/2)    #Place the pair number, math.floor(i/2) ensures that we will always have x in {x; 0<=x<=8}

print(swapCards)

crashed = False


##Setup cards as pygame Images
backCards = []
frontCards = []
card_width = int(400/3.6)
card_height = int(600/3.6)
for i in range(16):

    ##Back cards
    backImg = pygame.image.load('Card back.jpg')    #Loads the card picture
    backImg = pygame.transform.scale(backImg, (card_width, card_height))   #Scale the image to size (scales were random)
    backCards.append(backImg)   #Scale the image to size (scales were random)

    ##Front cards
    frontImg = pygame.image.load(swapCards[i][0])
    frontImg = pygame.transform.scale(frontImg, (card_width, card_height))
    frontCards.append(frontImg)

##Setup coordinates for top left corner of each card
x_coords = []
y_coords = []
for i in range(4):   #creates x,y coordinates for each card (for the top left corner)
    for j in range(4):
        x_coords.append(width*0.2*(j+1.05))
        y_coords.append(height*0.25*(i+0.05))


##Setup board and place initial cards
gameDisplay.fill(UoEBlue)  #Makes the background UoE blue
gameDisplay.blit(Logo, (0,0))
for i in range(len(backCards)): # Loads all the cards with their coords onto the screen
    gameDisplay.blit(backCards[i], (x_coords[i],y_coords[i]))

pygame.display.update()


totalCorrectPairs = 0       #Max value 6
numberOfFlippedCards = 0    #Values 0 or 1
currentFlippedCardNo = 999

while not crashed:


    for event in pygame.event.get():   #Make sure game can handle crashes
        if event.type == pygame.QUIT:
            crashed = True

        if event.type == pygame.MOUSEBUTTONDOWN:

            clickPos = event.pos

            for i in range(16):

                #Determine which card was clicked
                if x_coords[i] <= clickPos[0] <= x_coords[i] + card_width and y_coords[i] <= clickPos[1] <= y_coords[i] + card_height:

                    if swapCards[i][2] == True:
                        #This card has already been correctly matched
                        break

                    pygame.display.update(gameDisplay.blit(frontCards[i], (x_coords[i],y_coords[i])))   #This line will swap out the card for someones face or a description
                    print(i)

                    if numberOfFlippedCards == 0:
                        #first card
                        currentFlippedCardNo = i
                        numberOfFlippedCards += 1
                        break

                    elif numberOfFlippedCards == 1:

                        if currentFlippedCardNo == i:
                            #User has clicked on the same card in quick succession
                            #Not valid, so break out
                            break

                        #Check if card is of the same pair as the one already flipped
                        if swapCards[currentFlippedCardNo][1] == swapCards[i][1]:
                            ##MATCH - fill in red for the moment
                            pygame.time.wait(500)  #Wait in milliseconds
                            pygame.display.update(pygame.draw.rect(gameDisplay, red, (x_coords[currentFlippedCardNo], y_coords[currentFlippedCardNo], card_width, card_height,)))
                            pygame.display.update(pygame.draw.rect(gameDisplay, red, (x_coords[i], y_coords[i], card_width, card_height,)))

                            totalCorrectPairs += 1

                            ##Update these cards as matched
                            swapCards[i][2] = True
                            swapCards[currentFlippedCardNo][2] = True

                        else:
                            ##not a match
                            #set both to back card image
                            pygame.time.wait(500)  #Wait in milliseconds
                            pygame.display.update(gameDisplay.blit(backCards[i], (x_coords[i], y_coords[i])))
                            pygame.display.update(gameDisplay.blit(backCards[currentFlippedCardNo], (x_coords[currentFlippedCardNo], y_coords[currentFlippedCardNo])))

                        #Reset flipped cards to zero
                        numberOfFlippedCards = 0
                        break

            #If end of this loop is reached and the IF condition is never met then user did not click on a card but somewhere else instead

    if totalCorrectPairs == 8:
        break

    pygame.display.update()
    clock.tick(60)

print("GAME WON")

#create a text object and a box to go behind
font = pygame.font.Font('freesansbold.ttf', 100)
text = font.render("Game Complete!", False, black)
text_rect = text.get_rect(center=(width/2, height/2))
pygame.draw.rect(gameDisplay, white, text_rect)
gameDisplay.blit(text, text_rect)

pygame.display.update()

##Wait for two seconds then display all cards
pygame.time.wait(2000)

gameDisplay.fill(UoEBlue)  # Makes the background UoE blue
gameDisplay.blit(Logo, (0, 0))
for i in range(len(frontCards)):  # Loads all the cards with their coords onto the screen
    gameDisplay.blit(frontCards[i], (x_coords[i], y_coords[i]))

pygame.display.update()

##Wait for 60 seconds before closing
pygame.time.wait(60000)

pygame.quit()
quit()