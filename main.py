from pathlib import Path

from YoutubeAPI.credentials import YoutubeCredentials
from YoutubeAPI.playlistData import PlaylistData
from parseVideo import ParseVideo

if __name__ == '__main__':

    playlistID = 'PLdrYmPSKBRMwcxumBOfPci1hFBg7Q_Nnw'
    posTag = ['S', 'N', 'A']
    client_secretPATH = 'YoutubeAPI/client_secret.json'

    Path("Outputs").mkdir(parents=True, exist_ok=True)

    credential = YoutubeCredentials(client_secretPATH).get()
    playlist = PlaylistData(credential).get(playlistID).askLessons().playlist

    for video in playlist:
        parseVideo = ParseVideo(str(video['lesson']))
        parseVideo.getCaptionFromID(video['videoId'], client_secretPATH).parse(posTag)
        print('Elaborata lezione ', str(video['lesson']))

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
