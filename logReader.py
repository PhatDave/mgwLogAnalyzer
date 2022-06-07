from utils import *
from tqdm import tqdm

timeFrames = [
	[8, 6, 0],
]


def formatTimeFrame(timeFrame):
	return '{}-{}-{}'.format(timeFrame[0], timeFrame[1], timeFrame[2])


# Read files whose names are reflected in the timeFrames list
fileGenerators = []
files = []
for timeFrame in timeFrames:
	fileName = formatTimeFrame(timeFrame)
	files.append(fileName)
	fileGenerator = FileReader(f'{fileName}.log')
	fileGenerators.append(fileGenerator)

pbar = tqdm()
for i, gen in enumerate(fileGenerators):
	first = False
	firstMessage = False
	maxLine = 0
	lastLine = ""
	for line, lineNo in gen:
		pbar.update(1)
		if not first:
			first = True
			print(f'First line of file {files[i]} is\n{line}')
		if not firstMessage and 'is being routed to center' in line:
			firstMessage = True
			print(f'First message of file {files[i]} is\n{line}')
		if lineNo > maxLine:
			maxLine = lineNo
			lastLine = line
	print(f'Last line of file {files[i]} is\n{lastLine}')
