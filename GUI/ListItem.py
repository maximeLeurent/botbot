from PyQt5.QtWidgets import QComboBox
from ItemBase import ItemBase

class ListItem(QComboBox):
    def __init__(self, parent):
        QComboBox.__init__(self,parent)
        
        self.addItem("coucou")
        self.addItem("caca")
        
    def getItemBase(self):
        return ItemBase()