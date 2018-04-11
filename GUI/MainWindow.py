
# coding: utf-8

# In[1]:


import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import * 
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPixmap, QColor
from MainWindowMenuBar import MainWindowMenuBar
from AchatWindow import AchatWindow




class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
 
        self.setMinimumSize(QSize(640, 480))    
        self.setWindowTitle("Bot Bot") 
        
        self.centralWidget = QMdiArea(self)          
        self.setCentralWidget(self.centralWidget)   
 
        menuBar = MainWindowMenuBar(self)
        self.setMenuWidget(menuBar)
        
    def openAchat(self):
        achat = AchatWindow(self.centralWidget)
        achat.show()
        


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit( app.exec_() )

