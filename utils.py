from datetime import datetime
import os
import re


class Messages:
    def __init__(self):
        self.messages = []

    def addMessage(self, message):
        if not self.hasMessage(message.mgwid):
            self.messages.append(message)

    def hasMessage(self, mgwid):
        for message in self.messages:
            if message.mgwid == mgwid:
                return True
        return False

    def printAll(self):
        for message in self.messages:
            print(str(message))

    def getCount(self):
        sendMessages = 0
        notifyMessages = 0

        for message in self.messages:
            if message.type == 'SEND':
                sendMessages += 1
            elif message.type == 'NOTIFY':
                notifyMessages += 1

        return sendMessages, notifyMessages


class Message:
    def __init__(self):
        self.receiveDate = None
        self.mgwid = None
        self.type = None
        self.line = ""
        self.lineFound = 0

    def getMgwid(self, line):
        search = re.search(r'mgwid ([a-zA-Z0-9]+)', line)
        self.mgwid = self._getIfExists(search)

    def getReceiveDate(self, line):
        search = re.search(r'\d\d:\d\d:\d\d\.\d\d\d', line)
        self.receiveDate = self._getIfExists(search)
        self.receiveDate = datetime.strptime(self.receiveDate, '%H:%M:%S.%f')

    def _getIfExists(self, search):
        if search is not None:
            return search.group(0)
        else:
            return '00:00:00.000'


def getLogsFromDir(dir):
    logs = []
    # Find all files with the .log extension in root
    for root, dirs, files in os.walk(dir):
        for file in files:
            if file.endswith(".log"):
                logs.append(os.path.join(root, file))
    return logs


def FileReader(file):
    with open(file, 'r', encoding="utf-8") as f:
        for lineNo, line in enumerate(f):
            try: yield line, lineNo
            except UnicodeEncodeError as e: continue
