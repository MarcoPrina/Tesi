import os
from collections import defaultdict
from pathlib import Path
import math


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
                    next(f)
                    tokens = [line.rstrip() for line in f]
                    for token in tokens:
                        totalToken.write(token + ';' + lesson + '\r\n')
        return self

    def genereteCommonWords(self):
        lessons = os.listdir('Outputs')

        totLesson = 0
        commonWords = {}

        for lesson in lessons:
            if self.isALesson(lesson):
                totLesson += 1
                with open('Outputs/' + lesson + '/words.csv') as f:
                    next(f)
                    words = [line.split(';') for line in f]
                    for word in words:
                        if word[0] in commonWords:
                            commonWords[word[0]]['totCount'] += int(word[1])
                            commonWords[word[0]]['lessons'].append(lesson)
                            commonWords[word[0]]['tf-idf'][lesson] = float(word[3])
                        else:
                            commonWords[word[0]] = {
                                'word': word[0],
                                'totCount': int(word[1]),
                                'lessons': [lesson],
                                'tf-idf': {lesson: float(word[3])}
                            }

        ordered = sorted(commonWords.items(), key=lambda x: (len(x[1]['lessons']), x[1]['totCount']), reverse=True)
        self.generateFile('commonWords', ordered)
        return ordered

    def genereteCommonBinomi(self):
        lessons = os.listdir('Outputs')

        totLesson = 0
        commonBinomi = {}

        for lesson in lessons:
            if self.isALesson(lesson):
                totLesson += 1
                with open('Outputs/' + lesson + '/binomi.csv') as f:
                    next(f)
                    binomi = [line.strip().split(';') for line in f]
                    for binomio in binomi:
                        binomioWord = binomio[0]
                        if binomioWord in commonBinomi:
                            commonBinomi[binomioWord]['totCount'] += int(binomio[3])
                            commonBinomi[binomioWord]['lessons'].append(lesson)
                            commonBinomi[binomioWord]['tf-idf'][lesson] = float(binomio[4])
                        else:
                            commonBinomi[binomioWord] = {
                                'word': binomio[1],
                                'totCount': int(binomio[3]),
                                'lessons': [lesson],
                                'tf-idf': {lesson: float(binomio[4])}
                            }

        for binomio in commonBinomi:
            idf = math.log10(totLesson / len(commonBinomi[binomio]['lessons']))
            for lesson in commonBinomi[binomio]['tf-idf']:
                commonBinomi[binomio]['tf-idf'][lesson] = commonBinomi[binomio]['tf-idf'][lesson] * idf
        ordered = sorted(commonBinomi.items(), key=lambda x: (len(x[1]['lessons']), x[1]['totCount']), reverse=True)
        self.generateFile('commonBionomi', ordered)
        return ordered

    def generateFile(self, filename, words):
        if os.path.exists('Outputs/totalVideo/' + filename + '.csv'):
            os.remove('Outputs/totalVideo/' + filename + '.csv')
        commonWordsFile = open('Outputs/totalVideo/' + filename + '.csv', 'a')
        commonWordsFile.write('word' + ';' + 'in lessons' + ';' + 'tot count' + ';' + 'tf-idf' + '\r\n')
        for word in words:
            sortTfIdf = sorted(word[1]['tf-idf'].items(), key=lambda x: x[1], reverse=True)
            tfIdf = ''
            for lesson in sortTfIdf:
                tfIdf += str(lesson[0]) + ' ' + str(lesson[1]) + ';'
            commonWordsFile.write(
                word[1]['word'] +
                ';' +
                ' '.join(sorted(word[1]['lessons'], key=lambda x: int(x))) +
                ';' +
                str(word[1]['totCount']) +
                ';' +
                tfIdf +
                '\r\n')

    def isALesson(self, lesson):
        try:
            int(lesson)
            return True
        except ValueError:
            return False
