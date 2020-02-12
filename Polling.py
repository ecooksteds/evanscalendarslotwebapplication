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




        for block in self.globalBlockList[0]:
            print(block)

    def getOpenBlock(self):
        #for block in globalBlockList[0]:
            #result = self.matchExists(block)
            #if result == True:
                #match = True
                #break
        #if result == False:
            #return "No Compatible Block"
        #else:
            #print(block)
            #return block

        return "No Compatible Slot"

    def matchExists(self, blockLocationInGlobalBlockList):
        #block = blockLocationInGlobalBlockList
        #listLength = 0
        #if another list exists:
            #for compBlock in list:
                #length += 1
                #if block matches compBlock:
                    #matchExists(compBlock)
                #elif length <= nextList:
                    #return false
        #else:
            #if block matches compBlock:
                #result = True
            #else:
                #result = false
        #return result
        return None


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

    def sortChits(self, chitArray):
        for index in range(len(chitArray)):
            for j in range(len(chitArray) - index - 1):
                if chitArray[j].getStartTime() > chitArray[j+1].getStartTime():
                    temp = chitArray[j]
                    chitArray[j] = chitArray[j+1]
                    chitArray[j+1] = temp


        return chitArray


    def getMeetingLength(self):
        db = pymysql.connect(host = "us-cdbr-iron-east-05.cleardb.net", user = "b15bfd522a38aa", password = "d436c805", database = "heroku_66bd76f57e3f221")
        cursor = db.cursor()

        cursor.execute("SELECT meetingLength FROM meeting WHERE meetingID = %s", [self.meeting])
        lengthTuple = cursor.fetchone()
        length = int(lengthTuple[0])
        print(length)
        db.commit()
        cursor.close()
        db.close()

        return length

    def buildBlockList(self, chitList):
        blockList = []
        sortedChitList = self.sortChits(chitList)
        index = 0
        nextIndex = 1
        while nextIndex < len(sortedChitList):
            currentChit = sortedChitList[index]
            miniSlotList = []
            miniSlotList.append(currentChit)
            blockLength = 1
            miniIndex = index
            miniNextIndex = nextIndex
            while blockLength != self.length and miniNextIndex < len(sortedChitList):
                print(blockLength)
                if sortedChitList[miniIndex].getDate() == sortedChitList[miniNextIndex].getDate():
                    if sortedChitList[miniIndex].getEndTime() == sortedChitList[miniNextIndex].getStartTime():
                        miniSlotList.append(sortedChitList[miniNextIndex])
                        blockLength += 1
                        miniIndex += 1
                        miniNextIndex +=1
                    else:
                        miniSlotList = [sortedChitList[miniNextIndex]]
                        miniIndex += 1
                        miniNextIndex += 1
                        blockLength = 1

            if blockLength == self.length:
                #print(miniSlotList)
                tempBlock = Block(miniSlotList, self.length)
                blockList.append(tempBlock)
            index += 1
            nextIndex += 1

        return blockList

    def buildGlobalBlockList(self):
        globalBlockList = []
        for list in self.globalChitList:
            tempList = self.buildBlockList(list)
            globalBlockList.append(tempList)

        return globalBlockList

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




