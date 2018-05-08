from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel,QItemDelegate,QLineEdit, QPushButton, QTableView
from PyQt5.QtCore import pyqtSignal,QSize
from PyQt5.QtGui import QIntValidator

from .TablePriceIngredientModel import TablePriceIngredientModel
import datetime

class LabelPlusMoins(QWidget):
    valueChanged =pyqtSignal(int)
    def __init__(self, parent, title, initValue):
        QItemDelegate.__init__(self, parent)
        mainLayout = QHBoxLayout(self)

        if title:
            label = QLabel(title, self)
            mainLayout.addWidget(label)
        self.lineEdit = QLineEdit(self )
        self.lineEdit.setValidator(QIntValidator())
        self.lineEdit.setText("0")
        self.initValue = "0"
        self.lineEdit.editingFinished.connect(self.sendValueChanged)
        mainLayout.addWidget(self.lineEdit)
        try:
            int(initValue)
            self.initValue = initValue
            self.lineEdit.setText(str(initValue))
        except:
            pass
        buttonLayout = QVBoxLayout(self)
        mainLayout.addLayout(buttonLayout)
        self.plusButton = QPushButton("+", self)
        self.plusButton.clicked.connect(self.plus)
        buttonLayout.addWidget(self.plusButton)
        self.moinsButton = QPushButton("-", self)
        self.moinsButton.clicked.connect(self.moins)
        buttonLayout.addWidget(self.moinsButton)
        self.setSizeButton()

    def reset(self):
        self.lineEdit.setText(str(self.initValue))

    def sendValueChanged(self):
        text = self.lineEdit.text()
        if(not text):
            val = 0
        try:
            val = int(text)
        except:
            val = 0
        self.valueChanged.emit(val)

    def plus(self):
        self.lineEdit.setText(str(int(self.lineEdit.text())+1))

    def moins(self):
        self.lineEdit.setText(str(int(self.lineEdit.text())-1))

    def resizeEvent(self, event):
        self.setSizeButton()

    def setSizeButton(self):
        self.plusButton.resize(QSize(self.lineEdit.size().height()/2, self.lineEdit.size().height()/2))
        self.moinsButton.resize(QSize(self.lineEdit.size().height()/2, self.lineEdit.size().height()/2))

class LabelPlusMoinsDeledate(QItemDelegate):
    def __init__(self, parent, initValue):
        QItemDelegate.__init__(self, parent)
        self.widget = LabelPlusMoins(self, parent,"", initValue)

    def createEditoer(self, value):
        return self.widget

class PriceDisplay(QItemDelegate):
    def __init__(self, parent):
        QItemDelegate.__init__(self, parent)
        self.buttonAchat = QPushButton("? K", self)
        self.labelTime= QLabel("?", self)

    def setData(self, value):
        """
        value is a tuple of two element : a int, that should be the price, and a date that should be the last maj
        """

        self.buttonAchat.setText(value[0])
        timeDisplay = datetime.datetime.now() - value[1]
        if timeDisplay.days != 0:
            text = "%i jours"%timeDisplay.days
        elif timeDisplay.hours != 0:
            text = "%i heures"%timeDisplay.hours
        elif timeDisplay.minutes != 0:
            text = "%i minutes"%timeDisplay.minutes
        else:
            text = "%i seconds"%timeDisplay.seconds
        self.labelTime.setText(text)

class TableIngredientView(QTableView):
    def __init__(self, parent, mainWin):
        QTableView.__init__(self,parent)
        self.setModel(TablePriceIngredientModel(self, mainWin))

class TableIngredientWidget(QWidget):
    """Parent of the table that show the prices of ingrdients use in the seleted ingredient's receipt"""
    def __init__(self, parent, mainWin):
        super(QWidget, self).__init__(parent)
        self.selectedIng = None
        self.mainWin = mainWin

        layout = QVBoxLayout(self)

        topLayout = QHBoxLayout()
        self.nbCraft = LabelPlusMoins(self, "nbCraft", 1)
        topLayout.addWidget(self.nbCraft)
        buttonMajPrice = QPushButton("Refesh Prices", self)
        buttonMajPrice.clicked.connect(self.sendMajPrices)
        topLayout.addWidget(buttonMajPrice)
        layout.addLayout(topLayout)

        middleLayout = QHBoxLayout()
        layout.addLayout(middleLayout)
        self.tableView = TableIngredientView(self, mainWin)
        middleLayout.addWidget(self.tableView)
        self.setMinimumSize(QSize(300, 500))
        self.nbCraft.valueChanged.connect(self.tableView.model().majNbCraft)

        bottomLayout = QHBoxLayout()
        layout.addLayout(bottomLayout)
        creerButton = QPushButton("Buy & Create")
        bottomLayout.addWidget(creerButton)
        achatButton = QPushButton("Buy")
        bottomLayout.addWidget(achatButton)

    def majIngSelected(self, ing):
        self.selectedIng = ing
        self.tableView.model().majActiveIngredient(ing)
        self.nbCraft.reset()

    def sendMajPrices(self):
        if(self.selectedIng and self.selectedIng.craftable):
            listIng = []
            for i in range(8):
                if(getattr(self.selectedIng, "ing_%i"%(i+1))):
                    listIng.append(getattr(self.selectedIng, "ing_%i"%(i+1)))
                else:
                    break
            self.mainWin.persoProcessor.getPrices(listIng)
        elif(not self.selectedIng):
            self.mainWin.warning.emit("Select a objet to craft")
        else:
            self.mainWin.warning.emit("Objet not craftable")
