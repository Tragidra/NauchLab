import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from PyQt5.uic import loadUi
from PyQt5.uic.uiparser import QtWidgets


class Rachet(QDialog):
    check_box = None
    tray_icon = None
    def __init__(self):
        super(Rachet, self).__init__()
        loadUi("Rachet.ui",self)

app = QApplication(sys.argv)
mainW = Rachet()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainW)
widget.setFixedWidth(500)
widget.setFixedHeight(400)
widget.show()
app.exec()