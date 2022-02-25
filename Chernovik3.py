import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import QDir
from PyQt5.QtWidgets import QMainWindow, QApplication, QHBoxLayout, QWidget, QTreeView, QListView, QFileSystemModel
from PyQt5.uic import loadUi
from pyqtgraph.flowchart import Flowchart
import pyqtgraph.flowchart.library as fclib
from pyqtgraph.flowchart.library.common import CtrlNode

class Main(QMainWindow):
    check_box = None
    tray_icon = None
    def __init__(self):
        super(Main, self).__init__()
        loadUi("UI/Main.ui",self)
        terminals = {
            'dataIn': {'io': 'in'},
            'dataOut': {'io': 'out'},
            'dataIn2': {'io': 'in'},
            'dataOut2': {'io': 'out'},
        }
        fc = Flowchart(terminals)
        w = fc.widget()

        self.LayOut1.addWidget(w, 0, 0, 2, 1)
        f = open('C:/Users/astra/PycharmProjects/Laboratoria1.0/resour/experementi/Exper1.txt')
        data = f.read()
        library = fclib.LIBRARY.copy()
        library.addNodeType(UnsharpMaskNode, [('Текст',),
                                              ('Submenu_test', 'submenu2', 'submenu3')])
        fc.setLibrary(library)
        data1 = "Hahaha"
        data2 = "Solo"
        fNode = fc.createNode('Текст', pos=(0, 0))
        fc.connectTerminals(fc['dataIn'], fNode['dataIn'])
        fc.connectTerminals(fNode['dataOut'], fc['dataOut'])
        fc.setInput(dataIn=data)
        fc.setInput(dataIn2=data1)

class UnsharpMaskNode(CtrlNode):
    nodeName = "Текст"

    def __init__(self, name):
        terminals = {
            'dataIn': {'io' : 'in'},
            'dataOut': {'io': 'out'}}
        CtrlNode.__init__(self, name, terminals=terminals)

    def process(self, dataIn, display=True):

        text = dataIn
        output = text
        return {'dataOut': output}

class FileOtobr(QWidget):
    def __init__(self):
        super().__init__()
        hlay = QHBoxLayout(self)
        self.treeview = QTreeView()
        self.listview = QListView()
        hlay.addWidget(self.treeview)
        hlay.addWidget(self.listview)

        path = QDir.rootPath()
        path1 = "C:/Users/astra/PycharmProjects/Laboratoria1.0/resour/proecti"
        #C:/Users/astra/PycharmProjects/Laboratoria1.0/resour/proecti
        self.dirModel = QFileSystemModel()
        self.dirModel.setRootPath(QDir.rootPath())
        self.dirModel.setFilter(QDir.NoDotAndDotDot | QDir.AllDirs)

        self.fileModel = QFileSystemModel()
        self.fileModel.setFilter(QDir.NoDotAndDotDot |  QDir.Files)

        self.treeview.setModel(self.dirModel)
        self.listview.setModel(self.fileModel)

        self.treeview.setRootIndex(self.dirModel.index(path1))
        self.listview.setRootIndex(self.fileModel.index(path))

        self.treeview.clicked.connect(self.on_clicked)
        self.listview.clicked.connect(self.on_clicked2)

    def on_clicked(self, index):
        path = self.dirModel.fileInfo(index).absoluteFilePath()
        self.listview.setRootIndex(self.fileModel.setRootPath(path))

    def on_clicked2(self, index):
        path = self.dirModel.fileInfo(index).absoluteFilePath()
        file = open("C:/Users/astra/PycharmProjects/Laboratoria1.0/resour/pesocflow.txt", "r")
        lines = file.readlines()
        chet1 = len(lines) - 2
        file.close()
        w = open("C:/Users/astra/PycharmProjects/Laboratoria1.0/resour/pesocflow.txt", "w")
        w.writelines([item for item in lines[:-1]])
        w.close()
        dd1 = "'dataIn" + str(chet1) + "': {'io': 'in'},"
        dd2 = "'dataOut" + str(chet1) + "': {'io': 'out'},"
        with open("C:/Users/astra/PycharmProjects/Laboratoria1.0/resour/pesocflow.txt", "a") as myfile:
            myfile.write(dd1+"\n")
            myfile.write(dd2+"\n")
            myfile.write("}")
        self.close()

app = QApplication(sys.argv)
mainW = Main()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainW)
widget.setFixedWidth(1700)
widget.setFixedHeight(900)
widget.show()
app.exec()
