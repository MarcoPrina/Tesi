import json
import os
from collections import defaultdict


class FindBinomi():

    def __init__(self, tokenizedCaptions: json) -> None:
        self.binomi = []
        self.tokenizedCaptions = tokenizedCaptions

    def searchForTwo(self, posTag=['']) -> json:
        self.binomi = []
        pre = {}
        first = True
        buffBinomi = defaultdict(int)
        for sentence in self.tokenizedCaptions['sentences']:
            for token in sentence['tokens']:
                if first and token['pos'].startswith(tuple(posTag)):
                    first = False
                    pre = token
                elif token['pos'].startswith(tuple(posTag)):
                    buffBinomi[pre['word'] + ';' + pre['pos'] + ';' + token['word'] + ';' + token['pos']] += 1
                    pre = token
        self.binomi = sorted(buffBinomi.items(), key=lambda x: x[1], reverse=True)
        return self.binomi

    def searchForThree(self, posTag=['']) -> json:
        self.binomi = []
        pre0 = {}
        pre1 = {}
        first = True
        second = False
        buffBinomi = defaultdict(int)
        for sentence in self.tokenizedCaptions['sentences']:
            for token in sentence['tokens']:
                if first and token['pos'].startswith(tuple(posTag)):
                    first = False
                    second = True
                    pre0 = token
                elif second and token['pos'].startswith(tuple(posTag)):
                    second = False
                    pre1 = token
                elif token['pos'].startswith(tuple(posTag)):
                    buffBinomi[pre0['word'] + ';' + pre0['pos'] + ';' + pre1['word'] + ';' + pre1['pos'] + ';' + token['word'] + ';' + token['pos']] += 1
                    pre0 = pre1
                    pre1 = token
        self.binomi = sorted(buffBinomi.items(), key=lambda x: x[1], reverse=True)
        return self.binomi

    def generateFile(self, directoryName: str, fileName='binomi'):
        if os.path.exists('Outputs/' + directoryName + "/" + fileName + ".csv"):
            os.remove('Outputs/' + directoryName + "/" + fileName + ".csv")
        binomiFile = open('Outputs/' + directoryName + "/" + fileName + ".csv", "a")

        for binomio, count in self.binomi:
            binomiFile.write(binomio + ';' + str(count) + '\r\n')


