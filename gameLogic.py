import random
import copy

# Object for each card
class Card:
    def __init__(self, suit, number):
        self.suit = suit
        self.number = number
    def __repr__(self):
        return f'{self.number}{self.suit}'
    def getCardValue(self):
        return self.number
    
    
# Object containing multiple cards
class Hand:
    def __init__(self):
        self.hand = []
        self.done = False
    # Function to get hand score based on rules of the game
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
    # Function to get hand score based on rules of the game minus the top card
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
    # Copy hand into a new hand object and add an addtional card
    def copyHandWithCard(self, card):
        newHand = Hand()
        newHand.hand = copy.deepcopy(self.hand)
        newHand.addCard(card)
        return newHand
    #Add card object to hand
    def addCard(self, card):
        self.hand.append(card)

#Create deck with every card
def generateDeck():
    deck = []
    for suit in ['H', 'D', 'C', 'S']:
        for i in range(1, 14):
            deck.append(Card(suit, i))
    return deck

#combine multiple decks and shuffle them
def generateMultipleDecks(count):
    return shuffleDeck(generateDeck() * count)


#Fisher–Yates shuffle
def shuffleDeck(d):
    for i in range(len(d)-1, -1, -1):
        randomIndex = random.randint(0, i)
        d[i], d[randomIndex] = d[randomIndex], d[i]
    return d

#Pops top value of deck
def getTopCard(d):
    return d.pop(0)

#Class with all game logic fucntions
class Game:

    def __init__(self):
        self.playerDone = False
        self.computerDone = False
        self.player = Hand()
        self.computer = Hand()
        self.deck = generateMultipleDecks(6)

    #Makes one move if player is still going, makes multiple moves if player is done; uses expectiminimax
    def makeComputerMove(self):        
        move = exepectiMiniMax(self.player, self.computer, self.playerDone)
        if move == "hit":
            self.computerHit()
        else:
            self.computerStand()
        if self.playerDone and not(self.computerDone):                        
            self.makeComputerMove()            

    #Deal cards
    def startGame(self):        
        self.player.addCard(getTopCard(self.deck))
        self.computer.addCard(getTopCard(self.deck))


    #Hit/Stand Actions

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

    #Check Game state
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


#Expectiminimax algorithm

#Nodes are either gamestate/chance nodes and are terminating/non terminating
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

#Scoring system for terminating nodes
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
        
#Scoring system for non terminating nodes
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
        
#Determine best computer move
def exepectiMiniMax(playerHand, computerHand, playerDone):
    
    averageHitScore = 0
    averageStandScore = 0
    
    #Top card is hidden, create a game state for each possible top card, run algorithm to calculate hit/stand scores for each
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
        hitScore = initialNode.children[0].value
        standScore = initialNode.children[1].value
        averageHitScore += hitScore
        averageStandScore += standScore

    #Average out hit/stand scores for all possible hidden card hands
    averageHitScore /= len(cards)
    averageStandScore /= len(cards)    
    
    print("Average Hit Score:", averageHitScore)
    print("Average Stand Score:", averageStandScore)
    
    #Determine move based on average hit/stand scores
    if abs(averageHitScore - averageStandScore) < 0.01:
        return "hit"
    elif averageHitScore >= averageStandScore:
        return "hit"
    else:
        return "stand"

#Get value of each node
def expectedHandValue(node, depth=0):        
    depth += 1
    
    #If terminating node, return value of node
    if (node.playerDone and node.computerDone) or (node.turn == "") or (node.terminating):
        if node.value == "":            
            node.value = node.gameStateScore()        
        return node.value
    else:
        if node.nodeType == "gameState":
            
            #create child node for each possible option
            standNode = Node(copy.deepcopy(node.playerHand), copy.deepcopy(node.computerHand), "gameState", "x")            
            chanceNode = Node(copy.deepcopy(node.playerHand), copy.deepcopy(node.computerHand), "chance", node.turn)                

            if node.turn == "computer":
                standNode.turn = "player"
                standNode.computerDone = True
                
            elif node.turn == "player":
                standNode.turn = "computer"
                standNode.playerDone = True
                
                
            #check if nodes are partially/fully terminating
            if standNode.computerHand.getScore() >= 112 or standNode.playerHand.getScore() >= 112:
                standNode.computerDone = True
                standNode.playerDone = True                
                standNode.terminating = standNode.computerDone and standNode.playerDone

            if chanceNode.computerHand.getScore() >= 112 or chanceNode.playerHand.getScore() >= 112:
                chanceNode.computerDone = True
                chanceNode.playerDone = True            

            hitScore = 0
            standScore = 0

            #check depth
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

            #recursively get scores for hitting/standing
            hitScore = expectedHandValue(chanceNode, depth)
            standScore = expectedHandValue(standNode, depth)
            
            chanceNode.value = hitScore
            standNode.value = standScore            

            #return best option for minimizing/maximizing player
            node.children = [chanceNode, standNode]                 
            if node.turn == "computer":                
                return max(hitScore, standScore)
            elif node.turn == "player":                
                return min(hitScore, standScore)
            else:
                return 0

        elif node.nodeType == "chance":
            
            #if node is a chance node, create a child game state node for every possible hit card
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