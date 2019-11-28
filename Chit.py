class Chit(object):

    def __init__(self, date, timeStart, timeEnd, user):
        self.date = date
        self.timeStart = timeStart
        self.timeEnd = timeEnd
        self.userID = user

    def getUserID(self):
        return self.userID

    def getStartTime(self):
        return self.timeStart

    def getEndTime(self):
        return self.timeEnd

    def getDate(self):
        return self.date

    def __str__(self):  # toString method
        return "{} {} {} {}".format(self.date, self.timeStart, self.timeEnd, self.userID)