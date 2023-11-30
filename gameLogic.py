import random
import time
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
        total = 0
        for card in self.hand:
            cardVal = min(10, card.getCardValue())
            if total == 0:
                total += cardVal
            else:
                if cardVal < 10:
                    total *= cardVal
                else:
                    total += cardVal            
        return total
    def getBlindScore(self):
        total = 1
        for i in range(len(self.hand) - 1):
            card = self.hand[i]
            cardVal = min(10, card.getCardValue())
            if total == 0:
                total += cardVal
            else:
                if cardVal < 10:
                    total *= cardVal
                else:
                    total += cardVal            
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

class Game:

    def __init__(self):
        self.playerDone = False
        self.computerDone = False
        self.player = Hand()
        self.computer = Hand()
        self.deck = generateMultipleDecks(6)

    def makeComputerMove(self):        
        if self.computer.getScore() < 90:
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
            




