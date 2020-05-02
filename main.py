from pathlib import Path

from AggregateData.cropCaption import CropCaption
from AggregateData.prioritize import Prioritize
from AggregateData.tokenize import Tokenize
from AggregateData.findBinomi import FindBinomi
from AggregateData.breakAnalyzer import BreakAnalyzer

from YoutubeAPI.captionDownload import CaptionDownload

if __name__ == '__main__':

    Path("Outputs").mkdir(parents=True, exist_ok=True)

    videoID = "244fChGNSkg"
    captionFileName = 'Outputs/caption.txt'
    posTag = ['S', 'N', 'A']

    if videoID:
        captionDownload = CaptionDownload('YoutubeAPI/client_secret.json')
        captionDownload.download(videoID)

        cropCaption = CropCaption()
        usableCaption = cropCaption.getUsableCaption()
        cropCaption.generateFile()
    else:
        captionFile = open(captionFileName, 'r')
        usableCaption = captionFile.read()

    tokenizer = Tokenize(usableCaption)
    sentencesWithToken = tokenizer.getTokens()
    tokenizer.generateFile()

    findBinomi = FindBinomi(sentencesWithToken)
    findBinomi.searchForTwo(posTag)
    findBinomi.generateFile()
    findBinomi.searchForThree(posTag)
    findBinomi.generateFile('trinomi')

    prioritize = Prioritize(sentencesWithToken)
    prioritize.getOrdered(posTag)
    prioritize.generateFile()

    breakAnalyzer = BreakAnalyzer(sentencesWithToken)
    breakAnalyzer.getBreaks()
    breakAnalyzer.generateFile()
