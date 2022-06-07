from datetime import datetime
import re
import os
from tqdm import tqdm
from utils import *


def getMessages(file):
    messages = Messages()
    pbar = tqdm(total=LIMIT, desc='Processing file', ncols=200)
    for line, lineNo in FileReader(file):
        pbar.update(1)
        if r'is being routed to center' in line:
            message = Message()
            message.getMgwid(line)
            message.getReceiveDate(line)
            message.type = "SEND"
            message.lineFound = lineNo
            messages.addMessage(message)

        if lineNo >= LIMIT != 0:
            break

    # messages.printAll()
    sendMessages, notifyMessages = messages.getCount()
    print(f'Found {sendMessages} send messages and {notifyMessages} notify messages')
    return messages


def countMessages(messages: Messages):
    perSecond = {}
    perMinute = {}
    perHour = {}
    for message in messages.messages:
        hourTime = str(message.receiveDate.hour)
        minuteTime = f'{hourTime}:{str(message.receiveDate.minute)}'
        secondTime = f'{minuteTime}:{str(message.receiveDate.second)}'

        if secondTime not in perSecond:
            perSecond[secondTime] = 0
        if minuteTime not in perMinute:
            perMinute[minuteTime] = 0
        if hourTime not in perHour:
            perHour[hourTime] = 0

        perSecond[secondTime] += 1
        perMinute[minuteTime] += 1
        perHour[hourTime] += 1

    return perSecond, perMinute, perHour


def getTimeStats(timeSet: dict):
    total = 0
    min = 1e5
    max = 0
    for time in timeSet:
        noMessages = timeSet[time]
        if noMessages > max:
            max = noMessages
        if noMessages < min:
            min = noMessages
        total += noMessages

    if len(timeSet) == 0:
        return 0, 0, 0
    average = total / len(timeSet)
    return average, min, max


LIMIT = 0

# Get messages from every file in files
for log in getLogsFromDir(r"C:\Users\Dave\PycharmProjects\mgwLogAnalyzer"):
    print("Processing file: " + log)
    messages = getMessages(log)
    perSecond, perMinute, perHour = countMessages(messages)
    average, min, max = getTimeStats(perSecond)
    print(f'Average messages per second: {average}')
    print(f'Min messages per second: {min}')
    print(f'Max messages per second: {max}')

    average, min, max = getTimeStats(perMinute)
    print(f'Average messages per minute: {average}')
    print(f'Min messages per minute: {min}')
    print(f'Max messages per minute: {max}')

    average, min, max = getTimeStats(perHour)
    print(f'Average messages per hour: {average}')
    print(f'Min messages per hour: {min}')
    print(f'Max messages per hour: {max}')
