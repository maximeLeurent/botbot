
# coding: utf-8

# In[1]:


import sys, os, inspect
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QMdiArea
from PyQt5.QtCore import QSize, pyqtSignal
from PyQt5.QtGui import QPixmap, QColor
from GUI.MainWindowMenuBar import MainWindowMenuBar
from GUI.AchatWindow import AchatWindow
from GUI.MessageDisplayer import MessageDisplayer
from BDD.DatabaseProcessor import DatabaseProcessor
from Perso.PersoProcessor import PersoProcessor


cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() )) [0]))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)


class MainWindow(QMainWindow):
    message = pyqtSignal(str)
    warning = pyqtSignal(str)
    error = pyqtSignal(str)
    def __init__(self):
        QMainWindow.__init__(self)
        self.dbProcessor = DatabaseProcessor()
        self.persoProcessor = PersoProcessor()
        self.messageDisplayer = MessageDisplayer(self)
        self.message.connect(self.messageDisplayer.showMessage)
        self.warning.connect(self.messageDisplayer.showWarning)
        self.error.connect(self.messageDisplayer.showError)


        self.setMinimumSize(QSize(640, 480))
        self.setWindowTitle("Bot Bot")

        self.centralWidget = QMdiArea(self)
        self.setCentralWidget(self.centralWidget)

        menuBar = MainWindowMenuBar(self)
        self.setMenuWidget(menuBar)

    def openAchat(self):
        achat = AchatWindow(self.centralWidget, self)
        achat.show()



if __name__ == "__main__":
    ## Hello Main Albert Duval
    app = QtWidgets.QApplication(sys.argv)
    global mainWin
    mainWin = MainWindow()
    mainWin.show()
    sys.exit( app.exec_() )
