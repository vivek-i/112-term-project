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
    def getBlindScore(self):
        total = 1
        for i in range(len(self.hand) - 1):
            card = self.hand[i]
            cardVal = min(10, card.getCardValue())
            total *= cardVal
        return total
    def addCard(self, card):
        self.hand.append(card)
    def copyAndAdd(self, newCard):
        newCards = self.hand + [newCard]
        newHand = Hand()
        newHand.hand = newCards
        return newHand

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

# def displayGame(player, computer):
#     print("\nDealer: ", end="")    
#     for card in computer.hand:
#         print(card, end=" ")
#     print(computer.getScore(), end="")
#     print("\nPlayer: ", end="")
#     for card in player.hand:
#         print(card, end=" ")
#     print(player.getScore(), end="")
#     print('\n')    

# def getOutcomeScore(dealerScore, playerScore):
#     if dealerScore > 112:
#         return -1
#     if dealerScore > playerScore:
#         return 1
#     elif dealerScore < playerScore:
#         return -1
#     else:
#         return 0

# def expectiMax(hand, playerScore):        
#     deckVals = [1,2,3,4,5,6,7,8,9,10,10,10,10]
#     handScore = hand.getScore()
#     noHitScore = getOutcomeScore(handScore, playerScore)
#     expectedValue = 0
#     for cardVal in deckVals:
#         newScore = handScore + cardVal
#         expectedValue += getOutcomeScore(newScore, playerScore)
#     expectedValue /= len(deckVals)
#     print("No Hit Score: " + str(noHitScore))
#     print("Hit Score: " + str(expectedValue))
#     if noHitScore > expectedValue:
#         return "Stand"
#     return "Hit"

# def makeComputerDecision(computer, playerScore):
#     computerScore = computer.getScore()
#     result = expectiMax(computer, playerScore)
#     print(result)
#     return result
#     # if computerScore < 50:
#     #     return "Hit"
#     # return "Stand"


class Game:

    def __init__(self):
        self.playerDone = False
        self.computerDone = False
        self.player = Hand()
        self.computer = Hand()
        self.deck = generateMultipleDecks(6)

    def makeComputerMove(self):        
        if self.computer.getScore() < 50:
            self.computerHit()
        else:
            self.computerStand()
        if self.playerDone and not(self.computerDone):
            self.makeComputerMove()
        print(gameStateScore(self.computer.getScore(), self.player.getScore()))

    def startGame(self):        
        self.player.addCard(getTopCard(self.deck))
        self.computer.addCard(getTopCard(self.deck))


    def playerHit(self):
        if not(self.playerDone):
            self.player.addCard(getTopCard(self.deck))
            if self.player.getScore() >= 112:
                self.playerDone = True

    def playerStand(self):
        self.playerDone = True

    def computerHit(self):
        if not(self.computerDone):
            self.computer.addCard(getTopCard(self.deck))
            if self.computer.getScore() >= 112:
                self.computerDone = True

    def computerStand(self):
        self.computerDone = True

    def determineWinner(self):
        if self.playerDone and self.computerDone:
            computerScore = self.computer.getScore()
            playerScore = self.player.getScore()
            if computerScore == playerScore:
                return "Push"
            if playerScore > 112 and computerScore > 112:
                return "Push"
            if playerScore > 112:
                return "Computer Wins"
            if computerScore > 112:
                return "Player Wins"
            if playerScore > computerScore:
                return "Player Wins"
            if computerScore > playerScore:
                return "Computer Wins"
        return "In Progress"


        # while not(self.computerDone) or not(self.playerDone):
        #     if not(self.playerDone):                
        #         if self.player.getScore() >= 112:
        #             self.playerDone = True
        #             break
        #         displayGame(self.player, self.computer)
        #         options = self.player.getHandOptions()
        #         if len(options) > 0:
        #             print(options)
        #             choice = input("Pick an Option for Player: ")
        #             if choice == 'Hit':
        #                 self.player.addCard(getTopCard(self.deck))
        #             elif choice == 'Stand':
        #                 self.playerDone = True
        #     if not(self.computerDone):
        #         if self.computer.getScore() >= 112:
        #             self.computerDone = True
        #             break
        #         displayGame(self.player, self.computer)
        #         options = self.computer.getHandOptions()
        #         if len(options) > 0:
        #             print(options)
        #             choice = input("Pick an Option for Computer: ")
        #             if choice == 'Hit':
        #                 self.computer.addCard(getTopCard(self.deck))
        #             elif choice == 'Stand':
        #                 self.computerDone = True

            
        # displayGame(self.player, self.computer)

        # playerScoreDiff = 112 - self.player.getScore()
        # computerScoreDiff = 112 - self.computer.getScore()

        # if playerScoreDiff >= 0 and computerScoreDiff > 0:
        #     if playerScoreDiff < computerScoreDiff:
        #         print("Player Wins")
        #     else:
        #         print("Dealer Wins")
        # elif playerScoreDiff >= 0 and computerScoreDiff < 0:
        #     print("Player Wins")
        # elif computerScoreDiff >= 0 and playerScoreDiff < 0:
        #     print("Dealer Wins")
        # else:
        #     print("Push")


#Expectiminimax Logic
#Not Completed Yet!!!

class Node:
    def __init__(self, nodeType, value, parent):
        self.parent = parent
        self.nodeType = nodeType
        self.children = []
        self.averageScore = 0
        self.value = value

def gameStateScore(computerScore, playerScore):
    if playerScore > 112 and computerScore > 112:
        return 0
    if computerScore > 112:
        return -100
    if playerScore > 112:
        return 100
    if computerScore > playerScore:
        return 50
    if playerScore > computerScore:
        return -50
    return 0

def oppositeType(p):
    if p == "computer":
        return "player"
    return "computer"

def expectiMiniMax(computerHand, playerHand, node):
    if node.nodeType == "computer" or node.nodeType == "player":
        hit = Node("chance", "hit", node.nodeType)
        stand = Node("chance", "stand", node.nodeType)
        node.children.add(hit)
        node.children.add(stand)
        hit.value = expectiMiniMax(computerHand, playerHand, hit)
        stand.value = expectiMiniMax(computerHand, playerHand, stand)
    elif node.nodeType == "chance":
        cards = [1,2,3,4,5,6,7,8,9,10,10,10,10]
        for card in cards:
            if node.parent == "computer":
                h = computerHand.copyAndAdd(Card('A', card))
            else:
                h = playerHand.copyAndAdd(Card('A', card))
            




