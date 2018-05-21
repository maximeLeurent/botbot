from PyQt5.QtCore import QRect

import win32gui

class MyRect(QRect):
    @staticmethod
    def fromWindow(window):
        """
        return a MyRect with the size of the window
        """
        winPos = win32gui.GetWindowRect(window)
        return MyRect(winPos[0],winPos[1], winPos[2]- winPos[0], winPos[3]-winPos[1])

    def leftTopTuple(self):
        return (self.left(), self.top())

    def widthHeightTuple(self):
        return (self.width(), self.height())

    def __str__(self):
        return "t: %i, l: %i, r: %i, b: %i"%(self.top(), self.left(), self.right(), self.bottom())
