from youtubeClient import YouTubeClient
from spotifyClient import SpotifyClient

from credentials.credentails import SPOTIFY_USER_ID

from mainWindow import MainWindow
from PyQt5 import QtWidgets
import sys

YOUTUBE_CREDS = "./credentials/youtube_creds.json"

def main():
    youtubeClient = YouTubeClient(YOUTUBE_CREDS)
    spotifyClient = SpotifyClient(SPOTIFY_USER_ID)
    
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    ui = MainWindow()
    ui.setupUi(mainWindow, youtubeClient, spotifyClient)
    mainWindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()