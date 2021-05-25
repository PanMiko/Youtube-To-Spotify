from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage

import requests

# Window with information about converted song
class SongWindow(object):
    def __init__(self, track):
        super(SongWindow, self).__init__()
        self.track = track

    def setupUi(self, MainWindow, url_img=None):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 500)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.image = QImage()
        self.image.loadFromData(requests.get(url_img).content)

        self.photo = QtWidgets.QLabel(self.centralwidget)
        self.photo.setGeometry(QtCore.QRect(250, 50, 300, 300))
        self.photo.setText("")
        self.photo.setPixmap(QtGui.QPixmap(self.image))
        self.photo.setScaledContents(True)
        self.photo.setObjectName("photo")

        self.trackLabel = QtWidgets.QLabel(self.centralwidget)
        self.trackLabel.setGeometry(QtCore.QRect(0, 400, 801, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.trackLabel.setFont(font)
        self.trackLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.trackLabel.setObjectName("trackLabel")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setFixedSize(800, 500)
        MainWindow.setWindowTitle(_translate("MainWindow", "Song details"))
        self.trackLabel.setText(_translate("MainWindow", str(self.track)))
