from pathlib import Path

from AggregateData.breakAnalyzer import BreakAnalyzer
from AggregateData.cropCaption import CropCaption
from AggregateData.findBinomi import FindBinomi
from AggregateData.prioritize import Prioritize
from AggregateData.tokenize import Tokenize
from YoutubeAPI.captionDownload import CaptionDownload
from YoutubeAPI.credentials import YoutubeCredentials


class ParseVideo():

    def __init__(self, directoryName: str) -> None:
        self.directoryName = directoryName
        self.usableCaption = ''
        Path('Outputs/' + self.directoryName).mkdir(parents=True, exist_ok=True)

    def getCaptionFromID(self, videoID: str, client_secretPATH: str):
        credentials = YoutubeCredentials(client_secretPATH).get()

        CaptionDownload(credentials).get(videoID, self.directoryName)

        cropCaption = CropCaption(self.directoryName)

        self.usableCaption = cropCaption.getUsableCaption()
        cropCaption.generateFile()
        return self

    def getCaptionFromFile(self, captionFileName: str):
        captionFile = open(captionFileName, 'r')
        self.usableCaption = captionFile.read()
        return self

    def parse(self, posTag=['']):
        tokenizer = Tokenize(self.usableCaption)
        sentencesWithToken = tokenizer.getTokens()
        tokenizer.generateFile(directoryName=self.directoryName)

        findBinomi = FindBinomi(sentencesWithToken)
        findBinomi.searchForTwo(posTag)
        findBinomi.generateFile(directoryName=self.directoryName)
        # findBinomi.searchForThree(posTag)
        # findBinomi.generateFile(directoryName=self.directoryName, fileName='trinomi')

        prioritize = Prioritize(sentencesWithToken)
        prioritize.getOrdered(posTag)
        prioritize.generateFile(directoryName=self.directoryName)

        breakAnalyzer = BreakAnalyzer(sentencesWithToken)
        breakAnalyzer.getBreaks()
        breakAnalyzer.generateFile(directoryName=self.directoryName)

    def parseFromTokenFile(self, lesson, posTag=['']):
        sentencesWithToken = []
        with open('Outputs/' + lesson + '/token.csv') as f:
            next(f)
            token = [line.strip().split(';') for line in f]
            for data in token:
                sentencesWithToken.append({
                    'word': data[0],
                    'time': data[1],
                    'pos': data[2],
                })

        findBinomi = FindBinomi(sentencesWithToken)
        findBinomi.searchForTwo(posTag)
        findBinomi.generateFile(directoryName=self.directoryName)
        # findBinomi.searchForThree(posTag)
        # findBinomi.generateFile(directoryName=self.directoryName, fileName='trinomi')

        prioritize = Prioritize(sentencesWithToken)
        prioritize.getOrdered(posTag)
        prioritize.generateFile(directoryName=self.directoryName)

        breakAnalyzer = BreakAnalyzer(sentencesWithToken)
        breakAnalyzer.getBreaks()
        breakAnalyzer.generateFile(directoryName=self.directoryName)
