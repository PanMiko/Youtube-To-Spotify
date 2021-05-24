from PyQt5 import QtCore, QtGui, QtWidgets

# Window with more statistics
class StatsWindow(object):
    def setupUi(self, Dialog, stats):
        self.stats = stats
        Dialog.setObjectName("Dialog")
        Dialog.resize(570, 300)

        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(60, 40, 501, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(60, 90, 501, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(60, 140, 501, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(60, 190, 501, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        Dialog.setFixedSize(570, 300)
        self.label.setText(_translate("Dialog", str(self.stats[0])))
        self.label_2.setText(_translate("Dialog", str(self.stats[1])))
        self.label_3.setText(_translate("Dialog", str(self.stats[2])))
        self.label_4.setText(_translate("Dialog", str(self.stats[3])))