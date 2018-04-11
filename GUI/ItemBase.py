from PyQt5.QtGui import QPixmap, qRgb, QImage
import numpy as np


class ItemBase():
    def __init__(self):
        pass
        
    def getPixmap(self, height,width):      
        COLORTABLE=[]
        for i in range(256): COLORTABLE.append(qRgb(i/4,i,i/2))
        a = np.random.random(height*width)*255
        a = np.reshape(a,(height,width))
        a = np.require(a, np.uint8, 'C')
        QI = QImage(a.data, width, height, QImage.Format_Indexed8)
        QI.setColorTable(COLORTABLE)
        return QPixmap.fromImage(QI)