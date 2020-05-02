import json
import os
from collections import defaultdict
from datetime import datetime


class BreakAnalyzer():

    def __init__(self, tokenizedCaptions: json) -> None:
        self.tokenizedCaptions = tokenizedCaptions
        self.timePattern = '%H:%M:%S.%f'
        self.orderedBreaks = []

    def getBreaks(self):
        pre = {}
        first = True
        breaks = []
        for sentence in self.tokenizedCaptions['sentences']:
            for token in sentence['tokens']:
                if first:
                    first = False
                    pre = token
                else:
                    start = datetime.strptime(pre['time'], self.timePattern)
                    end = datetime.strptime(token['time'], self.timePattern)
                    timeBreak = end - start
                    breaks.append({'break': timeBreak.__str__(), 'start': pre['time']})
                    pre = token

        self.orderedBreaks = sorted(breaks, key=lambda x: x['break'], reverse=True)
        return self.orderedBreaks

    def generateFile(self, fileName='breaks'):
        if os.path.exists("Outputs/" + fileName + ".csv"):
            os.remove("Outputs/" + fileName + ".csv")
        breaksFile = open("Outputs/" + fileName + ".csv", "a")

        breaksFile.write('durata' + ';' + 'inizio' + '\r\n')

        for timeBreak in self.orderedBreaks:
            breaksFile.write(timeBreak['break'] + ';' + timeBreak['start'] + '\r\n')
