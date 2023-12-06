import random
import copy


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
        self.done = False
    def getScore(self):
        total = 0
        for card in self.hand:
            cardVal = min(10, card.getCardValue())
            if total == 0:
                total += cardVal
            else:
                if cardVal < 8:
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
                if cardVal < 8:
                    total *= cardVal
                else:
                    total += cardVal       
        return total
    def copyHandWithCard(self, card):
        newHand = Hand()
        newHand.hand = copy.deepcopy(self.hand)
        newHand.addCard(card)
        return newHand

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
        move = exepectiMiniMax(self.player, self.computer, self.playerDone)
        print(move)
        if move == "hit":
            self.computerHit()
        else:
            self.computerStand()
        if self.playerDone and not(self.computerDone):                        
            self.makeComputerMove()            


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
    def __init__(self, playerHand, computerHand, nodeType, turn):
        self.nodeType = nodeType
        self.turn = turn
        self.playerHand = playerHand
        self.computerHand = computerHand
        self.terminating = False
        self.computerDone = False
        self.playerDone = False
        self.children = []        
        self.value = ""

    def gameStateScore(self):
        playerScore = self.playerHand.getScore()
        computerScore = self.computerHand.getScore()
        if computerScore == playerScore:
            return 0
        if playerScore > 112 and computerScore > 112:
            return 0
        if playerScore > 112:
            return 10
        if computerScore > 112:
            return -10
        if playerScore > computerScore:
            return -10
        if computerScore > playerScore:
            return 10
    def gameStateDepthScore(self):        
        playerScore = self.playerHand.getScore()
        computerScore = self.computerHand.getScore()                
        if computerScore > 112:
            return -10
        elif playerScore > 112:
            return 10

        dPlayer = 112 - playerScore
        dComputer = 112 - computerScore
        
        return (dPlayer-dComputer)/5
        

def exepectiMiniMax(playerHand, computerHand, playerDone):
    
    
    

    averageHitScore = 0
    averageStandScore = 0
    cards = [1,2,3,4,5,6,7,8,9,10,10,10,10]
    for cardVal in cards:
        blindHand = copy.deepcopy(playerHand.hand)
        blindHand = blindHand[:-1]
        playerBlindHand = Hand()
        playerBlindHand.hand = blindHand
        blindCard = Card("A", cardVal)
        playerBlindHand.addCard(blindCard)
        initialNode = Node(playerBlindHand, computerHand, "gameState", "computer")
        initialNode.playerDone = playerDone
        expectedHandValue(initialNode)
        # print("hit score", initialNode.children[0].value)
        # print("stand score", initialNode.children[1].value)
        hitScore = initialNode.children[0].value
        standScore = initialNode.children[1].value
        averageHitScore += hitScore
        averageStandScore += standScore

    averageHitScore /= len(cards)
    averageStandScore /= len(cards)

    print("average hit score", averageHitScore)
    print("average stand score", averageStandScore)

    if averageHitScore >= averageStandScore:
        return "hit"
    return "stand"


def expectedHandValue(node, depth=0):        
    depth += 1
    # print(depth, node.playerHand.getScore(), node.computerHand.getScore())
    if (node.playerDone and node.computerDone) or (node.turn == "") or (node.terminating):
        if node.value == "":            
            node.value = node.gameStateScore()        
        return node.value
    else:
        if node.nodeType == "gameState":
            
            standNode = Node(copy.deepcopy(node.playerHand), copy.deepcopy(node.computerHand), "gameState", "x")            
            chanceNode = Node(copy.deepcopy(node.playerHand), copy.deepcopy(node.computerHand), "chance", node.turn)                

            if node.turn == "computer":
                standNode.turn = "player"
                standNode.computerDone = True
                
            elif node.turn == "player":
                standNode.turn = "computer"
                standNode.playerDone = True
                
            if standNode.computerHand.getScore() >= 112 or standNode.playerHand.getScore() >= 112:
                standNode.computerDone = True
                standNode.playerDone = True                
                standNode.terminating = standNode.computerDone and standNode.playerDone

            if chanceNode.computerHand.getScore() >= 112 or chanceNode.playerHand.getScore() >= 112:
                chanceNode.computerDone = True
                chanceNode.playerDone = True            

            hitScore = 0
            standScore = 0

            if depth > 5:
                standNode.terminating = True
                chanceNode.terminating = True
                standNode.playerDone = True
                standNode.computerDone = True
                standScore = standNode.gameStateDepthScore()
                standNode.value = standNode.gameStateDepthScore()
                chanceNode.playerDone = True
                chanceNode.computerDone = True
                hitScore = chanceNode.gameStateDepthScore()
                chanceNode.value = chanceNode.gameStateDepthScore()                            

            hitScore = expectedHandValue(chanceNode, depth)
            standScore = expectedHandValue(standNode, depth)
            
            chanceNode.value = hitScore
            standNode.value = standScore            

            node.children = [chanceNode, standNode]                 
            if node.turn == "computer":                
                return max(hitScore, standScore)
            elif node.turn == "player":                
                return min(hitScore, standScore)
            else:
                return 0

        elif node.nodeType == "chance":
            cards = [1,2,3,4,5,6,7,8,9,10,10,10,10]
            totalScore = 0            
            for cardVal in cards:                
                newNode = Node(copy.deepcopy(node.playerHand), copy.deepcopy(node.computerHand), "gameState", "")
                newCard = Card('A', cardVal)
                if node.turn == "computer":
                    newHand = node.computerHand.copyHandWithCard(newCard)
                    newNode.computerHand = newHand                   
                    if not(node.playerDone):
                        newNode.turn = "player"
                elif node.turn == "player":
                    newHand = node.playerHand.copyHandWithCard(newCard)
                    newNode.playerHand = newHand                    
                    if not(node.computerDone):
                        newNode.turn = "computer"
                if newNode.computerHand.getScore() >= 112:
                    newNode.computerDone = True
                    newNode.playerDone = True
                if newNode.playerHand.getScore() >= 112:
                    newNode.computerDone = True
                    newNode.playerDone = True
                newNode.terminating = newNode.computerDone and newNode.playerDone
                node.children.append(newNode)
                x = expectedHandValue(newNode, depth)
                newNode.value = x                
                totalScore += x
            node.value = totalScore/len(cards)
            return totalScore/len(cards)








