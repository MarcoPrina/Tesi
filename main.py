from pathlib import Path

from parseVideo import ParseVideo

if __name__ == '__main__':

    Path("Outputs").mkdir(parents=True, exist_ok=True)

    videoID = "THNwJlawXic"
    captionFileName = 'Outputs/caption.txt'
    posTag = ['S', 'N', 'A']
    client_secretPATH = 'YoutubeAPI/client_secret.json'

    parseVideo = ParseVideo('1')

    if videoID:
        parseVideo.getCaptionFromID(videoID, client_secretPATH).parse(posTag)
    else:
        parseVideo.getCaptionFromFile(captionFileName).parse(posTag)
