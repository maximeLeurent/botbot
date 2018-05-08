
from PyQt5.QtCore import pyqtSignal

class Order():
    error = pyqtSignal(Order, str)
    warning =pyqtSignal(Order, str)
    info = pyqtSignal(Order, str)
    def __init__(self):
        self.listPreSubOrder = []
        self.listPostSubOrder = []

    def addPreSubOrder(self, subOrder):
        self.listPreSubOrder.append(subOrder)
        self.connectSignalSubOrder(subOrder)

    def addPostSubOrder(self, subOrder):
        self.listPostSubOrder.append(subOrder)
        self.connectSignalSubOrder(subOrder)

    def connectSignalSubOrder(self, subOrder):
        subOrder.error.connect(self.error)
        subOrder.warning.connect(self.warning)
        subOrder.info.connect(self.info)

    def diffIngEnd(self):
        return []

    def getPosEnd(self):
        pass

    def yieldSubOrder(self):
        for order in self.listPreSubOrder:
            yield order
        for order in self.listPostSubOrder:
            yield order

    def breakAll(self):
        for order in self.yieldSubOrder():
            order.breakAll()

    def unBreakAll(self):
        for order in self.yieldSubOrder():
            order.unBreakAll()

    def myOwnExecution(self):
        pass

    def execution(self):
        for order in listPostSubOrder:
            order.execution()

        self.myOwnExecution()

        for order in self.listPostSubOrder:
            order.execution()

    def cancel(self):
        pass
