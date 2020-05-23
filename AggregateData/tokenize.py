import json
import os
import re
import subprocess

from tqdm import tqdm

import time

import requests


class Tokenize():

    def __init__(self, usableCaption: str) -> None:
        self.sentencesWithToken = {}
        self.usableCaption = usableCaption.replace('\r\n', '\r').replace('\n', '\r')

    def getTokens(self) -> json:
        self.startTint()
        file = self.usableCaption.split('\r')
        tokenized = { "sentences": []}
        with tqdm(total=len(file)) as pbar:
            for index, line in enumerate(file):
                pbar.update(1)
                if line:
                    sentence = self.posLine(line)["sentences"][0]
                    sentence['index'] = index
                    remainingLine = line
                    time = ''
                    for token in sentence["tokens"]:
                        word = token['word']
                        lineParts = remainingLine.split(word, 1)
                        if len(lineParts) > 1 and lineParts[1]:
                            remainingLine = remainingLine.split(word, 1)[1].strip()
                            if '<' in remainingLine:
                                time = remainingLine[remainingLine.find('<')+1:].split('>', 1)[0]
                        token['time'] = time
                    tokenized["sentences"].append(sentence)

        self.sentencesWithToken = tokenized
        return tokenized


    def posLine(self, line) -> json:
        parsedLine = self.parseLine(line)
        parameters = {"text": parsedLine}
        response = requests.get("http://localhost:8012/tint", params=parameters)
        return response.json()

    def parseLine(self, line) -> str:
        parsedLine = line.replace("\\n", "").replace("\\r", "")
        return re.sub(r"<([^<>]*)>", "", parsedLine)

    def startTint(self):
        try:
            parameters = {"text": 'test'}
            response = requests.get("http://localhost:8012/tint", params=parameters)
        except:
            subprocess.Popen(["./tint/tint-server.sh", "-c", "./tint/sampleProps.properties"])
            time.sleep(7)

    def generateFile(self, directoryName: str, fileName='token'):
        if os.path.exists('Outputs/' + directoryName + "/" + fileName +".csv"):
            os.remove('Outputs/' + directoryName + "/" + fileName +".csv")
        tokenFile = open('Outputs/' + directoryName + "/" + fileName +".csv", "a")
        for sentence in self.sentencesWithToken['sentences']:
            for token in sentence['tokens']:
                tokenFile.write(token['word'] + ';' + token['time'] + ';' + token['pos'] + '\r\n')
        tokenFile.close()



