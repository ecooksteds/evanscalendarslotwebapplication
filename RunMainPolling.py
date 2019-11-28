from Polling import Polling
import sys

# meetingID = sys.argv[0]
# print("Meeting ID = " + meetingID)

polling = Polling(461)

print(polling.getOpenSlot())
