from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QListWidgetItem

from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QIcon, QPixmap

from gui.songWindow import SongWindow
from gui.statsWindow import StatsWindow
from helpers.worker import Worker

class MainWindow(object):
    # setting the entire window
    def setupUi(self, MainWindow, youtubeClient, spotifyClient):
        # fields
        self.youtubeClient = youtubeClient
        self.spotifyClient = spotifyClient

        self.chosenYTPlaylist = None
        self.chosenSpotifyPlaylist = None
        self.ytPlaylistsList = []
        self.spotifyPlaylistsList = []
        self.converted = []
        self.statistics = []

        # Main Window
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(878, 780)
        MainWindow.setAutoFillBackground(False)
        # MainWindow.setStyleSheet("background-color: rgb(0, 0, 0);")
        MainWindow.setAnimated(True)
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # title label
        self.title = QtWidgets.QLabel(self.centralwidget)
        self.title.setEnabled(True)
        self.title.setGeometry(QtCore.QRect(10, 20, 861, 61))
        font = QtGui.QFont()
        font.setPointSize(28)
        font.setBold(True)
        font.setWeight(75)
        self.title.setFont(font)
        # self.title.setStyleSheet("color: rgb(255, 255, 255);")
        self.title.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.title.setAutoFillBackground(False)
        self.title.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.title.setObjectName("title")

        self.logo = QtWidgets.QLabel(self.centralwidget)
        self.logo.setGeometry(QtCore.QRect(730, 10, 100, 100))
        # self.logo.setStyleSheet("")
        self.logo.setText("")
        self.logo.setPixmap(QtGui.QPixmap("img/icon.png"))
        self.logo.setScaledContents(True)
        self.logo.setObjectName("label_4")

        # 'Get Youtube and Spotify Playlists' Button
        self.getPlaylistsBtn = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.pressGetPlaylistsBtn())
        self.getPlaylistsBtn.setGeometry(QtCore.QRect(314, 100, 250, 80))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.getPlaylistsBtn.setFont(font)
        self.getPlaylistsBtn.setObjectName("getPlaylistsBtn")

        # 'From YT: ' Label
        self.fromLabel = QtWidgets.QLabel(self.centralwidget)
        self.fromLabel.setGeometry(QtCore.QRect(270, 215, 338, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.fromLabel.setFont(font)
        self.fromLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.fromLabel.setObjectName("fromLabel")

        # 'To Spotify: ' Label
        self.toLabel = QtWidgets.QLabel(self.centralwidget)
        self.toLabel.setGeometry(QtCore.QRect(270, 265, 338, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.toLabel.setFont(font)
        # self.toLabel.setStyleSheet("color: rgb(255, 255, 255)")
        self.toLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.toLabel.setObjectName("toLabel")

        # List of playlists from YouTube
        self.ytPlaylistsWidget = QtWidgets.QListWidget(self.centralwidget)
        self.ytPlaylistsWidget.setGeometry(QtCore.QRect(80, 200, 190, 180))
        self.ytPlaylistsWidget.setObjectName("ytPlaylistsWidget")
        # self.ytPlaylistsWidget.setStyleSheet("background-color: rgb(94, 94, 94);color: rgb(255, 255, 255);")
        self.ytPlaylistsWidget.itemDoubleClicked.connect(self.setChosenYtPlaylist)
        self.ytPlaylistsWidget.itemDoubleClicked.connect(lambda: self.fromLabel.setText(f"YT: {self.ytPlaylistsWidget.currentItem().text().split('. ', 1)[1]}"))

        # 'Youtube Playlists' Label
        self.ytPlayistsLabel = QtWidgets.QLabel(self.centralwidget)
        self.ytPlayistsLabel.setGeometry(QtCore.QRect(80, 165, 190, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.ytPlayistsLabel.setFont(font)
        # self.ytPlayistsLabel.setStyleSheet("color: rgb(255, 255, 255);")
        self.ytPlayistsLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.ytPlayistsLabel.setObjectName("ytPlayistsLabel")

        # 'Spotify Playlists' Label
        self.spotifyPlaylistsLabel = QtWidgets.QLabel(self.centralwidget)
        self.spotifyPlaylistsLabel.setGeometry(QtCore.QRect(608, 165, 190, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.spotifyPlaylistsLabel.setFont(font)
        # self.spotifyPlaylistsLabel.setStyleSheet("color: rgb(255, 255, 255);")
        self.spotifyPlaylistsLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.spotifyPlaylistsLabel.setObjectName("spotifyPlaylistsLabel")

        # List of playlists from Spotify
        self.spotifyPlaylistsWidget = QtWidgets.QListWidget(self.centralwidget)
        self.spotifyPlaylistsWidget.setGeometry(QtCore.QRect(608, 200, 190, 180))
        self.spotifyPlaylistsWidget.setObjectName("spotifyPlaylistsWidget")
        # self.spotifyPlaylistsWidget.setStyleSheet("background-color: rgb(255, 255, 255);\n""color: rgb(0, 0, 0);")
        self.spotifyPlaylistsWidget.itemDoubleClicked.connect(self.setChosenSpotifyPlaylist)
        self.spotifyPlaylistsWidget.itemDoubleClicked.connect(lambda: self.toLabel.setText(f"SPTFY: {self.spotifyPlaylistsWidget.currentItem().text().split('. ', 1)[1]}"))

        # 'Start Converting' Button
        self.startConvertBtn = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.pressStartConvertBtn())
        self.startConvertBtn.setGeometry(QtCore.QRect(339, 310, 200, 50))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.startConvertBtn.setFont(font)
        # self.startConvertBtn.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.startConvertBtn.setObjectName("startConvertBtn")
        self.startConvertBtn.setEnabled(False)

        # List of successful converted songs to Spotify Playlist from YouTube playlist
        self.convertedSongsWidget = QtWidgets.QListWidget(self.centralwidget)
        self.convertedSongsWidget.setGeometry(QtCore.QRect(270, 420, 338, 261))
        self.convertedSongsWidget.setObjectName("convertedSongsWidget")
        # self.convertedSongsWidget.setStyleSheet("background-color: rgb(255, 255, 255);\n""color: rgb(0, 0, 0);")
        self.convertedSongsWidget.itemDoubleClicked.connect(self.showSongWindow)

        # 'Songs saved on Spotify' Label
        self.savedSongsLabel = QtWidgets.QLabel(self.centralwidget)
        self.savedSongsLabel.setGeometry(QtCore.QRect(270, 380, 338, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.savedSongsLabel.setFont(font)
        # self.savedSongsLabel.setStyleSheet("color: rgb(255, 255, 255);")
        self.savedSongsLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.savedSongsLabel.setObjectName("savedSongsLabel")

        # More statistic Button
        self.moreStatisticsBtn = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.showMoreStats())
        self.moreStatisticsBtn.setGeometry(QtCore.QRect(300, 690, 278, 28))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.moreStatisticsBtn.setFont(font)
        # self.moreStatisticsBtn.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.moreStatisticsBtn.setEnabled(False)
        self.moreStatisticsBtn.setObjectName("moreStatisticsBtn")

        # 'Wait...' Label
        self.waitLabel = QtWidgets.QLabel(self.centralwidget)
        self.waitLabel.setGeometry(QtCore.QRect(270, 420, 341, 261))
        font = QtGui.QFont()
        font.setPointSize(36)
        self.waitLabel.setFont(font)
        self.waitLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.waitLabel.setVisible(False)
        self.waitLabel.setObjectName("waitLabel")

        # setting up
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 878, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    # handle 'Get Youtube and Spotify Playlists' Button
    def pressGetPlaylistsBtn(self):
        self.resetWindow()

        self.thread = QThread()
        self.worker = Worker(self.youtubeClient, self.spotifyClient)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.runGetPlaylists)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progressOfGettingPlaylists.connect(self.handleGettingPlaylists)
        self.thread.start()
        self.getPlaylistsBtn.setEnabled(False)
        self.thread.finished.connect(
            lambda: self.getPlaylistsBtn.setEnabled(True)
        )

    # Handle the end of the thread Worker work
    def handleGettingPlaylists(self, ytPlaylists, spotifyPlaylists):
        self.ytPlaylistsList = ytPlaylists
        self.spotifyPlaylistsList = spotifyPlaylists

        for i, playlist in enumerate(ytPlaylists):
            item = QListWidgetItem(f"{i + 1}. {playlist.title}")
            self.ytPlaylistsWidget.addItem(item)

        for i, playlist in enumerate(spotifyPlaylists):
                item = QListWidgetItem(f"{i + 1}. {playlist.title}")
                self.spotifyPlaylistsWidget.addItem(item)

    # Handle 'Start Converting' Button
    def pressStartConvertBtn(self):
        self.convertedSongsWidget.clear()
        self.moreStatisticsBtn.setEnabled(False)
        self.waitLabel.setVisible(True)

        self.thread = QThread()
        self.worker = Worker(self.youtubeClient, self.spotifyClient, self.chosenYTPlaylist, self.chosenSpotifyPlaylist)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.runStartConvert)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progressOfConverting.connect(self.handleConverting)
        self.thread.start()
        self.startConvertBtn.setEnabled(False)
        self.thread.finished.connect(self.endConverting)

    # Handle the end of the thread Worker work
    def handleConverting(self, successSavedOnSpotify, statistics):
        [self.convertedSongsWidget.addItem(f"{item.artist} - {item.track}") for item in successSavedOnSpotify]
        self.converted = successSavedOnSpotify
        self.statistics = statistics
        self.moreStatisticsBtn.setEnabled(True)

    # Updating GUI
    def endConverting(self):
        self.startConvertBtn.setEnabled(True)
        self.waitLabel.setVisible(False)

    # Showing window with image + artist - title 
    def showSongWindow(self, item):
        url_img = self.converted[self.convertedSongsWidget.currentRow()].url_img

        self.songWindow = QtWidgets.QMainWindow()
        ui = SongWindow(item.text())
        ui.setupUi(self.songWindow, url_img)
        self.songWindow.show()

    # Handle 'More statistics' Button
    def showMoreStats(self):
        self.statsWindow = QtWidgets.QMainWindow()
        ui = StatsWindow()
        ui.setupUi(self.statsWindow, self.statistics)
        self.statsWindow.show()

    # Setting chosen YT playlist
    def setChosenYtPlaylist(self):
        print('>>> YT playlist chosen')
        index = self.ytPlaylistsWidget.currentRow()
        self.chosenYTPlaylist = self.ytPlaylistsList[index]
        self.enableStartConvertBtn()

    # Setting chosen Spotify playlist
    def setChosenSpotifyPlaylist(self):
        print('>>> SPOTIFY playlist chosen')
        index = self.spotifyPlaylistsWidget.currentRow()
        self.chosenSpotifyPlaylist = self.spotifyPlaylistsList[index]
        self.enableStartConvertBtn()
        
    # Enable start converting button after selecting playlists
    def enableStartConvertBtn(self):
        if self.chosenYTPlaylist is not None and self.chosenSpotifyPlaylist is not None:
            self.startConvertBtn.setEnabled(True)

    # Reseting fields
    def resetWindow(self):
        self.chosenYTPlaylist = None
        self.chosenSpotifyPlaylist = None
        self.ytPlaylistsList = []
        self.spotifyPlaylistsList = []
        self.converted = []
        self.statistics = []

        self.ytPlaylistsWidget.clear()
        self.spotifyPlaylistsWidget.clear()
        self.convertedSongsWidget.clear()
        self.fromLabel.setText("From YouTube")
        self.toLabel.setText("To Spotify")
        self.startConvertBtn.setEnabled(False)
        self.moreStatisticsBtn.setEnabled(False)

    # Setting up GUI
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate

        MainWindow.setWindowTitle(_translate("MainWindow", "Youtube to Spotify Converter"))
        MainWindow.setFixedSize(878, 780)
        self.title.setText(_translate("MainWindow", "YouTube to Spotify Converter"))
        self.getPlaylistsBtn.setText(_translate("MainWindow", "Get \n"
                                                        "Youtube and Spotify\n"
                                                        " Playlists"))
        self.startConvertBtn.setText(_translate("MainWindow", "Start Converting"))
        self.fromLabel.setText(_translate("MainWindow", "From YouTube"))
        self.toLabel.setText(_translate("MainWindow", "To Spotify"))
        self.ytPlayistsLabel.setText(_translate("MainWindow", "YouTube Playlists"))
        self.spotifyPlaylistsLabel.setText(_translate("MainWindow", "Spotify Playlists"))

        self.savedSongsLabel.setText(_translate("MainWindow", "Songs saved on Spotify"))

        self.moreStatisticsBtn.setText(_translate("MainWindow", "Show more statistics"))

        self.waitLabel.setText(_translate("MainWindow", "Wait..."))