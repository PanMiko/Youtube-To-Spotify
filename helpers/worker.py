from helpers.helper import getPlaylists, startConvert
from PyQt5.QtCore import QObject, pyqtSignal

# Worker class used for threads
class Worker(QObject):
    # Signals 
    finished = pyqtSignal()
    progressOfGettingPlaylists = pyqtSignal(list, list)
    progressOfConverting = pyqtSignal(list, list)

    # Constructor
    def __init__(self, youtubeClient, spotifyClient, chosenYTPlaylist=None, chosenSpotifyPlaylist=None):
        super(Worker, self).__init__()
        self.youtubeClient = youtubeClient
        self.spotifyClient = spotifyClient
        self.chosenYTPlaylist = chosenYTPlaylist
        self.chosenSpotifyPlaylist = chosenSpotifyPlaylist

    # Getting playlists from YT and Spotify
    def runGetPlaylists(self):
        ytPlaylists, spotifyPlaylists = getPlaylists(self.youtubeClient, self.spotifyClient)
        self.progressOfGettingPlaylists.emit(ytPlaylists, spotifyPlaylists)
        self.finished.emit()
    
    # Starting converting songs from YT to Spotify
    def runStartConvert(self):
        successSavedOnSpotify, statistics = startConvert(self.chosenYTPlaylist, self.chosenSpotifyPlaylist, self.youtubeClient, self.spotifyClient)
        self.progressOfConverting.emit(successSavedOnSpotify, statistics)
        self.finished.emit()