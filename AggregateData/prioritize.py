import json
import os
from collections import defaultdict


class Prioritize():

    def __init__(self, tokenizedCaptions: json) -> None:
        self.tokenizedCaptions = tokenizedCaptions
        self.ordered = []

    def getOrdered(self, posTag=['']) -> list:
        words = {}
        for sentence in self.tokenizedCaptions['sentences']:
            for token in sentence['tokens']:
                if token['word'] in words:
                    words[token['word']]['counter'] += 1
                    words[token['word']]['pos'][token['pos']] += 1
                elif token['pos'].startswith(tuple(posTag)):
                    words[token['word']] = {}
                    words[token['word']]['counter'] = 1
                    words[token['word']]['pos'] = defaultdict(int)
                    words[token['word']]['pos'][token['pos']] += 1
        self.ordered = sorted(words.items(), key=lambda x: x[1]['counter'], reverse=True)
        return self.ordered

    def generateFile(self, fileName='words'):
        if os.path.exists("Outputs/" + fileName + ".csv"):
            os.remove("Outputs/" + fileName + ".csv")
        wordsFile = open("Outputs/" + fileName + ".csv", "a")

        for word, data in self.ordered:
            ordered = sorted(data['pos'].items(), key=lambda x: x[1], reverse=True)
            wordsFile.write(word + ";" + str(data['counter']) + ";" + ordered[0][0] + '\r\n')

        wordsFile.close()