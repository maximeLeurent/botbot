from PyQt5.QtWidgets import QMenuBar, QMenu, QAction

class MainWindowMenuBar(QMenuBar):
    def __init__(self,parent):
        QMenuBar.__init__(self,parent)        
        
        menuFenetre = QMenu("Fenetre",self)      
        self.addMenu(menuFenetre)
        
        achatAction = QAction("Achat",self)
        menuFenetre.addAction(achatAction)
        achatAction.triggered.connect(parent.openAchat)
        
        venteAction = QAction("Vente", self)
        menuFenetre.addAction(venteAction)