from pathlib import Path

from AggregateData.breakAnalyzer import BreakAnalyzer
from AggregateData.cropCaption import CropCaption
from AggregateData.findBinomi import FindBinomi
from AggregateData.lda import LDA
from AggregateData.prioritize import Prioritize
from AggregateData.tokenize import Tokenize
from YoutubeAPI.captionDownload import CaptionDownload
from YoutubeAPI.credentials import YoutubeCredentials
from YoutubeAPI.speech2text import Speech2Text
from YoutubeAPI.video2audio import Video2audio


class ParseVideo():

    def __init__(self, directoryName: str) -> None:
        self.directoryName = directoryName
        self.usableCaption = ''
        Path('Outputs/' + self.directoryName).mkdir(parents=True, exist_ok=True)

    def getCaptionFromVideo(self, videoName: str, pathCredentials: str):
        speech = Speech2Text(pathCredentials)
        # Video2audio().processVideo(videoName)
        audioName = videoName + '.flac'
        # speech.upload_blob(audioName)
        speech.sample_long_running_recognize(audioName)
        speech

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

    def parseFromCaption(self, posTag=['']):
        tokenizer = Tokenize(self.usableCaption)
        sentencesWithToken = tokenizer.getTokens()
        tokenizer.generateFile(directoryName=self.directoryName)

        self.parse(posTag, sentencesWithToken)

    def parseFromTokenFile(self, posTag=['']):
        sentencesWithToken = []
        with open('Outputs/' + self.directoryName + '/token.csv') as f:
            next(f)
            token = [line.strip().split(';') for line in f]
            for data in token:
                sentencesWithToken.append({
                    'word': data[0],
                    'time': data[1],
                    'pos': data[2],
                })

        self.parse(posTag, sentencesWithToken)


    def parse(self, posTag, sentencesWithToken):

        findBinomi = FindBinomi(sentencesWithToken)
        findBinomi.searchForTwo(posTag)
        findBinomi.generateFile(directoryName=self.directoryName)

        prioritize = Prioritize(sentencesWithToken)
        prioritize.getOrdered(posTag)
        prioritize.generateFile(directoryName=self.directoryName)

        breakAnalyzer = BreakAnalyzer(sentencesWithToken)
        breakAnalyzer.getBreaks()
        breakAnalyzer.generateFile(directoryName=self.directoryName)

        lda = LDA()
        lda.findTopic(sentencesWithToken, posTag=posTag, nTopic=8)
        lda.generateFile(directoryName=self.directoryName)
        #lda.display()
