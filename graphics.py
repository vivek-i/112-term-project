import gameLogic
from cmu_graphics import *
import random

def onAppStart(app):
    app.playerBalance = 1000
    app.screen = "rules"
    app.width = 1200
    app.height = 1000
    
def startGame(app):
    app.screen = "game"    
    app.game = gameLogic.Game()
    app.game.startGame()
    app.playerCards = []
    app.computerCards = []
    app.betsPlaced = False
    app.betAmount = (app.playerBalance // 10) - ((app.playerBalance // 10)%10)
    app.gameOver = False
    app.result = ""

def onStep(app):
    pass

def onKeyPress(app, key):
    if key == 'r':
        if app.gameOver:
            if app.game.determineWinner() == "Player Wins":
                app.playerBalance += app.betAmount*2
            if app.game.determineWinner() == "Push":
                app.playerBalance += app.betAmount
        startGame(app)
    if key == 'e':
        gameLogic.exepectiMiniMax(app.game.player, app.game.computer)

def redrawAll(app):
    if app.screen == "game":
        drawBoard(app)
        if not(app.betsPlaced):
            drawBettingOptions(app)
        else:
            if not(app.game.playerDone):
                drawOptions(app)      
        if app.betsPlaced:      
            cardOffset = 0
            for i in range(len(app.game.player.hand) - 0):
                card = app.game.player.hand[i]
                drawCard(app, card.suit, card.number, 250 + cardOffset, 250 + cardOffset)
                cardOffset += 30
            # drawBlankCard(app, 250 + cardOffset, 250 + cardOffset)    
            hiddenCards = 0
            if app.game.playerDone == False:
                hiddenCards = 1
            cardOffset = 0
            for i in range(len(app.game.computer.hand) - hiddenCards):
                card = app.game.computer.hand[i]
                drawCard(app, card.suit, card.number, 850 - cardOffset, 250 + cardOffset)
                cardOffset += 30
            if app.game.playerDone == False:
                drawBlankCard(app, 850 - cardOffset, 250 + cardOffset)       
        if app.result != "":
            drawLabel(app.result + " - Press 'r' to play another hand", app.width/2, 885, align = "center", size=35, fill="white")
    elif app.screen == "rules":
        drawRulesScreen(app)
    else:
        drawHomeScreen(app)

def drawRulesScreen(app):
    drawRect(0,0,app.width, app.height, fill="darkGreen")
    drawLabel("112 Blackjack Rules", 100, 100, size=60, fill="white", align="left")    
    drawLabel("- The objective is to get a hand value close to 112 without exceeding it.", 150, 160, size=30, fill="white", align="left")    
    drawLabel("- All cards have values. 2-10 are numbered. A = 1, J,Q,K = 10", 150, 200, size=30, fill="white", align="left")    
    drawLabel("- Each player gets one card to begin with", 150, 240, size=30, fill="white", align="left")    
    drawLabel("- Choose 'hit' for another card or 'stand' to keep current cards on each turn", 150, 280, size=30, fill="white", align="left")    
    drawLabel("- If a card value is less than 10, your hand score is multiplied by that value", 150, 320, size=30, fill="white", align="left")    
    drawLabel("- If a card value is 10, 10 is added to your hand score", 150, 360, size=30, fill="white", align="left")    
    drawLabel("- The player with the hand valued closest to 112 without crossing wins.", 150, 400, size=30, fill="white", align="left")        
    drawLabel("- You are given $1000 to start with.", 150, 440, size=30, fill="white", align="left")    
    drawLabel("- You can bet as much of it as you want before each game.", 150, 480, size=30, fill="white", align="left")    
    drawLabel("- Winning doubles your bet.", 150, 520, size=30, fill="white", align="left")    
    drawLabel("- You cannot see the computer's top card.", 150, 560, size=30, fill="white", align="left")    
    drawLabel("- The computer cannot see your top card.", 150, 600, size=30, fill="white", align="left")    

    drawRect(app.width/2-300, 800, 200, 60, fill="red")
    drawLabel("Back", app.width/2-200, 830, size=40)
    drawRect(app.width/2+100, 800, 200, 60, fill="yellow")
    drawLabel("Play", app.width/2+200, 830, size=40)

def drawHomeScreen(app):
    drawRect(0,0,app.width, app.height, fill="darkGreen")
    drawLabel("112 Blackjack", app.width/2, 100, size=80, fill="white")    
    drawRect(app.width/2-300, 800, 200, 60, fill="red")
    drawLabel("Rules", app.width/2-200, 830, size=40)
    drawRect(app.width/2+100, 800, 200, 60, fill="yellow")
    drawLabel("Play", app.width/2+200, 830, size=40)
    for i in range(1,14):
        symbols = ['C', 'H', 'C', 'D']        
        drawCard(app, symbols[i%4], i, 370 + (i-1)*30, 200+(i-1)*30)


def drawBoard(app):    
    drawRect(0,0,app.width, app.height, fill="darkGreen")
    drawRect(100,200,app.width-200, app.height-400, fill="green", border="black", borderWidth=20)
    drawLabel("112 Blackjack", app.width/2, app.height/2, size=80, fill="darkGreen")
    if app.betsPlaced:
        drawLabel("Player: " + str(app.game.player.getScore()), app.width * (1/4), app.height-300, size=40, fill="darkGreen")
        if app.game.playerDone == False:
            drawLabel("Computer: " + str(app.game.computer.getBlindScore()), app.width* (3/4), app.height-300, size=40, fill="darkGreen")
        else:
            drawLabel("Computer: " + str(app.game.computer.getScore()), app.width* (3/4), app.height-300, size=40, fill="darkGreen")
    drawLabel("Balance: " + str(app.playerBalance), 20, 30, size=30, align="left")

def drawOptions(app):
    # drawRect(0,0,290,0)
    drawRect(110,820,180,50, fill="blue", border="black")
    drawLabel("Hit", 200,845, size=20, fill="white")
    drawRect(310,820,180,50, fill="red", border="black")
    drawLabel("Stand", 400,845, size=20, fill="white")

def drawBettingOptions(app):
    drawRect(app.width/2-80, 820, 160, 50, border="black", fill=None)
    drawLabel(str(app.betAmount), app.width/2, 845, size=25)
    drawCircle(app.width/2-120, 845, 25, border="black", fill=None)
    drawLabel("-", app.width/2-120, 849, size=30)
    drawCircle(app.width/2+120, 845, 25, border="black", fill=None)
    drawLabel("+", app.width/2+120, 847, size=30)
    drawRect(app.width/2-40, 885, 80, 30, fill="Yellow")
    drawLabel("Bet", app.width/2, 900, size=25)
    

def drawBlankCard(app, x, y):
    drawRect(x, y, 100, 150, fill="pink", border="white", borderWidth=4)

def onMousePress(app, mouseX, mouseY):
    if app.screen == "game":
        if app.betsPlaced == True:
            if mouseX >= 110 and mouseX <= 290 and mouseY >= 820 and mouseY <= 870:
                app.game.playerHit()
                app.game.makeComputerMove()
            elif mouseX >= 310 and mouseX <= 490 and mouseY >= 820 and mouseY <= 870:
                app.game.playerStand()
                app.game.makeComputerMove()
            if not(app.game.determineWinner() == "In Progress"):
                app.result = app.game.determineWinner()
                app.gameOver = True        
        else:
            betSize = 10
            if app.playerBalance <= 20:
                betSize = 1
            if distance(mouseX, app.width/2-120, mouseY, 845) <= 25:
                if app.betAmount >= betSize:
                    print("bet decrease")
                    app.betAmount -= betSize
            elif distance(mouseX, app.width/2+120, mouseY, 845) <= 25:
                if app.betAmount <= app.playerBalance - betSize:
                    print("bet increase")
                    app.betAmount += betSize
            elif mouseX >= app.width/2-40 and mouseX <= app.width/2+40 and mouseY >= 885 and mouseY <= 915:
                print("bet submit")
                app.playerBalance -= app.betAmount
                app.betsPlaced = True
    elif app.screen == "home":
        # drawRect(app.width/2-300, 800, 200, 60, fill="red")
        if mouseX >= app.width/2-300 and mouseX <= app.width/2-100 and mouseY >= 800 and mouseY <= 860:
            app.screen="rules"
        elif mouseX >= app.width/2+100 and mouseX <= app.width/2+300 and mouseY >= 800 and mouseY <= 860:
            app.screen="game"
            startGame(app)

    elif app.screen == "rules":
        if mouseX >= app.width/2-300 and mouseX <= app.width/2-100 and mouseY >= 800 and mouseY <= 860:
            app.screen="home"
        elif mouseX >= app.width/2+100 and mouseX <= app.width/2+300 and mouseY >= 800 and mouseY <= 860:
            app.screen="game"
            startGame(app)


def drawCard(app, suit, number, x, y):
    if number == 11:
        number = 'J'
    elif number == 12:
        number = 'Q'
    elif number == 13:
        number = 'K'
    elif number == 1:
        number = 'A'
    #    ♠♥♦♣
    symbol = '♥'
    color = 'red'
    if suit == "H":
        symbol = '♥'
    elif suit == 'D':
        symbol = '♦'
    elif suit == 'C':
        color = 'black'
        symbol = '♣'
    elif suit == 'S':
        color = 'black'
        symbol = '♠'

    drawRect(x, y, 100, 150, fill="lavenderBlush", border="white", borderWidth=4)
    drawLabel(number, x+10,y+20, size=20, align="left", fill=color)
    drawLabel(number, x+90,y+130, size=20, align="right", fill=color)
    drawLabel(symbol, x+50,y+75, size=50, align="center", fill=color)

def distance(x1, x2, y1, y2):
    dx = abs(x1-x2)
    dy = abs(y1-y2)
    return ((dx**2 + dy**2)**0.5)
    
runApp()