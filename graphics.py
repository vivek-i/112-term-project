import gameLogic
from cmu_graphics import *
import leaderboardLogic
from PIL import Image

def onAppStart(app):    
    app.leaderboard = leaderboardLogic.Leaderboard()
    app.screen = "home"    
    app.width = 1200
    app.height = 1000
    app.playerId = app.leaderboard.generateHash()
    app.playerBalance = 1000
    app.playerName = ""
    app.nameInput = ""
    app.gameBackground = CMUImage(Image.open('bg.png'))
    
    
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
    app.suggestion = ""

def onKeyPress(app, key):
    #Type in name
    if app.playerName == "":
        if key == "backspace":
            if len(app.nameInput) > 0:
                app.nameInput = app.nameInput[:-1]
        elif key in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ":
            if len(app.nameInput) < 15:
                app.nameInput += key
    else:
        #Restart game
        if key == 'r':
            if app.gameOver:
                if app.game.determineWinner() == "Player Wins":
                    app.playerBalance += app.betAmount*2
                if app.game.determineWinner() == "Push":
                    app.playerBalance += app.betAmount
            startGame(app)
        #For testing, show hit/stand scores for computer
        elif key == 'e':
            gameLogic.exepectiMiniMax(app.game.player, app.game.computer, app.game.playerDone)
        #show suggestion for player
        elif key == 's':
            app.suggestion = gameLogic.exepectiMiniMax(app.game.computer, app.game.player, app.game.computerDone)

def redrawAll(app):
    gold = rgb(251, 232, 139)
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
            if app.game.determineWinner() == "Player Wins":                
                app.leaderboard.addEntry(app.playerId, app.playerName, app.playerBalance + app.betAmount*2)
            elif app.game.determineWinner() == "Push":
                app.leaderboard.addEntry(app.playerId, app.playerName, app.playerBalance + app.betAmount)
            else:
                app.leaderboard.addEntry(app.playerId, app.playerName, app.playerBalance)
            drawLabel(app.result + " - Press 'r' to play another hand", app.width/2, 885, align = "center", size=35, fill=gold, font="cursive")
        if app.playerName == "":
            drawNamePopup(app)
    elif app.screen == "rules":
        drawRulesScreen(app)
    elif app.screen == "leaderboard":
        drawLeaderboardScreen(app)
    else:
        drawHomeScreen(app)
def drawNamePopup(app):
    drawRect(0,0,app.width, app.height, fill="black", opacity=80)
    drawRect(app.width/2 - 400, app.height/2-100, 800, 200, fill="white")
    drawLabel("Enter Your Name: ", app.width/2-380, app.height/2-50, fill="black", size=40, align="left")
    drawRect(app.width/2 - 380, app.height/2, 600, 50, border="black", fill="white")
    drawLabel(app.nameInput, app.width/2-360, app.height/2+25, size=30, align="left")
    drawRect(app.width/2+240, app.height/2, 140, 50, border="black", fill="white")
    drawLabel("Submit", app.width/2+310, app.height/2+25, size=30)
    

def drawRulesScreen(app):
    gold = rgb(251, 232, 139)
    drawRect(0,0,app.width, app.height, fill=rgb(34,34,34))
    drawLabel("112 Blackjack Rules", 100, 80, size=60, fill=gold, font="cursive", align="left")    
    drawLabel("- The objective is to get a hand value close to 112 without exceeding it.", 150, 160, size=25, fill="white", align="left")    
    drawLabel("- All cards have values. 2-10 are valued by their numbers. A = 1, J,Q,K = 10", 150, 200, size=25, fill="white", align="left")    
    drawLabel("- Each player gets one card to begin with", 150, 240, size=25, fill="white", align="left")    
    drawLabel("- Choose 'hit' for another card or 'stand' to keep current cards on each turn", 150, 280, size=25, fill="white", align="left")    
    drawLabel("- If a card value is 7 or less, your hand score is multiplied by that value", 150, 320, size=25, fill="white", align="left")    
    drawLabel("- If a card value is 8 or more, that value is added to your hand score", 150, 360, size=25, fill="white", align="left")    
    drawLabel("- The player with the hand valued closest to 112 without crossing wins.", 150, 400, size=25, fill="white", align="left")        
    drawLabel("- You are given $1000 to start with.", 150, 440, size=25, fill="white", align="left")    
    drawLabel("- You can bet as much of it as you want before each game.", 150, 480, size=25, fill="white", align="left")    
    drawLabel("- Winning doubles your bet.", 150, 520, size=25, fill="white", align="left")    
    drawLabel("- You cannot see the computer's top card.", 150, 560, size=25, fill="white", align="left")    
    drawLabel("- The computer cannot see your top card.", 150, 600, size=25, fill="white", align="left")    

    drawRect(app.width/2-300, 800, 200, 60, fill=None, border=gold)
    drawLabel("Back", app.width/2-200, 830, size=40, fill=gold)
    drawRect(app.width/2+100, 800, 200, 60, fill=None, border=gold)
    drawLabel("Play", app.width/2+200, 830, size=40, fill=gold)
    
def drawLeaderboardScreen(app):
    gold = rgb(251, 232, 139)
    drawRect(0,0,app.width, app.height, fill=rgb(34,34,34))
    drawLabel("Leaderboard", 100, 100, size=60, fill="white", align="left",font="cursive")    
    
    data = app.leaderboard.getLeaderboardData()
    
    numEntries = min(15, len(data))
    
    for i in range(numEntries):
        row = data[i]        
        drawLabel(f'{i+1}. {row[0]} - {row[1]}', 150, 160 + i*40, size=30, fill="white", align="left")    
    drawRect(app.width/2-300, 800, 200, 60, fill=None, border=gold)
    drawLabel("Home", app.width/2-200, 830, size=40, fill=gold)
    drawRect(app.width/2+100, 800, 200, 60, fill=None, border=gold)
    drawLabel("Play", app.width/2+200, 830, size=40, fill=gold)
    

def drawHomeScreen(app):
    gold = rgb(251, 232, 139)
    drawRect(0,0,app.width, app.height, fill=rgb(34,34,34))
    drawImage(app.gameBackground, 0, 0)
    drawLabel("112 Blackjack", app.width/2, 60, size=80, font='Cursive', fill=gold)    
    offset=80
    drawRect(app.width/2-300, 800+offset, 200, 60, fill=None, border=gold)
    drawLabel("Rules", app.width/2-200, 830+offset, size=40, fill=gold)
    drawRect(app.width/2+100, 800+offset, 200, 60, fill=None, border=gold)
    drawLabel("Play", app.width/2+200, 830+offset, size=40, fill=gold)        
    
    for i in range(1,14):
        symbols = ['C', 'H', 'C', 'D']        
        drawCard(app, symbols[i%4], i, 370 + (i-1)*30, 240+(i-1)*30)


def drawBoard(app):    
    drawRect(0,0,1200,1000,fill=rgb(34,34,34))
    gold = rgb(251, 232, 139)
    drawImage(app.gameBackground, 0, 0)
    drawLabel("112 Blackjack", app.width/2, app.height/2, size=80, fill="darkGreen", font="cursive")
    if app.betsPlaced:
        drawLabel("Player: " + str(app.game.player.getScore()), app.width * (1/4)+60, app.height-300, size=40, fill="darkGreen", font="cursive")
        if app.game.playerDone == False:
            drawLabel("Computer: " + str(app.game.computer.getBlindScore()), app.width* (3/4)-60, app.height-300, size=40, fill="darkGreen", font="cursive")
        else:
            drawLabel("Computer: " + str(app.game.computer.getScore()), app.width* (3/4)-60, app.height-300, size=40, fill="darkGreen", font="cursive")
    if app.playerName != "":
        drawLabel(f"{app.playerName}'s Balance: {app.playerBalance}" , 20, 30, size=30, align="left", fill=gold)
        
    drawRect(app.width-220, 20, 200, 60, fill=None, border=gold)
    drawLabel("Leaderboard", app.width-120, 50, size=30, fill=gold)

def drawOptions(app):
    gold = rgb(251, 232, 139)
    offset=70
    if app.suggestion == "hit":
        drawRect(110,820+offset,180,50, fill=gold, border=gold)
        drawLabel("Hit", 200,845+offset, size=20, fill="black")
        drawRect(310,820+offset,180,50, fill=None, border=gold)
        drawLabel("Stand", 400,845+offset, size=20, fill=gold)
    elif app.suggestion == "stand":
        drawRect(110,820+offset,180,50, fill=None, border=gold)
        drawLabel("Hit", 200,845+offset, size=20, fill=gold)
        drawRect(310,820+offset,180,50, fill=gold, border=gold)
        drawLabel("Stand", 400,845+offset, size=20, fill="black")
    else:
        drawRect(110,820+offset,180,50, fill=None, border=gold)
        drawLabel("Hit", 200,845+offset, size=20, fill=gold)
        drawRect(310,820+offset,180,50, fill=None, border=gold)
        drawLabel("Stand", 400,845+offset, size=20, fill=gold)
        
    drawLabel("Press 's' for a Suggestion", 1150, 950, size=25, fill=gold, align="right")

def drawBettingOptions(app):
    offset = 50
    gold = rgb(251, 232, 139)
    drawRect(app.width/2-80, 820+offset, 160, 50, border=gold, fill=None)
    drawLabel(str(app.betAmount), app.width/2, 845+offset, size=25, fill=gold)
    drawCircle(app.width/2-120, 845+offset, 25, border=gold, fill=None)
    drawLabel("-", app.width/2-120, 849+offset, size=30, fill=gold)
    drawCircle(app.width/2+120, 845+offset, 25, border=gold, fill=None)
    drawLabel("+", app.width/2+120, 847+offset, size=30, fill=gold)
    drawRect(app.width/2-40, 885+offset, 80, 30, fill=gold)
    drawLabel("Bet", app.width/2, 900+offset, size=25, fill="black")
    

def drawBlankCard(app, x, y):
    drawRect(x, y, 100, 150, fill="pink", border="white", borderWidth=4)

def onMousePress(app, mouseX, mouseY):
    if app.screen == "home":
        offset=80
        #Rules Screen
        if mouseX >= app.width/2-300 and mouseX <= app.width/2-100 and mouseY >= 800+offset and mouseY <= 860+offset:
            app.screen="rules"
        #Start Game
        elif mouseX >= app.width/2+100 and mouseX <= app.width/2+300 and mouseY >= 800+offset and mouseY <= 860+offset:
            app.screen="game"
            startGame(app)    
    elif app.screen == "game":
        #Submit Name
        if app.playerName == "":        
            if mouseX >= app.width/2+240 and mouseX <= app.width/2+380 and mouseY >= app.height/2 and mouseY <= app.height/2+50:
                if app.nameInput != "":
                    app.playerName = app.nameInput
                    app.leaderboard.addEntry(app.playerId, app.playerName, app.playerBalance)
                    app.nameInput = ""    
        else:
            #Go to leaderboard
            if mouseX >= app.width-220 and mouseX <= app.width-20 and mouseY >= 20 and mouseY <= 60:
                app.screen = "leaderboard"                        
            if app.betsPlaced == True:
                offset=70
                #Hit
                if mouseX >= 110 and mouseX <= 290 and mouseY >= 820+offset and mouseY <= 870+offset:
                    app.suggestion = ""
                    app.game.playerHit()
                    app.game.makeComputerMove()
                #Stand
                elif mouseX >= 310 and mouseX <= 490 and mouseY >= 820+offset and mouseY <= 870+offset:
                    app.suggestion = ""
                    app.game.playerStand()
                    app.game.makeComputerMove()
                #Check Game State
                if not(app.game.determineWinner() == "In Progress"):
                    app.result = app.game.determineWinner()
                    app.gameOver = True        
            else:
                betSize = 10
                offset = 50
                if app.playerBalance <= 20:
                    betSize = 1
                #Decrease bet
                if distance(mouseX, app.width/2-120, mouseY, 845+offset) <= 25:
                    if app.betAmount >= betSize:
                        app.betAmount -= betSize
                #Increase Bet
                elif distance(mouseX, app.width/2+120, mouseY, 845+offset) <= 25:
                    if app.betAmount <= app.playerBalance - betSize:
                        app.betAmount += betSize
                        
                #Submit Bet
                elif mouseX >= app.width/2-40 and mouseX <= app.width/2+40 and mouseY >= 885+offset and mouseY <= 915+offset:
                    app.playerBalance -= app.betAmount
                    app.betsPlaced = True                       
    elif app.screen == "rules":
        #Return Home
        if mouseX >= app.width/2-300 and mouseX <= app.width/2-100 and mouseY >= 800 and mouseY <= 860:
            app.screen="home"
        #Start Game
        elif mouseX >= app.width/2+100 and mouseX <= app.width/2+300 and mouseY >= 800 and mouseY <= 860:
            app.screen="game"
            startGame(app)
    elif app.screen == "leaderboard":
        #Return Home
        if mouseX >= app.width/2-300 and mouseX <= app.width/2-100 and mouseY >= 800 and mouseY <= 860:
            app.playerName = ""
            app.playerId = app.leaderboard.generateHash()
            app.playerBalance = 1000
            app.screen="home"
        #Start Game
        elif mouseX >= app.width/2+100 and mouseX <= app.width/2+300 and mouseY >= 800 and mouseY <= 860:
            app.playerName = ""
            app.playerId = app.leaderboard.generateHash()
            app.playerBalance = 1000
            app.screen = "game"
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