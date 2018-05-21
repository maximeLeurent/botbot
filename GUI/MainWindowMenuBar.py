from PyQt5.QtWidgets import QMenuBar, QMenu, QAction

class MainWindowMenuBar(QMenuBar):
    def __init__(self,parent, mainWindow):
        QMenuBar.__init__(self,parent)

        menuFenetre = QMenu("Fenetre",self)
        self.addMenu(menuFenetre)

        achatAction = QAction("Achat",self)
        menuFenetre.addAction(achatAction)
        achatAction.triggered.connect(mainWindow.openAchat)

        venteAction = QAction("Vente", self)
        menuFenetre.addAction(venteAction)

        takeScreenShotAction = QAction("ScreenShot Test",self)
        self.addAction(takeScreenShotAction)
        takeScreenShotAction.triggered.connect(mainWindow.openScreenShotTaker)
