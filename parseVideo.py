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

    def getCaptionFromID(self, videoID:str, client_secretPATH: str):
        youtubeCredentials = YoutubeCredentials(client_secretPATH)
        credentials = youtubeCredentials.get()
        captionDownload = CaptionDownload(credentials)
        captionDownload.get(videoID, self.directoryName)

        cropCaption = CropCaption(self.directoryName)
        cropCaption.generateFile()
        self.usableCaption = cropCaption.getUsableCaption()
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
        findBinomi.searchForThree(posTag)
        findBinomi.generateFile(directoryName=self.directoryName, fileName='trinomi')

        prioritize = Prioritize(sentencesWithToken)
        prioritize.getOrdered(posTag)
        prioritize.generateFile(directoryName=self.directoryName)

        breakAnalyzer = BreakAnalyzer(sentencesWithToken)
        breakAnalyzer.getBreaks()
        breakAnalyzer.generateFile(directoryName=self.directoryName)
