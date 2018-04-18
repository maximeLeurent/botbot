from PyQt5.QtWidgets import QComboBox

class ListEquipement(QComboBox):
    def __init__(self, parent):
        QComboBox.__init__(self,parent)


    def getCurrentEquipement(self):
        return self.model().getEquipement(self.currentIndex())
