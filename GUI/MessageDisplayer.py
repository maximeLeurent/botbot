from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QTextEdit, QHBoxLayout
import datetime


class MessageDisplayer(QWidget):
    def __init__(self, parent, maxLenLabel = 50):
        QWidget.__init__(self, parent)
        self.listMsg = []
        self.maxLenLabel = maxLenLabel

        layout = QHBoxLayout()
        self.setLayout(layout)
        self.label = QLabel(self)
        layout.addWidget(self.label)
        self.buttonMore = QPushButton("+",self)
        self.buttonMore.clicked.connect(self.displayMoreMessage)
        layout.addWidget(self.buttonMore)

        self.textEdit = QTextEdit(self)
        self.textEdit.hide()
        self.testEditShow = False

    def displayMoreMessage(self):
        if(not self.testEditShow ):
            self.textEdit.setText("\n".join(self.listMsg))
            self.textEdit.show()
            self.buttonMore.setText("-")
            self.testEditShow = True
        else:
            self.textEdit.hide()
            self.buttonMore.setText("+")
            self.testEditShow = False

    def __addMessage(self, msg, color):
        now = datetime.datetime.now()
        newMsg = "<font color=%s>[%i:%i:%i]%s</font><br \>"%(color, now.hour, now.minute,now.second, msg)
        if(len(newMsg) >self.maxLenLabel):
            labelMsg = "<font color=%s>[%i:%i:%i]%s</font><br \>"%(color, now.hour, now.minute,now.second, (msg[:50] + "..."))
        else:
            labelMsg = newMsg
        self.label.setText(labelMsg)
        self.listMsg.append(newMsg)

    def showMessage(self, msg):
        self.__addMessage(msg,"black")

    def showWarning(self, msg):
        self.__addMessage(msg,"orange")

    def showError(self, msg):
        self.__addMessage(msg,"red")
