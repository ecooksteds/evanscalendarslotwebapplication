from Slot import Slot
import pymysql.cursors
from Block import Block

class Polling():

    def __init__(self, meetingID):
        self.meeting = meetingID
        self.usersList = self.populateUsersList()
        self.length = self.getMeetingLength()
        self.allChits = self.buildAllChitList()
        self.globalChitList = self.buildGlobalChitList()
        self.globalBlockList = self.buildGlobalBlockList()

        for block in self.globalChitList[0]:
            print(block)

    # def getOpenBlock(self):
    #     for i in self.user1List:
    #         checkDay = i.getDay()
    #         checkDate = i.getDate()
    #         checkTimeStart = i.getTimeStart()
    #         for j in self.user2List:
    #             if(j.getDay()== checkDay):
    #                 if(j.getDate()==checkDate):
    #                     if(j.getTimeStart() == checkTimeStart):
    #                         return "Best Slot Offer: " + str(i)
    #     return "No Compatible Slot"


    def populateUsersList(self):
        db = pymysql.connect(host = "us-cdbr-iron-east-05.cleardb.net", user = "b15bfd522a38aa", password = "d436c805", database = "heroku_66bd76f57e3f221")
        cursor = db.cursor()

        cursor.execute("SELECT invitees FROM meeting WHERE meetingID = %s", [self.meeting])
        usersTuple = cursor.fetchone()
        userString = usersTuple[0]
        usersList = userString.split(',')
        cursor.close()

        cursor2 = db.cursor()
        cursor2.execute("SELECT invitationFrom from meeting where meetingID = %s", [self.meeting])
        inviterTuple = cursor2.fetchone()
        inviterString = inviterTuple[0]
        cursor2.close()
        db.close()
        usersList.append(inviterString)

        return usersList

    def getMeetingLength(self):
        db = pymysql.connect(host = "us-cdbr-iron-east-05.cleardb.net", user = "b15bfd522a38aa", password = "d436c805", database = "heroku_66bd76f57e3f221")
        cursor = db.cursor()

        cursor.execute("SELECT meetingLength FROM meeting WHERE meetingID = %s", [self.meeting])
        lengthTuple = cursor.fetchone()
        length = int(lengthTuple[0])
        db.commit()
        cursor.close()
        db.close()

        return length

    def buildBlockList(self, chitList):
        blockList = []
        sortedChitList = self.sortChits(chitList)

        for index in range(len(sortedChitList) - 1):
            currentChit = sortedChitList[index - 1]
            nextChit = sortedChitList[index]
            miniSlotList = []
            miniSlotList.append(currentChit)
            blockLength = 1
            miniIndex = index
            miniNextIndex = index + 1
            while blockLength != self.length and blockLength != -1 and miniNextIndex >= len(sortedChitList):
                if sortedChitList[miniIndex].getDate() == sortedChitList[miniNextIndex].getDate():
                    if sortedChitList[miniIndex].getEndTime() == sortedChitList[miniNextIndex].getStartTime():
                        miniSlotList.append(nextChit)
                        blockLength += 1
                        miniIndex += 1
                        miniNextIndex +=1
                else:
                    blockLength = -1

            if blockLength == self.length:
                tempBlock = Block(miniSlotList, self.length)
                blockList.append(tempBlock)



        return blockList

    def buildGlobalBlockList(self):
        globalBlockList = []
        for list in self.globalChitList:
            tempList = self.buildBlockList(list)
            globalBlockList.append(tempList)

        return globalBlockList

    def sortChits(self, chitArray):
        for index in range(len(chitArray)):
            for j in range(len(chitArray) - index - 1):
                if chitArray[j].getStartTime() > chitArray[j+1].getStartTime():
                    temp = chitArray[j]
                    chitArray[j] = chitArray[j+1]
                    chitArray[j+1] = temp

        return chitArray

    def buildAllChitList(self):
        tempAllChitList = []
        db = pymysql.connect(host="us-cdbr-iron-east-05.cleardb.net", user="b15bfd522a38aa", password="d436c805",
                             database="heroku_66bd76f57e3f221")
        cursor = db.cursor()

        cursor.execute("SELECT * FROM slot WHERE meetingID = %s", [self.meeting])
        allSlots = cursor.fetchall()

        for slot in allSlots:
            tempSlot = Slot(slot)
            tempChitList = tempSlot.convertToChitsList()
            for chit in tempChitList:
                tempAllChitList.append(chit)

        cursor.close()
        db.close()

        return tempAllChitList

    def buildGlobalChitList(self):
        bigChitList = []
        for user in self.usersList:
            tempChitList = []
            for chit in self.allChits:
                if chit.getUserID() == user:
                    tempChitList.append(chit)
            bigChitList.append(tempChitList)

        return bigChitList




