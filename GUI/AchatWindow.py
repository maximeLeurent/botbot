from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QGridLayout,QScrollArea,QTextEdit
from PyQt5.QtCore import QSize, pyqtSignal
from PyQt5.QtGui import QPixmap, QColor, QPalette
from ListItem import ListItem
from ItemBase import ItemBase

class IconWidget(QWidget):
    
    def __init__(self, parent):
        QWidget.__init__(self,parent)
        self.parent = parent
        iconLayout = QVBoxLayout(self)
        self.setLayout(iconLayout)  
        self.listItem = ListItem(self)        
        self.listItem.currentIndexChanged.connect(self.itemSelectedChanged)        
        self.iconWidget = QLabel(self)
        self.iconWidget.resize(QSize(50,50))
        pixmapWhite = QPixmap(50,50)
        pixmapWhite.fill(QColor("white"))
        self.iconWidget.setPixmap(pixmapWhite)        
        iconLayout.addWidget(self.listItem)
        iconLayout.addWidget(self.iconWidget)
        
    def itemSelectedChanged(self):
        self.parent.newItemSelected.emit(self.listItem.getItemBase())
    
    def majImage(self, item):
        self.iconWidget.setPixmap(item.getPixmap(50,50))
        
        
class CaracWidget(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self,parent)
        print("In init carac Widget")
        
        self.listLabel = []
        topLayout = QVBoxLayout(self)
        
        self.container =  QTextEdit()
        self.container.setReadOnly(True)
        self.container.setFixedHeight(70)
        self.container.setFixedWidth(250)
        topLayout.addWidget(self.container)
        print("out init carac widget")
        
    def majCarac(self, item):
        text = ""
        for typeCarac, minCarac, maxCarac in item.caracBase():
            print("New carac type %s" % typeCarac.name)
            if minCarac <0:
                color = "red"
            else:
                color = "black"
            text += "<font color=%s>%i à %i en %s</font><br \>" %(color,minCarac,maxCarac,typeCarac.name)
        if len(text)>4:
            text = text[:-4]
        print(text)
        self.container.setText(text)
                       
            

class AchatWindow(QWidget):
    newItemSelected = pyqtSignal(ItemBase)
    def __init__(self, parent):
        QWidget.__init__(self,parent)
        
        mainLayout = QVBoxLayout(self)
        self.setLayout(mainLayout)
        
        topLayout = QHBoxLayout(self)
        mainLayout.addLayout(topLayout)
                
        #========Icon widget in the left top corner (list + icon)
        iconWidget= IconWidget(self)
        topLayout.addWidget(iconWidget)    
        self.newItemSelected.connect(iconWidget.majImage)
        
        #========Carac widget in the middle top
        caracWidget = CaracWidget(self)
        topLayout.addWidget(caracWidget)
        self.newItemSelected.connect(caracWidget.majCarac)
        
        