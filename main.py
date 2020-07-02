from pathlib import Path

from AggregateData.aggregateVideos import AggregateVideos
from YoutubeAPI.credentials import YoutubeCredentials
from YoutubeAPI.playlistData import PlaylistData
from AggregateData.parseVideo import ParseVideo

if __name__ == '__main__':

    playlistID = ''  # 'PLdrYmPSKBRMwcxumBOfPci1hFBg7Q_Nnw'  # 'PLdrYmPSKBRMzHYgtsF0efrW5dtfvg7uwM'
    posTag = ['S', 'A']
    client_secretPATH = 'YoutubeAPI/client_secret.json'

    Path("Outputs").mkdir(parents=True, exist_ok=True)
    ParseVideo('1').getCaptionFromFile('Outputs/' + '1' + '/caption.txt').parseFromCaption(posTag)
    # ParseVideo('2').parseFromTokenFile(posTag)

    if playlistID:
        credential = YoutubeCredentials(client_secretPATH).get()
        playlist = PlaylistData(credential).get(playlistID).askLessons().playlist

        for video in playlist:
            parseVideo = ParseVideo(str(video['lesson']))
            # parseVideo.getCaptionFromID(video['videoId'], client_secretPATH).parseFromCaption(posTag)
            # parseVideo.getCaptionFromFile('Outputs/' + str(video['lesson']) + '/caption.txt').parseFromCaption(posTag)
            parseVideo.parseFromTokenFile(posTag)
            print('Elaborata lezione ', str(video['lesson']))

    # AggregateVideos().genereteCommonWords()
    # AggregateVideos().genereteCommonBinomi()
'''
    sentencesWithToken = []
    with open('Outputs/1/token.csv') as f:
        next(f)
        token = [line.strip().split(';') for line in f]
        for data in token:
            if data[2].startswith(tuple(posTag)):
                sentencesWithToken.append(data[0][:-1])
                '''



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
