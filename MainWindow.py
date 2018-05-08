
# coding: utf-8

# In[1]:


import sys, os, inspect
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QMdiArea, QMdiSubWindow, QWidget
from PyQt5.QtCore import QSize, pyqtSignal
from PyQt5.QtGui import QPixmap, QColor
from GUI.MainWindowMenuBar import MainWindowMenuBar
from GUI.AchatWindow import AchatWindow
from GUI.MessageDisplayer import MessageDisplayer
from GUI.UserPreference import UserPreference
from BDD.DatabaseProcessor import DatabaseProcessor
from Perso.PersoProcessor import PersoProcessor


cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() )) [0]))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)
pathPreference = os.path.join(cmd_folder, "prefUser.json")

class MainWindow(QMainWindow):
    message = pyqtSignal(str)
    warning = pyqtSignal(str)
    error = pyqtSignal(str)
    def __init__(self):
        QMainWindow.__init__(self)
        self.dbProcessor = DatabaseProcessor()
        self.persoProcessor = PersoProcessor(self)
        self.messageDisplayer = MessageDisplayer(self)
        self.userPref = UserPreference(self, pathPreference)
        self.message.connect(self.messageDisplayer.showMessage)
        self.warning.connect(self.messageDisplayer.showWarning)
        self.error.connect(self.messageDisplayer.showError)


        self.setMinimumSize(QSize(640, 480))
        self.setWindowTitle("Bot Bot")

        self.centralWidget = QWidget(self)
        self.centralWidget.setLayout(QtWidgets.QVBoxLayout(self.centralWidget))
        self.setCentralWidget(self.centralWidget)

        self.mdiArea = QMdiArea(self.centralWidget)
        self.centralWidget.layout().addWidget(self.mdiArea)
        self.achatWindow = self.createSubWindows(AchatWindow(self.centralWidget, self), "Achat")
        self.achatWindow.hide()

        menuBar = MainWindowMenuBar(self)
        self.setMenuWidget(menuBar)

    def createSubWindows(self, widget, title):
        subWindow = MySubWindow(self, self.userPref)
        subWindow.setWidget(widget)
        subWindow.setObjectName(title)
        subWindow.setWindowTitle(title)
        self.mdiArea.addSubWindow(subWindow)
        return subWindow

    def openAchat(self):
        self.achatWindow.show()

    def closeEvent(self, event):
        self.mdiArea.closeAllSubWindows()
        self.userPref.saveGeoWidget(self)
        self.userPref.saveFile()
        super(MainWindow, self).closeEvent(event)

class MySubWindow(QMdiSubWindow):
    def __init__(self, parent, userPref):
        super(MySubWindow, self).__init__(parent)
        self.userPref = userPref

    def showEvent(self, event):
        self.userPref.loadSubWindow(self)
        self.userPref.loadWidget(self.widget())

    def closeEvent(self,event):
        self.userPref.saveSubWindow(self)
        self.userPref.saveWidget(self.widget())
        self.hide()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    global mainWin
    mainWin = MainWindow()
    mainWin.show()
    sys.exit( app.exec_() )
