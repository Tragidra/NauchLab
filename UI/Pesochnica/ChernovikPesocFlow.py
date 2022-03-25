import ast
import os
import shutil
import sys
from UI.Pesochnica.opendirec import MyMainWindow
from PyQt5 import QtWidgets
from PyQt5.QtCore import QUrl, QByteArray, QFile, QIODevice, QDir
from PyQt5.QtGui import QPixmap
from PyQt5.QtWebEngineCore import QWebEngineUrlScheme, QWebEngineUrlSchemeHandler, QWebEngineUrlRequestInterceptor
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile
from PyQt5.QtWidgets import QMainWindow, QWidget, QTableWidgetItem, QTextEdit, QHBoxLayout, QLineEdit, QPushButton, \
    QToolBar, QApplication, QTreeView, QListView, QFileSystemModel
from PyQt5.uic import loadUi
from numpy import array
from pyqtgraph.flowchart import Flowchart
import pyqtgraph.flowchart.library as fclib
from pyqtgraph.flowchart.library.common import CtrlNode
pathP = "C:/Users/astra/PycharmProjects/Laboratoria1.0/resour/Pictures/mq-01.png"
dannie = ""
class ChernovikPesocFlow(QMainWindow):
    def __init__(self):
        super(ChernovikPesocFlow, self).__init__()
        loadUi("C:/Users/astra/PycharmProjects/Laboratoria1.0/UI/Pesochnica/NastroikaPesocFlow.ui",self) #self.line1.text() - количество входных данных, ZMass - сами входные данные
        papka = 'C:/Users/astra/PycharmProjects/Laboratoria1.0/resour/PesocFlow'
        files = os.listdir(papka)
        a = 0
        print(files)
        self.tableWidget.setRowCount(len(files))
        for i in files:
            self.tableWidget.setItem(a, 0, QTableWidgetItem(i))
            a = a = 1
        self.pushButton33.clicked.connect(self.prildoska1) #Открыть
        self.pushButton30.clicked.connect(self.prildoska3) #удалить
        self.pushButton333.clicked.connect(self.prildoska333) #создать
        self.ok.clicked.connect(self.sapflow)

    def prildoska333(self):
        self.TextEdit = TextEditPesoc()
        self.TextEdit.show()

    def prildoska1(self):
        tecfile = self.tableWidget.item(self.tableWidget.currentRow(), 0).text()
        print('C:/Users/astra/PycharmProjects/Laboratoria1.0/resour/PesocFlow' + tecfile)
        self.close()
        self.Window = Window()
        self.Window.load(QUrl('C:/Users/astra/PycharmProjects/Laboratoria1.0/resour/PesocFlow/' + tecfile))
        self.Window.show()


    def prildoska3(self):
        tecfile = self.tableWidget.item(self.tableWidget.currentRow(), 0).text()
        tempdelete = 'C:/Users/astra/PycharmProjects/Laboratoria1.0/resour/PesocFlow/' + tecfile
        os.remove(tempdelete)
        self.close()

    def sapflow(self):
        tecfile = self.tableWidget.item(self.tableWidget.currentRow(), 0).text()
        global dannie
        dannie = 'C:/Users/astra/PycharmProjects/Laboratoria1.0/resour/PesocFlow/' + tecfile
        self.close()
        self.PesocFlow = PesocFlow()
        self.PesocFlow.show()

    def smenaizo(self):
        self.FileOtobr = FileOtobrPesoc()
        self.FileOtobr.show()

class TextEditPesoc(QMainWindow): #не переносить
    def __init__(self, parent=None):
        super(TextEditPesoc, self).__init__(parent)
        self.textEdit = QTextEdit(self)
        self.setCentralWidget(self.textEdit)

        widget = QWidget(self)
        vb = QHBoxLayout(widget)
        vb.setContentsMargins(0, 0, 0, 0)
        self.findText = QLineEdit(self)
        self.findText.setText('Введите название файла(на английском)')
        findBtn = QPushButton('Сохранить', self)
        findBtn.clicked.connect(self.sochtest)
        vb.addWidget(self.findText)
        vb.addWidget(findBtn)

        tb = QToolBar(self)
        tb.addWidget(widget)
        self.addToolBar(tb)
        self.textEdit.setPlainText("Введите сюда данные для работы")

    def sochtest(self):
        nazv = self.findText.text() + ".txt"
        my_file = open(nazv, "w+")
        my_file.write(self.textEdit.toPlainText())
        my_file.close()
        os.path.isfile("/Laboratoria1.0/chernoviki/" + nazv)
        os.rename("C:/Users/astra/PycharmProjects/Laboratoria1.0/chernoviki/" + nazv, "C:/Users/astra/PycharmProjects/Laboratoria1.0/resour/PesocFlow/" + nazv)
        self.close()

class UrlSchemeHandler(QWebEngineUrlSchemeHandler):

    def requestStarted(self, job):
        url = job.requestUrl().toString()
        if url == 'myurl://png':
            file = QFile('Data/app.png', job)
            file.open(QIODevice.ReadOnly)
            job.reply(b'image/png', file)

class RequestInterceptor(QWebEngineUrlRequestInterceptor):

    def interceptRequest(self, info):
        url = info.requestUrl().toString()
        if url.endswith('.png'):
            info.redirect(QUrl('myurl://png'))

class Window(QWebEngineView): #не переносить

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.resize(800, 800)

        h1 = QWebEngineUrlScheme.schemeByName(QByteArray(b'http'))
        h2 = QWebEngineUrlScheme.schemeByName(QByteArray(b'https'))

        CorsEnabled = 0x80  # 5.14才增加
        h1.setFlags(h1.flags() |
                    QWebEngineUrlScheme.SecureScheme |
                    QWebEngineUrlScheme.LocalScheme |
                    QWebEngineUrlScheme.LocalAccessAllowed |
                    CorsEnabled)
        h2.setFlags(h2.flags() |
                    QWebEngineUrlScheme.SecureScheme |
                    QWebEngineUrlScheme.LocalScheme |
                    QWebEngineUrlScheme.LocalAccessAllowed |
                    CorsEnabled)

        de = QWebEngineProfile.defaultProfile()
        de.setRequestInterceptor(RequestInterceptor(self))
        de.installUrlSchemeHandler(QByteArray(b'myurl'), UrlSchemeHandler(self))

class PesocFlow(QWidget):
    def __init__(self,parent=None):
        super(PesocFlow, self).__init__(parent)
        loadUi("C:/Users/astra/PycharmProjects/Laboratoria1.0/UI/Pesochnica/Pesoc.ui",self)
        self.pusk.clicked.connect(self.poln)
        pixmap = QPixmap(pathP)
        self.labkar.setPixmap(pixmap)
        file = open(dannie, "r")
        contents = file.read()
        contents = contents.split()
        for i in range(len(contents)):
            contents[i] = float(contents[i])
        print(contents)
        contents = array(contents)
        file.close()

        fc = Flowchart(terminals={
    'dataIn': {'io': 'in'},
    'dataOut': {'io': 'out'}
})
        fc.setInput(dataIn=contents)
        w = fc.widget()

        self.LayOut1.addWidget(w, 0, 0, 2, 1)


        library = fclib.LIBRARY.copy()
        library.addNodeType(UnsharpMaskNode, [('Текст',),
                                          ('Submenu_test', 'submenu2', 'submenu3')])
        fc.setLibrary(library)

        fNode = fc.createNode('Текст', pos=(0, 0))
        fc.connectTerminals(fc['dataIn'], fNode['dataIn'])
        fc.connectTerminals(fNode['dataOut'], fc['dataOut'])
        self.smenacher.clicked.connect(self.sapfileot)


    def sapfileot(self):
        self.close()
        self.FileOtobr = FileOtobrPesoc()
        self.FileOtobr.show()
        pixmap = QPixmap(pathP)
        self.labkar.setPixmap(pixmap)

    def poln(self):
        self.MyMainWindow = MyMainWindow()
        self.MyMainWindow.show()


class UnsharpMaskNode(CtrlNode):
    """Return the input data passed through an unsharp mask."""
    nodeName = "Текст"
    def __init__(self, name):
        ## Define the input / output terminals available on this node
        terminals = {
            'dataIn': {'io' : 'in'},
            'dataOut': {'io': 'out'}}
        CtrlNode.__init__(self, name, terminals=terminals)

    def process(self, dataIn, display=True):

        text = dataIn
        output = text
        return {'dataOut': output}

class FileOtobrPesoc(QWidget):
    def __init__(self):
        super().__init__()
        hlay = QHBoxLayout(self)
        self.treeview = QTreeView()
        self.listview = QListView()
        hlay.addWidget(self.treeview)
        hlay.addWidget(self.listview)
        path1 = "C:/Users/astra/PycharmProjects/Laboratoria1.0/resour"
        path = QDir.rootPath()
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
        global pathP
        pathP = self.dirModel.fileInfo(index).absoluteFilePath()
        self.close()
        self.PesocFlow = PesocFlow()
        self.PesocFlow.show()

app = QApplication(sys.argv)
mainW = ChernovikPesocFlow()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainW)
widget.setFixedWidth(1120)
widget.setFixedHeight(900)
widget.show()
app.exec()