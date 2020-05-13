import os
from pathlib import Path


class AggregateVideos():

    def __init__(self) -> None:
        Path("Outputs/totalVideo").mkdir(parents=True, exist_ok=True)

    def genereteTotalTokens(self):
        lessons = os.listdir('Outputs')

        if os.path.exists('Outputs/totalVideo/totalToken.csv'):
            os.remove('Outputs/totalVideo/totalToken.csv')
        totalToken = open('Outputs/totalVideo/totalToken.csv', 'a')

        for lesson in lessons:
            if self.isALesson(lesson):
                with open('Outputs/' + lesson + '/token.csv') as f:
                    tokens = [line.rstrip() for line in f]
                    for token in tokens:
                        totalToken.write(token + ';' + lesson + '\r\n')
        return self

    def genereteCommonWords(self):
        lessons = os.listdir('Outputs')

        commonWords = {}

        for lesson in lessons:
            if self.isALesson(lesson):
                with open('Outputs/' + lesson + '/words.csv') as f:
                    words = [line.split(';') for line in f]
                    for word in words:
                        if word[0] in commonWords:
                            commonWords[word[0]]['totCount'] += int(word[1])
                            commonWords[word[0]]['lessons'].append(lesson)
                        else:
                            commonWords[word[0]] = {'word': word[0], 'totCount': int(word[1]), 'lessons': [lesson]}

        ordered = sorted(commonWords.items(), key=lambda x: (len(x[1]['lessons']), x[1]['totCount']), reverse=True)
        self.generateFile('commonWords', ordered)
        return ordered

    def genereteCommonBinomi(self):
        lessons = os.listdir('Outputs')

        commonBinomi = {}

        for lesson in lessons:
            if self.isALesson(lesson):
                with open('Outputs/' + lesson + '/binomi.csv') as f:
                    binomi = [line.strip().split(';') for line in f]
                    for binomio in binomi:
                        binomioWord = binomio[0] + ' ' + binomio[2]
                        if binomioWord in commonBinomi and lesson not in commonBinomi[binomioWord]['lessons']:
                            commonBinomi[binomioWord]['totCount'] += int(binomio[4])
                            commonBinomi[binomioWord]['lessons'].append(lesson)
                        else:
                            commonBinomi[binomioWord] = {'binomio': binomioWord, 'totCount': int(binomio[4]), 'lessons': [lesson]}

        ordered = sorted(commonBinomi.items(), key=lambda x: (len(x[1]['lessons']), x[1]['totCount']), reverse=True)
        self.generateFile('commonBionomi', ordered)
        return ordered

    def generateFile(self, filename, words):
        if os.path.exists('Outputs/totalVideo/' + filename + '.csv'):
            os.remove('Outputs/totalVideo/' + filename + '.csv')
        commonWordsFile = open('Outputs/totalVideo/' + filename + '.csv', 'a')
        commonWordsFile.write('word' + ';' + 'in lessons' + ';' + 'tot count' + '\r\n')
        for word in words:
            commonWordsFile.write(word[0] + ';' + ','.join(sorted(word[1]['lessons'], key=lambda x: int(x))) + ';' + str(word[1]['totCount']) + '\r\n')

    def isALesson(self, lesson):
        try:
            int(lesson)
            return True
        except ValueError:
            return False
