import os
from multiprocessing import Process
from more_itertools import pairwise
from tqdm import tqdm

from utils import *

root = r'C:\Users\Dave\Documents\mgw3-logs'
logs = getLogsFromDir(root)
# logs = [r'C:\Users\Dave\Documents\mgw3-logs\smallSection.log']

timeFrames = [
    # datetime.strptime('-'.join(['12', '13', '30']), '%H-%M-%S'),
    # datetime.strptime('-'.join(['12', '23', '00']), '%H-%M-%S'),
    # datetime.strptime('-'.join(['12', '27', '00']), '%H-%M-%S'),
    # datetime.strptime('-'.join(['12', '28', '30']), '%H-%M-%S'),
    # datetime.strptime('-'.join(['12', '30', '30']), '%H-%M-%S'),
    # datetime.strptime('-'.join(['12', '43', '30']), '%H-%M-%S'),
    # datetime.strptime('-'.join(['12', '56', '30']), '%H-%M-%S'),
    # datetime.strptime('-'.join(['13', '1', '00']), '%H-%M-%S'),
    # datetime.strptime('-'.join(['13', '4', '30']), '%H-%M-%S'),
    # datetime.strptime('-'.join(['13', '8', '30']), '%H-%M-%S'),
    # datetime.strptime('-'.join(['13', '23', '30']), '%H-%M-%S'),
    # datetime.strptime('-'.join(['13', '25', '30']), '%H-%M-%S'),
    datetime.strptime('-'.join(['8', '06', '00']), '%H-%M-%S'),
    datetime.strptime('-'.join(['8', '16', '00']), '%H-%M-%S'),
]


def formatTimeFrame(timeFrame):
    return f'{timeFrame.hour}-{timeFrame.minute}-{timeFrame.second}'


class MessageSet:
    def __init__(self, timeFrame):
        self.timeFrame = timeFrame
        self.messages = []

    # Save messages to file whose name is derived from timeFrame
    def save(self):
        print("Saving messages for time frame: " + str(self.timeFrame))
        fileName = f'{formatTimeFrame(self.timeFrame)}.log'
        with open(fileName, 'w', encoding='utf-8') as f:
            for message in self.messages:
                f.write(message.line)

    def sort(self):
        self.messages.sort(key=lambda x: x.receiveDate)

    def addMessage(self, message: Message):
        self.messages.append(message)


messageSets = {}
for timeFrame in timeFrames:
    formatTime = formatTimeFrame(timeFrame)
    open(f'{formatTime}.log', 'w').close()
    messageSets[formatTime] = MessageSet(timeFrame)

for log in logs:
    generator = FileReader(log)
    pbar = tqdm(ncols=200, desc=log)
    for line, lineNo in generator:
        pbar.update(1)
        message = Message()
        message.getReceiveDate(line)
        for timeFrame in pairwise(timeFrames):
            after = timeFrame[0]
            before = timeFrame[1]
            if after < message.receiveDate < before:
                message.line = line
                messageSets[formatTimeFrame(timeFrame[0])].addMessage(message)
                break

for messageSet in messageSets.values():
    messageSet.sort()
    messageSet.save()
