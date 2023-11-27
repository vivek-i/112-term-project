import random

class Card:
    def __init__(self, suit, number):
        self.suit = suit
        self.number = number
    def __repr__(self):
        return f'{self.number}{self.suit}'
    def getCardValue(self):
        return self.number
    
class Hand:
    def __init__(self):
        self.hand = []
    def getScore(self):
        total = 1
        for card in self.hand:
            cardVal = min(10, card.getCardValue())
            total *= cardVal
        return total
    def addCard(self, card):
        self.hand.append(card)
    def getHandOptions(self):
        if self.getScore() < 112:
            return ['Hit', 'Stand']
        # if len(self.hand) == 2 and self.hand[0].number == self.hand[1].number:
        #     return ['Hit', 'Stand', 'Double']
        return []

def generateDeck():
    deck = []
    for suit in ['H', 'D', 'C', 'S']:
        for i in range(1, 14):
            deck.append(Card(suit, i))
    return deck

def generateMultipleDecks(count):
    return shuffleDeck(generateDeck() * count)

def shuffleDeck(d):
    for i in range(len(d)-1, -1, -1):
        randomIndex = random.randint(0, i)
        d[i], d[randomIndex] = d[randomIndex], d[i]
    return d

def getTopCard(d):
    return d.pop(0)

def displayGame(player, computer, playerTurn):
    print("\nDealer: ", end="")    
    if playerTurn:
        print(computer.hand[0], end=" ")
        print("?", end=" ")
    else:
        for card in computer.hand:
            print(card, end=" ")
        print(computer.getScore(), end="")
    print("\nPlayer: ", end="")
    for card in player.hand:
        print(card, end=" ")
    print(player.getScore(), end="")
    print('\n')    

def getOutcomeScore(dealerScore, playerScore):
    if dealerScore > 112:
        return -1
    if dealerScore > playerScore:
        return 1
    elif dealerScore < playerScore:
        return -1
    else:
        return 0

def expectiMax(hand, playerScore):        
    deckVals = [1,2,3,4,5,6,7,8,9,10,10,10,10]
    handScore = hand.getScore()
    noHitScore = getOutcomeScore(handScore, playerScore)
    expectedValue = 0
    for cardVal in deckVals:
        newScore = handScore + cardVal
        expectedValue += getOutcomeScore(newScore, playerScore)
    expectedValue /= len(deckVals)
    print("No Hit Score: " + str(noHitScore))
    print("Hit Score: " + str(expectedValue))
    if noHitScore > expectedValue:
        return "Stand"
    return "Hit"





def makeComputerDecision(computer, playerScore):
    computerScore = computer.getScore()
    result = expectiMax(computer, playerScore)
    print(result)
    return result
    # if computerScore < 50:
    #     return "Hit"
    # return "Stand"



def gameManager():
    deck = generateMultipleDecks(6)
    playerTurn = True
    player = Hand()
    computer = Hand()
    player.addCard(getTopCard(deck))
    computer.addCard(getTopCard(deck))
    player.addCard(getTopCard(deck))
    computer.addCard(getTopCard(deck))
    while playerTurn:
        displayGame(player, computer, playerTurn)
        if player.getScore() > 112:
            playerTurn = False
            break
        options = player.getHandOptions()
        if len(options) > 0:
            print(options)
            choice = input("Pick an Option: ")
            if choice == 'Hit':
                player.addCard(getTopCard(deck))
            if choice == 'Stand':
                playerTurn = False
    computerMove = ''
    while computerMove != 'Stand':
        computerMove = makeComputerDecision(computer, player.getScore())
        if computerMove == 'Hit':
            computer.addCard(getTopCard(deck))
            displayGame(player, computer, playerTurn)
        
    displayGame(player, computer, playerTurn)

    playerScoreDiff = 112 - player.getScore()
    computerScoreDiff = 112 - computer.getScore()

    if playerScoreDiff >= 0 and computerScoreDiff > 0:
        if playerScoreDiff < computerScoreDiff:
            print("Player Wins")
        else:
            print("Dealer Wins")
    elif playerScoreDiff >= 0 and computerScoreDiff < 0:
        print("Player Wins")
    elif computerScoreDiff >= 0 and playerScoreDiff < 0:
        print("Dealer Wins")
    else:
        print("Push")
        
gameManager()



