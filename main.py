import os
from pathlib import Path

from AggregateData.aggregateVideos import AggregateVideos
from AggregateData.lda import LDA
from YoutubeAPI.credentials import YoutubeCredentials
from YoutubeAPI.playlistData import PlaylistData
from parseVideo import ParseVideo

if __name__ == '__main__':

    playlistID = ''  # 'PLdrYmPSKBRMwcxumBOfPci1hFBg7Q_Nnw'  # 'PLdrYmPSKBRMzHYgtsF0efrW5dtfvg7uwM'
    posTag = ['S', 'A']
    client_secretPATH = 'YoutubeAPI/client_secret.json'

    Path("Outputs").mkdir(parents=True, exist_ok=True)
    # ParseVideo('1').getCaptionFromFile('Outputs/' + '1' + '/caption.txt').parse(posTag)

    if playlistID:
        credential = YoutubeCredentials(client_secretPATH).get()
        playlist = PlaylistData(credential).get(playlistID).askLessons().playlist

        for video in playlist:
            parseVideo = ParseVideo(str(video['lesson']))
            # parseVideo.getCaptionFromID(video['videoId'], client_secretPATH).parse(posTag)
            parseVideo.getCaptionFromFile('Outputs/' + str(video['lesson']) + '/caption.txt').parse(posTag)
            # parseVideo.parseFromTokenFile(str(video['lesson']), posTag)
            print('Elaborata lezione ', str(video['lesson']))

    # AggregateVideos().genereteCommonWords()
    # AggregateVideos().genereteCommonBinomi()

    sentencesWithToken = []
    with open('Outputs/1/token.csv') as f:
        next(f)
        token = [line.strip().split(';') for line in f]
        for data in token:
            if data[2].startswith(tuple(posTag)):
                sentencesWithToken.append(data[0][:-1])

    lda = LDA()
    lda.findTopic([d.split() for d in sentencesWithToken], nTopic=5)
    lda.display()

"""
    videoID = "THNwJlawXic"
    captionFileName = 'Outputs/caption.txt'
    posTag = ['S', 'N', 'A']
    client_secretPATH = 'YoutubeAPI/client_secret.json'

    parseVideo = ParseVideo('1')

    if videoID:
        parseVideo.getCaptionFromID(videoID, client_secretPATH).parse(posTag)
    else:
        parseVideo.getCaptionFromFile(captionFileName).parse(posTag)
        """
