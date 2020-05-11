import os
from collections import defaultdict


class AggregateVideos():

    def genereteTotalTokens(self):
        lessons = os.listdir('Outputs')

        if os.path.exists('totalToken.csv'):
            os.remove('totalToken.csv')
        totalToken = open('totalToken.csv', 'a')

        for lesson in lessons:
            with open('Outputs/' + lesson + '/token.csv') as f:
                tokens = [line.rstrip() for line in f]
                for token in tokens:
                    totalToken.write(token + ';' + lesson + '\r\n')
        return self

    def genereteCommonWords(self):
        lessons = os.listdir('Outputs')

        if os.path.exists('commonWords.csv'):
            os.remove('commonWords.csv')
        commonWordsFile = open('commonWords.csv', 'a')
        commonWords = defaultdict(int)

        for lesson in lessons:
            with open('Outputs/' + lesson + '/words.csv') as f:
                words = [line.split(';')[0] for line in f]
                for word in words:
                    commonWords[word] += 1

        ordered = sorted(commonWords.items(), key=lambda x: x[1], reverse=True)
        for word in ordered:
            commonWordsFile.write(word[0] + ';' + str(word[1]) + '\r\n')
