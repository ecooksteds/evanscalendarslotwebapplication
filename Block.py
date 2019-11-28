class Block(object):

    def __init__(self, slotArray, length):
        self.blockDate = slotArray[0].getDate()
        self.blockStart = slotArray[0].getStartTime()
        self.blockEnd = slotArray[length-1].getEndTime()

    def getBlockDate(self):
        return self.blockDate

    def getBlockStart(self):
        return self.blockStart

    def getBlockEnd(self):
        return self.blockEnd

    def __str__(self):  # toString method
        return "{} {} {}".format(self.blockDate, self.blockStart, self.blockEnd)
