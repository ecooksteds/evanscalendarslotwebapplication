from Chit import Chit
class Slot(object):

    def __init__(self, slotTuple):
        self.slotTuple = slotTuple
        self.day = slotTuple[0]
        self.date = slotTuple[1]
        self.timeStart = slotTuple[2]
        self.timeEnd = slotTuple[3]
        self.userID = slotTuple[4]

    def parseTimeString(self, unParsedString):
        timeString = unParsedString[0] + unParsedString[1] + unParsedString[3] + unParsedString[4]
        timeInt = int(timeString)
        AMPMString = unParsedString[5] + unParsedString[6]
        if AMPMString == "pm":
            timeInt += 1200

        return timeInt

    def convertToChitsList(self):
        chitList = []
        leftBoundInt = self.parseTimeString(self.timeStart)
        rightBoundInt = self.parseTimeString(self.timeEnd)
        curr = leftBoundInt
        next = leftBoundInt + 15
        while next <= rightBoundInt:
            tempChit = Chit(self.date, curr, next, self.userID)
            chitList.append(tempChit)
            curr += 15
            next += 15
            if (next - 60) % 100 == 0:
                next += 40
            if (curr - 60) % 100 == 0:
                curr += 40

        return chitList





    def getDay(self):
        return self.day

    def getDate(self):
        return self.date

    def getTimeStart(self):
        return self.timeStart

    def getTimeEnd(self):
        return self.timeEnd

    def getUserID(self):
        return self.userID

    def __str__(self):  # toString method
        return "{} {} {} {}".format(self.day, self.date, self.timeStart, self.timeEnd)