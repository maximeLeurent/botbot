from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QGridLayout,QScrollArea,QTextEdit
from PyQt5.QtCore import QSize, pyqtSignal
from PyQt5.QtGui import QPixmap, QColor, QPalette, qRgb, QImage
from .ListEquipement import ListEquipement

from .ListEquipementModel import ListEquipementModel
from .TableIngredientWidget import TableIngredientWidget
from .ListVente import ListVente
from BDD.bdd import Equipement

import numpy as np

class IconWidget(QWidget):

    def __init__(self, parent, mainWin):
        QWidget.__init__(self,parent)
        iconLayout = QVBoxLayout(self)
        self.mainWin = mainWin
        self.setLayout(iconLayout)
        self.listItem = ListEquipement(self)
        self.listItem.setModel(ListEquipementModel(self, self.mainWin))
        self.listItem.currentIndexChanged.connect(self.itemSelectedChanged)
        self.iconWidget = QLabel(self)
        self.iconWidget.resize(QSize(50,50))
        pixmapWhite = QPixmap(50,50)
        pixmapWhite.fill(QColor("white"))
        self.iconWidget.setPixmap(pixmapWhite)
        iconLayout.addWidget(self.listItem)
        iconLayout.addWidget(self.iconWidget)

    def itemSelectedChanged(self):
        self.parent().newItemSelected.emit(self.listItem.getCurrentEquipement())

    def majImage(self, item):
        self.iconWidget.setPixmap(self.createRandomPixmap(50,50))

    def createRandomPixmap(self, height,width):
        COLORTABLE=[]
        for i in range(256): COLORTABLE.append(qRgb(i/4,i,i/2))
        a = np.random.random(height*width)*255
        a = np.reshape(a,(height,width))
        a = np.require(a, np.uint8, 'C')
        QI = QImage(a.data, width, height, QImage.Format_Indexed8)
        QI.setColorTable(COLORTABLE)
        return QPixmap.fromImage(QI)


class CaracWidget(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self,parent)

        self.listLabel = []
        topLayout = QVBoxLayout(self)

        self.container =  QTextEdit()
        self.container.setReadOnly(True)
        self.container.setFixedHeight(70)
        self.container.setFixedWidth(250)
        topLayout.addWidget(self.container)

    def majCarac(self, item):
        self.container.setText("<br \>".join(str(bonus) for bonus in item.boni))





class AchatWindow(QWidget):
    newItemSelected = pyqtSignal(Equipement)
    #newItemSelected = pyqtSignal(str)
    def __init__(self, parent, mainWin):
        QWidget.__init__(self,parent)
        self.mainWin = mainWin

        mainLayout = QVBoxLayout(self)
        self.setLayout(mainLayout)

        topLayout = QHBoxLayout()
        mainLayout.addLayout(topLayout)

        mediumLayout = QHBoxLayout()
        mainLayout.addLayout(mediumLayout)

        #========Icon widget in the left top corner (list + icon)
        iconWidget= IconWidget(self, self.mainWin)
        topLayout.addWidget(iconWidget)
        self.newItemSelected.connect(iconWidget.majImage)

        #========Carac widget in the middle top
        caracWidget = CaracWidget(self)
        topLayout.addWidget(caracWidget)
        self.newItemSelected.connect(caracWidget.majCarac)

        #======== the list of Objet actually in selling
        self.listVente = ListVente(self, mainWin, en_cours = True)
        self.newItemSelected.connect(self.listVente.majIngSelected)
        mediumLayout.addWidget(self.listVente)

        #======== the table with price of ingreident
        self.table = TableIngredientWidget(self, mainWin)
        self.newItemSelected.connect(self.table.majIngSelected)
        mediumLayout.addWidget(self.table)
