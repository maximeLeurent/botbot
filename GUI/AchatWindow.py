from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPixmap, QColor
from ListItem import ListItem

class AchatWindow(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self,parent)
        
        mainLayout = QVBoxLayout(self)
        self.setLayout(mainLayout)
        
        caracLayout = QHBoxLayout(self)
        mainLayout.addLayout(caracLayout)
        
        iconWidgetParent = QWidget(self)
        caracLayout.addWidget(iconWidgetParent)
        iconLayout = QVBoxLayout(iconWidgetParent)
        iconWidgetParent.setLayout(iconLayout)      
        
        self.listItem = ListItem(self)
        
        self.listItem.currentIndexChanged.connect(self.majObjet)
        
        self.iconWidget = QLabel(self)
        self.iconWidget.resize(QSize(50,50))
        pixmapWhite = QPixmap(50,50)
        pixmapWhite.fill(QColor("white"))
        self.iconWidget.setPixmap(pixmapWhite)
        
        iconLayout.addWidget(self.listItem)
        iconLayout.addWidget(self.iconWidget)
        print("In init widgatAchat")
        
    def majObjet(self, index):
        itemBase = self.listItem.getItemBase()
        self.iconWidget.setPixmap(itemBase.getPixmap(50,50))
        