import random


#Class for each leaderboard entry
class LeaderboardEntry:
    def __init__(self, name, value):
        self.name = name
        self.value = value        
    
#Class for entire leaderboard
class Leaderboard:
    def __init__(self):
        self.leaderboard = dict()
        self.loadLeaderboard()

    #Load previous leaderboard results from txt file
    def loadLeaderboard(self):
        f = open("leaderboard.txt", "r")
        data = f.read()
        if data == "":
            return
        for line in data.split("\n"):
            parts = line.split(",")
            gameId = parts[0]
            name = parts[1]
            value = int(parts[2])
            self.leaderboard[gameId] = LeaderboardEntry(name,value)
        
    #Add entry to leaderboard if score is greater than same users prev score
    def addEntry(self, gameId, name, value):
        if gameId in self.leaderboard:
            prevScore = self.leaderboard[gameId].value
            if value > prevScore:
                self.leaderboard[gameId].value = value
        else:
            newEntry = LeaderboardEntry(name, value)
            self.leaderboard[gameId] = newEntry
        self.writeLeaderBoard()
    
    #Writes leaderboard as csv to txt files
    def writeLeaderBoard(self):
        data = ""
        for key in self.leaderboard:
            entry = f"{key},{self.leaderboard[key].name},{self.leaderboard[key].value}\n"
            data += entry
        data = data[:-1]
        f = open('leaderboard.txt', 'w')
        f.write(data)        
    
    #Sorts items in dictionary based on score and returns an array
    def getLeaderboardData(self):
        sortedList = []
        scores = []
        names = []
        seenIds = set()
        for key in self.leaderboard:
            scores.append(self.leaderboard[key].value)
            names.append(self.leaderboard[key].name)
        scores = sorted(scores, reverse=True)
        for score in scores:
            for key in self.leaderboard:
                if self.leaderboard[key].value == score and key not in seenIds:
                    seenIds.add(key)
                    name = self.leaderboard[key].name
                    names.remove(name)
                    sortedList.append([name, score])
        return sortedList
    
    #Generates a hash for each user so that users in different sittings with the same name have unique rows on the leaderboard.
    def generateHash(self):
        keys = []
        for key in self.leaderboard:
            keys.append(key)
        gameId = random.getrandbits(128) #https://stackoverflow.com/questions/976577/random-hash-in-python
        while gameId in keys:
            gameId = random.getrandbits(128) #https://stackoverflow.com/questions/976577/random-hash-in-python
        return gameId
        


