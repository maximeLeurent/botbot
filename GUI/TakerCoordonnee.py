from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QWidget, QFormLayout,QLabel, QPushButton, QApplication
from PyQt5.QtCore import  pyqtSignal, QEvent
from PyQt5.QtGui import QPixmap

from Toolkit.MyRect import MyRect
from Toolkit.ScreenshotTools import takeScreenshot, findTextInImage

class TakerCoordonnee(QWidget):
    needScreenShot = pyqtSignal(MyRect)
    def __init__(self, parent, mainWindow):
        super(TakerCoordonnee, self).__init__(parent)
        self.mainWindow = mainWindow

        mainLayout = QFormLayout(self)
        self.setLayout(mainLayout)
        self.labelImage = QLabel(self)
        self.labelCoord = QLabel(self)
        self.labelTextFound = QLabel(self)
        mainLayout.addRow("ScreenShot", self.labelImage)
        mainLayout.addRow("Coord", self.labelCoord)
        mainLayout.addRow("Text", self.labelTextFound)

        buttonStart = QPushButton("Get Pos")
        buttonStart.clicked.connect(self.startGetPos)
        mainLayout.addRow(buttonStart)
        self.acceptScreenShot = False
        self.takeTopLeft = False
        self.takeButtomRight = False
        self.posTopLeft = None
        self.posButtomRight = None

        self.needScreenShot.connect(self.takeScreenShot)

    def startGetPos(self):
        self.acceptScreenShot = True
        self.takeTopLeft = True
        self.labelTextFound.setText("0 click")

    def takeScreenShot(self, rect):
        fileName = 'screenshot.bmp'
        self.labelCoord.setText(str(rect))
        takeScreenshot("Bot Bot", rect, fileName, keepScreen = True)
        pixmap = QPixmap(fileName)
        self.labelImage.setPixmap(pixmap)
        textInImage = findTextInImage(fileName)
        self.labelTextFound.setText(textInImage)

    def eventFilter(self,  event):
        if (self.acceptScreenShot and event.type() == QEvent.FocusOut):
            print("event filter reutrn true")
            return True
        print("event filter reutrn False")
        return False

    def mousePressEvent(self, event):
        print("Event %s"%str(event))
        if (self.acceptScreenShot):
            modifiers = QApplication.keyboardModifiers()
            cursor =QtGui.QCursor()
            if self.takeTopLeft and modifiers == QtCore.Qt.ControlModifier:
                print("Premier click")
                self.labelTextFound.setText("1 click")
                self.posTopLeft = cursor.pos()
                self.takeTopLeft = False
                self.takeButtomRight = True
            elif self.takeButtomRight and modifiers == QtCore.Qt.ControlModifier:
                print("Deuxieme click")
                self.labelTextFound.setText("2 click")
                self.posButtomRight = cursor.pos()
                self.takeTopLeft = False
                self.takeButtomRight = False
                self.needScreenShot.emit(MyRect(self.posTopLeft, self.posButtomRight))
