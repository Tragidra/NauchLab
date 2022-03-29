import ast
import sys
from tempfile import mkstemp

import psycopg2
import pyqtgraph.flowchart.library as fclib
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi
from pyqtgraph.flowchart import Flowchart
from pyqtgraph.flowchart.library.common import CtrlNode
from scipy import linalg
from PIL import ImageGrab
import numpy as np
import cv2
import os
import shutil
import pyqtgraph.exporters
from PyQt5 import QtWidgets, QtCore, QtWebEngineWidgets, QtWebChannel
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QTextCursor, QPainter, QPen, QImage
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QMainWindow, QDialog, QApplication, QWidget, QScrollArea, \
    QVBoxLayout, QSizePolicy, QSpacerItem, QSystemTrayIcon, QStyle, QAction, QMenu, QTableWidgetItem, QPushButton, \
    QLineEdit, QInputDialog, QComboBox, QTableWidget, QCheckBox
import pyqtgraph as pg
from scipy.linalg import solve_toeplitz, solve_banded, solve_triangular, eigh, eig_banded, eigh_tridiagonal, lu, \
    lu_factor, lu_solve, svdvals, diagsvd, orth, ldl, cholesky, polar, hessenberg
from PyQt5.QtCore import QRegExp, pyqtSignal, QPoint
from PyQt5.QtGui import QTextCharFormat, QTextCursor
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTextEdit,
                                 QToolBar, QLineEdit, QPushButton, QColorDialog, QHBoxLayout, QWidget)

from UI.Grafiki.LinGraph import Ui_Form
from UI.Visualisazia.VisualInput import Ui_Form as Form2
from UI.Grafiki.Grafiki import ThemeWidget
from PyQt5.QtCore import QUrl, QFile, QIODevice, QByteArray
from PyQt5.QtWebEngineCore import QWebEngineUrlSchemeHandler, \
    QWebEngineUrlRequestInterceptor, QWebEngineUrlScheme
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile
import datetime
import pyautogui

class Main(QMainWindow):
    check_box = None
    tray_icon = None
    def __init__(self):
        super(Main, self).__init__()
        loadUi("Main.ui",self)
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(
            self.style().standardIcon(QStyle.SP_ComputerIcon))
        show_action = QAction("Показать", self)
        quit_action = QAction("Выйти", self)
        hide_action = QAction("Скрыть", self)
        show_action.triggered.connect(self.show)
        hide_action.triggered.connect(self.hide)
        quit_action.triggered.connect(QApplication.instance().quit)
        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        self.otkrpoject.triggered.connect(self.onOpenFile)
        self.graphik.triggered.connect(self.loadgraph)
        self.dio.triggered.connect(self.loaddio)
        self.videotub.triggered.connect(self.loadyoutube)
        self.videofix.triggered.connect(self.sapis)
        self.endvideo.triggered.connect(self.zakonchitvideosapis)
        #self.pesochnica.triggered.connect(self.pesoc)
        self.formuli1.triggered.connect(self.formuli)
        self.experim1.triggered.connect(self.exper)
        self.pesochnica.triggered.connect(self.pesocdispl)
        #self.dobtextpes.triggered.connect(self.dobavittexttopes)
        #self.dobtextpes.triggered.connect(self.dobavittexttopes)
        self.otkritpesoc.triggered.connect(self.pesoc)

    def pesoc(self):
        from UI.Pesochnica.ChernovikPesocFlow import ChernovikPesocFlow
        self.ChernovikPesocFlow = ChernovikPesocFlow()
        self.ChernovikPesocFlow.show()

    def sapis(self):
        if not os.path.exists('temp.txt'):
            f = open('temp.txt', 'w')
            f.close()
            # Оценить индивидуальную запись экрана или полноэкранную запись на основе значения тега
        # преобразовываем эти пиксели в правильный массив numpy для работы с OpenCV
        record_region = None
        image = ImageGrab.grab(record_region)  # Получить экранный объект указанного диапазона
        width, height = image.size
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        dt_now = datetime.datetime.now()
        name = str(dt_now) + '.avi'
        video = cv2.VideoWriter(name, fourcc, 25, (width, height))  # Видео по умолчанию - 25 кадров
        while True:
            captureImage = ImageGrab.grab(record_region)  # Захват экрана указанного диапазона
            frame = cv2.cvtColor(np.array(captureImage), cv2.COLOR_RGB2BGR)
            video.write(frame)  # Записывать каждый кадр в видео файл
            if not os.path.exists('temp.txt'):
                break
        video.release()
        cv2.destroyAllWindows()

    def zakonchitvideosapis(self):
        self.TextEdit = TextEdit() #os.remove()
        self.TextEdit.show()

    def closeEvent(self, event):
            event.ignore()
            self.hide()
            self.tray_icon.showMessage(
                "Приложение скрыто",
                "Вы можете его развернуть нажав на иконку среди скрытых значков",
                QSystemTrayIcon.Information,
                2000
            )

    def onOpenFile(self): #тут и ниже - открытие файлов в подменю открыть проект
        path, _ = QFileDialog.getOpenFileName(
            self, 'Разные типы файлов для форматов, если буду менять, то не забыть изменить', '', 'excel(*.xlsx *.xls);;word(*.docx *.doc);;pdf(*.pdf)')
        if not path:
            return
        if _.find('*.doc'):
            return self.openOffice(path, 'Word.Application')
        if _.find('*.xls'):
            return self.openOffice(path, 'Excel.Application')
        if _.find('*.pdf'):
            return self.openPdf(path)

    def openOffice(self, path, app):
        self.axWidget.clear()
        if not self.axWidget.setControl(app):
            return QMessageBox.critical(self, '错误', '没有安装  %s' % app)
        self.axWidget.dynamicCall(
            'SetVisible (bool Visible)', 'false')  # 不显示窗体
        self.axWidget.setProperty('DisplayAlerts', False)
        self.axWidget.setControl(path)

    def openPdf(self, path):
        self.axWidget.clear()
        if not self.axWidget.setControl('Adobe PDF Reader'):
            return QMessageBox.critical(self, 'Ошибка', 'Установите Adobe PDF Reader')
        self.axWidget.dynamicCall('LoadFile(const QString&)', path)

    def loadgraph(self):
        self.graphAnalysis = graphAnalysis()
        self.graphAnalysis.show()

    def loaddio(self):
        self.ThemeWidget = ThemeWidget()
        self.ThemeWidget.show()

    def loadyoutube(self):
        self.visualInput = visualInput()
        self.visualInput.show()

    def formuli(self):
        self.Rachet = Rachet()
        self.Rachet.show()

    def exper(self):
        self.Widget = Widget() #поменять на Exper
        self.Widget.show()

    def pesocdispl(self):
        self.Pesoc = Pesoc()
        self.Pesoc.show()

    #def dobavittexttopes(self):
#        self.DobTextPes = DobTextPes()
#        self.DobTextPes.show()
        #self.FileOtobr = FileOtobr()
        #self.FileOtobr.show()

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

class CustomViewBox(pg.ViewBox):
    def __init__(self, *args, **kwds):
        pg.ViewBox.__init__(self, *args, **kwds)
        self.RectMode = 3
        self.setMouseMode(self.RectMode)

    def mouseClickEvent(self, ev):
        if ev.button() == pg.QtCore.Qt.RightButton:
            self.autoRange()

    def mouseDragEvent(self, ev):
        pg.ViewBox.mouseDragEvent(self, ev)

    def wheelEvent(self, ev, axis=None):
        # pg.ViewBox.wheelEvent(self, ev, axis)
        ev.ignore()

class DioRas(QDialog):
    def __init__(self):
        super(DioRas, self).__init__()
        loadUi("Grafiki/DioRas.ui", self)
        self.pushButton.clicked.connect(self.res)

    def res(self):
        kolg = 1
        tttemp = int(len((self.gf2.text()).split()) // kolg)
        tempxy = np.asarray((self.gf2.text()).split()).reshape(kolg, tttemp)
        for i in range(kolg):
            x = []
            y = []
            temp = tempxy[i]
            for j in range(len(tempxy[i])):
                if j%2 == 0:
                    x.append(temp[j])
                else:
                    y.append(temp[j])
            for t in range(len(x)):
                x[t] = float(x[t])
            for t in range(len(y)):
                y[t] = float(y[t])
            pg.plot(x, y, pen=None, symbol='o')


class graphAnalysis(QWidget, Ui_Form):
    '''def __init__(self):
        super(graphAnalysis, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.test)
        self.tabWidget.clear()

    def test(self):
        time = self.xInput.text()
        value = self.yInput.text()
        time = time.split(',')
        razmer = len(time)
        value = list(map(float, value.split(',')))
        tab1 = QWidget()
        scrollArea = QScrollArea(tab1)
        scrollArea.setMinimumSize(984, 550)
        scrollArea.setWidgetResizable(True)
        labelsContainer = QWidget()
        labelsContainer.setMinimumSize(0, 1500)
        scrollArea.setWidget(labelsContainer)
        layout = QVBoxLayout(labelsContainer)
        xdict = dict(enumerate(time))
        ticks = [list(zip(range(razmer), tuple(time)))]
        vb = CustomViewBox()
        plt = pg.PlotWidget(title="График", viewBox=vb)
        plt.setBackground(background=None)
        plt.plot(list(xdict.keys()), value)
        plt.getPlotItem().getAxis("bottom").setTicks(ticks)
        temp = QWidget()
        temp.setMinimumSize(900, 300)
        temp.setMaximumSize(900, 300)
        layout1 = QVBoxLayout(temp)
        layout1.addWidget(plt)
        layout.addWidget(temp)
        spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum,
                                 QSizePolicy.Expanding)
        layout.addItem(spacerItem)
        self.tabWidget.addTab(tab1, 'Ваш график')'''
    import pyqtgraph as pg
    def __init__(self):
        super(graphAnalysis,self).__init__()
        loadUi("Grafiki/Graf.ui", self)
        self.ready.clicked.connect(self.res)
        self.dioras.clicked.connect(self.DiogRas)


    def res(self):
        kolg = int(self.gf1.text())
        tttemp = int(len((self.gf2.text()).split())//kolg)
        print(((self.gf2.text()).split()))
        print(tttemp)
        tempxy = np.asarray((self.gf2.text()).split ()).reshape(kolg,tttemp)
        plotWidget = pg.plot(title="Ваш график")
        legend = pg.LegendItem((80, 60), offset=(70, 20))
        legend.setParentItem(plotWidget.graphicsItem())
        if (self.bc1.isChecked()):
            plotWidget.setBackground('w')
        if (self.bc2.isChecked()):
            plotWidget.setBackground('k')
        if (self.bc3.isChecked()):
            plotWidget.setBackground('b')
        if (self.bc4.isChecked()):
            plotWidget.setBackground('r')
        if (self.bc5.isChecked()):
            plotWidget.setBackground('y')
        if (self.bc6.isChecked()):
            plotWidget.setBackground('c')
        if (self.bc7.isChecked()):
            plotWidget.setBackground('m')
        if (self.setka.isChecked()):
            plotWidget.showGrid(x=True, y=True)
        for i in range(kolg):
            x = []
            y = []
            temp = tempxy[i]
            for j in range(len(tempxy[i])):
                if j%2 == 0:
                    x.append(temp[j])
                else:
                    y.append(temp[j])
            for t in range(len(x)):
                x[t] = float(x[t])
            for t in range(len(y)):
                y[t] = float(y[t])
            plotWidget.plot(x, y, pen=(i, kolg))  ## setting pen=(i,3) automaticaly creates three different-colored pens
            if (self.stolbdio.isChecked()):
                bg1 = pg.BarGraphItem(x=x, height=y, width=0.3, brush='b', pen=(i, kolg), name='bar')
                plotWidget.addItem(bg1)
                ttth = 'Диаграмма графика' + str(i)
                legend.addItem(bg1, ttth)
        if (self.gfr1.isChecked()):
            temmu = np.asarray((self.gf3.text()).split()).reshape(2,2)
            xp = temmu[0]
            yp = temmu[1]
            r = pg.PolyLineROI([(int(xp[0]), int(xp[1])), (int(yp[0]), int(yp[1]))])
            plotWidget.addItem(r)
        nazvtemp = self.nazvi.text()
        exporter = pg.exporters.ImageExporter(plotWidget.scene())
        exporter.export(nazvtemp + ".png")
        nazv = nazvtemp + ".png"
        os.path.isfile("/Laboratoria1.0/UI/" + nazv)
        os.rename("C:/Users/astra/PycharmProjects/Laboratoria1.0/UI/" + nazv,
                  "C:/Users/astra/PycharmProjects/Laboratoria1.0/resour/Diograph/" + nazv)
        tobd = "C:/Users/astra/PycharmProjects/Laboratoria1.0/resour/Diograph/" + nazv
        try:
            connection = psycopg2.connect(dbname='Laboratoria', user='postgres',
                                password='astrafaz99', host='127.0.0.1', port="5432")
            cursor = connection.cursor()

            postgres_insert_query = """ INSERT INTO experements (accountid, way) VALUES (%s,%s)"""
            my_file = open('Temp.txt', "r")
            idd = my_file.read()
            my_file.close()
            record_to_insert = (idd, tobd)
            cursor.execute(postgres_insert_query, record_to_insert)

            connection.commit()
            count = cursor.rowcount
            print(count, "Данные записаны в базу данных")

        except (Exception, psycopg2.Error) as error:
            print("Не получилось подключиться к таблице", error)

        finally:
            # closing database connection.
            if connection:
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")

    def DiogRas(self):
        self.DioRas = DioRas()
        self.DioRas.show()

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

class Window(QWebEngineView):

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

class Window2(QWebEngineView):
    closed = pyqtSignal()
    def __init__(self, *args, **kwargs):
        super(Window2, self).__init__(*args, **kwargs)
        self.resize(800, 800)
        self.openbtn = QPushButton('close')
        self.openbtn.clicked.connect(self.close)
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

    def closeEvent(self, event):
        self.TextEdit = TextEdit()
        self.TextEdit.show()


class visualInput(QDialog,Form2):
    def __init__(self):
        super(visualInput, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.spisiv)

    def spisiv(self):
        nazv = self.visualInput.text()
        self.Window = Window()
        self.Window.show()
        self.Window.load(QUrl('https://www.youtube.com/results?search_query=' + nazv))

class Nazvan(QDialog):
    def __init__(self):
        super(Nazvan, self).__init__()
        loadUi("Visualisazia/VisualInput.ui",self)
        self.pushButton.clicked.connect(self.click333)

    def click333(self):
        nazv = self.visualInput.text() + ".html"
        shutil.copy2("C:/Users/astra/PycharmProjects/Laboratoria1.0/resour/proecti/project1.html",
                     "C:/Users/astra/PycharmProjects/Laboratoria1.0/resour/proecti/" + nazv)
        tempfile = "C:/Users/astra/PycharmProjects/Laboratoria1.0/resour/proecti/" + nazv
        f = open(tempfile, 'r')
        basedata = f.read()
        tempstroka1 = "snapshot: JSON.parse(localStorage.getItem('" + nazv + "')),"
        tempstroka2 = "localStorage.setItem('" + nazv + "', JSON.stringify(lc.getSnapshot()));"
        newdata = basedata.replace("snapshot: JSON.parse(localStorage.getItem('drawing')),",tempstroka1)
        with open(tempfile, 'w') as f:
            f.write(newdata)
        f.close()
        f = open(tempfile, 'r')
        basedata = f.read()
        newdata1 = basedata.replace("localStorage.setItem('drawing', JSON.stringify(lc.getSnapshot()));", tempstroka2)
        with open(tempfile, 'w') as f:
            f.write(newdata1)
        f.close()
        self.close()
        self.Window = Window()
        self.Window.load(QUrl('C:/Users/astra/PycharmProjects/Laboratoria1.0/resour/proecti/' + nazv))
        self.Window.show()

class Exper(QDialog):
    def __init__(self):
        super(Exper, self).__init__()
        loadUi("Exper/Exper1.ui",self)
        self.pushButton30.clicked.connect(self.udalit)
        self.pushButton33.clicked.connect(self.otkrit)
        self.pushButton333.clicked.connect(self.clickSozd)

    def clickSozd(self):
        print('')

    def otkrit(self):
        print('')

    def udalit(self):
        print('')


def replace(file_path, pattern, subst):
    # Create temp file
    fh, abs_path = mkstemp()
    with os.fdopen(fh, 'w', encoding='utf8') as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                new_file.write(line.replace(pattern, subst))
    # Copy the file permissions from the old file to the new file
    shutil.copymode(file_path, abs_path)
    # Remove original file
    os.remove(file_path)
    # Move new file
    shutil.move(abs_path, file_path)

class Backend(QtCore.QObject):
    valueChanged = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._value = ""

    @QtCore.pyqtProperty(str)
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        self._value = v
        self.valueChanged.emit(v)

class Widget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.webEngineView = QtWebEngineWidgets.QWebEngineView()
        self.label = QtWidgets.QLabel(alignment=QtCore.Qt.AlignCenter)

        lay = QtWidgets.QVBoxLayout(self)
        lay.addWidget(self.webEngineView, stretch=1)
        lay.addWidget(self.label, stretch=1)

        backend = Backend(self)
        # backend.valueChanged.connect(self.label.setText)
        backend.valueChanged.connect(self.foo_function)
        self.channel = QtWebChannel.QWebChannel()
        self.channel.registerObject("backend", backend)
        self.webEngineView.page().setWebChannel(self.channel)

        path = "C:/Users/astra/PycharmProjects/Laboratoria1.0/resour/cherteji/index.html"
        self.webEngineView.setUrl(QtCore.QUrl.fromLocalFile(path))

    @QtCore.pyqtSlot(str)
    def foo_function(self, value):
        value = "var dataToImport = " + value
        shutil.copy('C:/Users/astra/PycharmProjects/Laboratoria1.0/resour/cherteji/basa.html',
                    'C:/Users/astra/PycharmProjects/Laboratoria1.0/resour/cherteji/index1.html')
        replace("C:/Users/astra/PycharmProjects/Laboratoria1.0/resour/cherteji/index1.html", "var dataToImport",
                        value)
        os.remove("C:/Users/astra/PycharmProjects/Laboratoria1.0/resour/cherteji/index.html")
        os.rename("C:/Users/astra/PycharmProjects/Laboratoria1.0/resour/cherteji/index1.html",
                    "C:/Users/astra/PycharmProjects/Laboratoria1.0/resour/cherteji/index.html")


class SFor(QDialog):
    def __init__(self):
        super(SFor, self).__init__()
        self.click555()

    def click555(self):
        self.close()
        self.Window = Window()
        self.Window.load(QUrl('C:/Users/astra/PycharmProjects/Laboratoria1.0/resour/svform/NewFormul.html'))
        self.Window.show()

class Rachet(QDialog):
    def __init__(self):
        super(Rachet,self).__init__()
        loadUi("formuli/Rachet.ui", self)
        self.classmath.clicked.connect(self.classicmath)
        self.geomet.clicked.connect(self.classicmath)
        self.stats.clicked.connect(self.classicmath)
        self.mashine.clicked.connect(self.classicmath)
        self.svform.clicked.connect(self.svfo1rm)

        classicmath = ['Сложение матриц','Умножение матриц', 'Транспонирование матриц', 'Определитель матрицы','Обратная матрица','Solve equation a x = b. a is Hermitian positive-definite banded matrix'] #Линейная алгебра, scipy,pandas
        geometry = [] #матплот, керас и т.д.
        statistica = [] #statsmodel
        mashin = [] #Машинное обучение, skitlearn/pytorch [[1,2,3],[4,5,6]]

    def classicmath(self):
        self.ClassM = ClassM()
        self.ClassM.show()

    def svfo1rm(self):
        self.SFor = SFor()
        self.SFor.show()

class OneMatr1(QDialog):
    def __init__(self):
        super(OneMatr1,self).__init__()
        loadUi("formuli/OneMatrix.ui", self)
        self.ready.clicked.connect(self.ras)

    def ras(self):
        TempOtvet = np.matrix(self.line1.text()).transpose()
        print(TempOtvet)
        self.tb1.setRowCount(len(TempOtvet))
        self.tb1.setColumnCount(len(TempOtvet[0]))
        for i, row in enumerate(TempOtvet):
            for j, val in enumerate(row):
                self.tb1.setItem(i, j, QTableWidgetItem(str(val)))

class OneMatr2(QDialog):
    def __init__(self):
        super(OneMatr2,self).__init__()
        loadUi("formuli/OneMatrix.ui", self)
        self.ready.clicked.connect(self.ras)

    def ras(self):
        TempOtvet = linalg.det(np.matrix(self.line1.text()))
        print(TempOtvet)
        self.tb1.setRowCount(1)
        self.tb1.setColumnCount(1)
        self.tb1.setItem(0, 0, QTableWidgetItem(str(TempOtvet)))

class OneMatr3(QDialog):
    def __init__(self):
        super(OneMatr3,self).__init__()
        loadUi("formuli/OneMatrix.ui", self)
        self.ready.clicked.connect(self.ras)

    def ras(self):
        TempOtvet = linalg.inv(np.matrix(self.line1.text()))
        self.tb1.setRowCount(len(TempOtvet))
        self.tb1.setColumnCount(len(TempOtvet[0]))
        for i, row in enumerate(TempOtvet):
            for j, val in enumerate(row):
                self.tb1.setItem(i, j, QTableWidgetItem(str(val)))

class Teplic(QDialog):
    def __init__(self):
        super(Teplic,self).__init__()
        loadUi("formuli/Teplic.ui", self)
        self.ready.clicked.connect(self.ras)

    def ras(self):
        a = np.array(self.line2.text())
        b = np.array(self.line1.text())
        c = np.array(self.line3.text())
        x = solve_toeplitz((a, b), c)
        self.tb1.setRowCount(len(x))
        self.tb1.setColumnCount(len(x[0]))
        for i, row in enumerate(x):
            for j, val in enumerate(row):
                self.tb1.setItem(i, j, QTableWidgetItem(str(val)))

class Liner1(QDialog):
    def __init__(self):
        super(Liner1,self).__init__()
        loadUi("formuli/Liner1.ui", self)
        self.ready.clicked.connect(self.ras)

    def ras(self):
        a = np.matrix(self.line1.text())
        b = np.matrix(self.line2.text())
        x = linalg.solve(a, b)
        self.tb1.setRowCount(len(x))
        self.tb1.setColumnCount(len(x[0]))
        for i, row in enumerate(x):
            for j, val in enumerate(row):
                self.tb1.setItem(i, j, QTableWidgetItem(str(val)))

class Liner2(QDialog):
    def __init__(self):
        super(Liner2,self).__init__()
        loadUi("formuli/Liner2.ui", self)
        self.ready.clicked.connect(self.ras)

    def ras(self):
        ab = np.matrix(self.line1.text())
        b = np.matrix(self.line2.text())
        nen = self.line3.text()
        print(ab)
        print(b)
        print(nen)
        x = solve_banded((1,2), ab, b)
        self.tb1.setRowCount(len(x))
        self.tb1.setColumnCount(len(x[0]))
        for i, row in enumerate(x):
            for j, val in enumerate(row):
                self.tb1.setItem(i, j, QTableWidgetItem(str(val)))

class Poloj(QDialog):
    def __init__(self):
        super(Poloj,self).__init__()
        loadUi("formuli/Poloj.ui", self)
        self.ready.clicked.connect(self.ras)

    def ras(self):
        ab = np.matrix(self.line1.text())
        b = np.matrix(self.line2.text())
        print(ab)
        print(b)
        x = solve_banded(ab, b, lower=True)
        self.tb1.setRowCount(len(x))
        self.tb1.setColumnCount(len(x[0]))
        for i, row in enumerate(x):
            for j, val in enumerate(row):
                self.tb1.setItem(i, j, QTableWidgetItem(str(val)))

class treugM(QDialog):
    def __init__(self):
        super(treugM,self).__init__()
        loadUi("formuli/treugM.ui", self)
        self.ready.clicked.connect(self.ras)

    def ras(self):
        a = np.array([[3, 0, 0, 0], [2, 1, 0, 0], [1, 0, 1, 0], [1, 1, 1, 1]])
        b = np.array([4, 2, 4, 2])
        x = solve_triangular(a, b, lower=True)
        print(x)
        a = np.matrix(self.line1.text())
        b = np.matrix(self.line2.text())
        x = solve_triangular(a, b, lower=True)
        self.tb1.setRowCount(len(x))
        self.tb1.setColumnCount(len(x[0]))
        for i, row in enumerate(x):
            for j, val in enumerate(row):
                self.tb1.setItem(i, j, QTableWidgetItem(str(val)))

class OneMatrObProb(QDialog):
    def __init__(self):
        super(OneMatrObProb,self).__init__()
        loadUi("formuli/OneMatrix.ui", self)
        self.ready.clicked.connect(self.ras)

    def ras(self):
        TempOtvet = np.matrix(self.line1.text())
        print(TempOtvet)
        TempOtvet1 = linalg.eigvals(TempOtvet)
        print(TempOtvet1)
        self.tb1.setRowCount(1)
        self.tb1.setColumnCount(1)
        self.tb1.setItem(0, 0, QTableWidgetItem(str(TempOtvet1)))

class OneMatrObProb2(QDialog):
    def __init__(self):
        super(OneMatrObProb2,self).__init__()
        loadUi("formuli/1ProbMat.ui", self)
        self.ready.clicked.connect(self.ras)

    def ras(self):
        TempOtvet = np.matrix(self.line1.text())
        print(TempOtvet)
        if (self.cbx1.isChecked() and self.cbx2.isChecked()):
            TempOtvet1 = linalg.eig(TempOtvet)
            print(TempOtvet1)
            self.tb1.setRowCount(1)
            self.tb1.setColumnCount(1)
            self.tb1.setItem(0, 0, QTableWidgetItem(str(TempOtvet1)))
        elif (self.cbx1.isChecked() and self.cbx2.isChecked() == False):
            TempOtvet1 = linalg.eig(TempOtvet, left=True, right=False)
            print(TempOtvet1)
            self.tb1.setRowCount(1)
            self.tb1.setColumnCount(1)
            self.tb1.setItem(0, 0, QTableWidgetItem(str(TempOtvet1)))
        elif (self.cbx2.isChecked() and self.cbx1.isChecked() == False):
            TempOtvet1 = linalg.eig(TempOtvet, left=False, right=True)
            print(TempOtvet1)
            self.tb1.setRowCount(1)
            self.tb1.setColumnCount(1)
            self.tb1.setItem(0, 0, QTableWidgetItem(str(TempOtvet1)))

class OneMatrObProb3(QDialog):
    def __init__(self):
        super(OneMatrObProb3,self).__init__()
        loadUi("formuli/OneMatrix.ui", self)
        self.ready.clicked.connect(self.ras)

    def ras(self):
        TempOtvet = np.matrix(self.line1.text())
        print(TempOtvet)
        TempOtvet1 = eigh(TempOtvet, eigvals_only=True)
        print(TempOtvet1)
        self.tb1.setRowCount(1)
        self.tb1.setColumnCount(len(TempOtvet))
        for j in range(len(TempOtvet)):
            print(len(TempOtvet))
            self.tb1.setItem(0, j, QTableWidgetItem(str(TempOtvet1[j])))

class OneMatrObProb4(QDialog):
    def __init__(self):
        super(OneMatrObProb4,self).__init__()
        loadUi("formuli/1ProbMatTreug.ui", self)
        self.ready.clicked.connect(self.ras)

    def ras(self):
        TempOtvet = np.matrix(self.line1.text())
        print(TempOtvet)
        if (self.cbx1.isChecked()):
            TempOtvet1 = eig_banded(TempOtvet, lower=True, eigvals_only=True)
            self.tb1.setRowCount(1)
            self.tb1.setColumnCount(len(TempOtvet))
            for j in range(len(TempOtvet)):
                print(len(TempOtvet))
                self.tb1.setItem(0, j, QTableWidgetItem(str(TempOtvet1[j])))
        else:
            TempOtvet1 = eig_banded(TempOtvet, lower=False, eigvals_only=True)
            self.tb1.setRowCount(1)
            self.tb1.setColumnCount(len(TempOtvet))
            for j in range(len(TempOtvet)):
                print(len(TempOtvet))
                self.tb1.setItem(0, j, QTableWidgetItem(str(TempOtvet1[j])))

class DiogObProb(QDialog):
    def __init__(self):
        super(DiogObProb,self).__init__()
        loadUi("formuli/DiogObProb.ui", self)
        self.ready.clicked.connect(self.ras)

    def ras(self):
        d = self.line1.text()
        e = self.line2.text()
        d = [float(val) for val in d.split(' ')]
        e = [float(val) for val in e.split(' ')]
        w = eigh_tridiagonal(d, e, eigvals_only=True)
        self.tb1.setRowCount(1)
        self.tb1.setColumnCount(len(d))
        for j in range(len(d)):
            print(len(d))
            self.tb1.setItem(0, j, QTableWidgetItem(str(w[j])))

class LuM(QDialog):
    def __init__(self):
        super(LuM,self).__init__()
        loadUi("formuli/LUM.ui", self)
        self.ready.clicked.connect(self.ras)

    def ras(self):
        TempOtvet = np.matrix(self.line1.text())
        print(TempOtvet)
        p,l,u = lu(TempOtvet)
        self.tb1.setRowCount(len(p))
        self.tb1.setColumnCount(len(p[0]))
        for i, row in enumerate(p):
            for j, val in enumerate(row):
                self.tb1.setItem(i, j, QTableWidgetItem(str(val)))
        self.tb2.setRowCount(len(l))
        self.tb2.setColumnCount(len(l[0]))
        for i, row in enumerate(l):
            for j, val in enumerate(row):
                self.tb2.setItem(i, j, QTableWidgetItem(str(val)))
        self.tb3.setRowCount(len(u))
        self.tb3.setColumnCount(len(u[0]))
        for i, row in enumerate(u):
            for j, val in enumerate(row):
                self.tb3.setItem(i, j, QTableWidgetItem(str(val)))

class LuMf(QDialog):
    def __init__(self):
        super(LuMf,self).__init__()
        loadUi("formuli/Liner1.ui", self)
        self.ready.clicked.connect(self.ras)

    def ras(self):
        A = np.matrix(self.line1.text())
        b = np.matrix(self.line2.text())
        lu, piv = lu_factor(A)
        print(lu)
        print(piv)
        x = lu_solve((lu, piv), b)
        print(x)
        np.allclose(A @ x - b, np.zeros((4,)))
        self.tb1.setRowCount(len(x))
        self.tb1.setColumnCount(len(x[0]))
        for i, row in enumerate(x):
            for j, val in enumerate(row):
                self.tb1.setItem(i, j, QTableWidgetItem(str(val)))

class Sing(QDialog):
    def __init__(self):
        super(Sing,self).__init__()
        loadUi("formuli/SIN.ui", self)
        self.ready.clicked.connect(self.ras)

    def ras(self):
        TempOtvet = np.matrix(self.line1.text())
        U, s, Vh = linalg.svd(TempOtvet)
        self.tb1.setRowCount(len(U))
        self.tb1.setColumnCount(len(U[0]))
        for i, row in enumerate(U):
            for j, val in enumerate(row):
                self.tb1.setItem(i, j, QTableWidgetItem(str(val)))
        self.tb2.setRowCount(1)
        self.tb2.setColumnCount(len(s))
        print(s)
        for j in range(len(s)):
            print(str(s[j]))
            self.tb2.setItem(0, j, QTableWidgetItem(str(s[j])))
        self.tb3.setRowCount(len(Vh))
        self.tb3.setColumnCount(len(Vh[0]))
        for i, row in enumerate(Vh):
            for j, val in enumerate(row):
                self.tb3.setItem(i, j, QTableWidgetItem(str(val)))

class SingV(QDialog):
    def __init__(self):
        super(SingV,self).__init__()
        loadUi("formuli/OneMatrix.ui", self)
        self.ready.clicked.connect(self.ras)

    def ras(self):
        TempOtvet = np.matrix(self.line1.text())
        temp1 = svdvals(TempOtvet)
        self.tb1.setRowCount(1)
        self.tb1.setColumnCount(len(temp1))
        for j in range(len(temp1)):
            print(str(temp1[j]))
            self.tb1.setItem(0, j, QTableWidgetItem(str(temp1[j])))

class SingMat(QDialog):
    def __init__(self):
        super(SingMat,self).__init__()
        loadUi("formuli/SingMatr.ui", self)
        self.ready.clicked.connect(self.ras)

    def ras(self):
        TempOtvet = self.line1.text()
        TempOtvet = [float(val) for val in TempOtvet.split(' ')]
        m = int(self.line2.text())
        n = int(self.line3.text())
        print(len(TempOtvet))
        print(TempOtvet)
        temp1 = diagsvd(TempOtvet,m,n)
        self.tb1.setRowCount(len(temp1))
        self.tb1.setColumnCount(len(temp1[0]))
        for i, row in enumerate(temp1):
            for j, val in enumerate(row):
                self.tb1.setItem(i, j, QTableWidgetItem(str(val)))

class OrtMat(QDialog):
    def __init__(self):
        super(OrtMat,self).__init__()
        loadUi("formuli/OneMatrix.ui", self)
        self.ready.clicked.connect(self.ras)

    def ras(self):
        TempOtvet = np.matrix(self.line1.text())
        temp1 = orth(TempOtvet)
        self.tb1.setRowCount(len(temp1))
        self.tb1.setColumnCount(len(temp1[0]))
        for i, row in enumerate(temp1):
            for j, val in enumerate(row):
                self.tb1.setItem(i, j, QTableWidgetItem(str(val)))

class LDTtT(QDialog):
    def __init__(self):
        super(LDTtT,self).__init__()
        loadUi("formuli/LDT.ui", self)
        self.ready.clicked.connect(self.ras)

    def ras(self):
        TempOtvet = np.matrix(self.line1.text())
        lu, d, perm = ldl(TempOtvet) #lower=0, если надо верхнюю
        self.tb1.setRowCount(len(lu))
        self.tb1.setColumnCount(len(lu[0]))
        for i, row in enumerate(lu):
            for j, val in enumerate(row):
                self.tb1.setItem(i, j, QTableWidgetItem(str(val)))
        self.tb2.setRowCount(1)
        self.tb2.setColumnCount(len(perm))
        for j in range(len(perm)):
            self.tb2.setItem(0, j, QTableWidgetItem(str(perm[j])))
        self.tb3.setRowCount(len(d))
        self.tb3.setColumnCount(len(d[0]))
        for i, row in enumerate(d):
            for j, val in enumerate(row):
                self.tb3.setItem(i, j, QTableWidgetItem(str(val)))

class Holeck(QDialog):
    def __init__(self):
        super(Holeck,self).__init__()
        loadUi("formuli/Holec.ui", self)
        self.ready.clicked.connect(self.ras)

    def ras(self):
        TempOtvet = np.matrix(self.line1.text())
        if (self.cbx1.isChecked()):
            temp1 = cholesky(TempOtvet, lower=True)
            self.tb1.setRowCount(len(temp1))
            self.tb1.setColumnCount(len(temp1[0]))
            for i, row in enumerate(temp1):
                for j, val in enumerate(row):
                    self.tb1.setItem(i, j, QTableWidgetItem(str(val)))
        elif (self.cbx2.isChecked()):
            temp1 = cholesky(TempOtvet, lower=False)
            self.tb1.setRowCount(len(temp1))
            self.tb1.setColumnCount(len(temp1[0]))
            for i, row in enumerate(temp1):
                for j, val in enumerate(row):
                    self.tb1.setItem(i, j, QTableWidgetItem(str(val)))

class PolarDec(QDialog):
    def __init__(self):
        super(PolarDec,self).__init__()
        loadUi("formuli/OneMatrix2out.ui", self)
        self.ready.clicked.connect(self.ras)

    def ras(self):
        TempOtvet = np.matrix(self.line1.text())
        u, p = polar(TempOtvet)
        self.tb1.setRowCount(len(u))
        self.tb1.setColumnCount(len(u[0]))
        for i, row in enumerate(u):
            for j, val in enumerate(row):
                self.tb1.setItem(i, j, QTableWidgetItem(str(val)))
        self.tb2.setRowCount(len(p))
        self.tb2.setColumnCount(len(p[0]))
        for i, row in enumerate(p):
            for j, val in enumerate(row):
                self.tb2.setItem(i, j, QTableWidgetItem(str(val)))

class QRD(QDialog):
    def __init__(self):
        super(QRD,self).__init__()
        loadUi("formuli/hessenberg.ui", self)
        self.ready.clicked.connect(self.ras)

    def ras(self):
        TempOtvet = np.matrix(self.line1.text())
        u, p = hessenberg(TempOtvet, calc_q=True)
        self.tb1.setRowCount(len(u))
        self.tb1.setColumnCount(len(u[0]))
        for i, row in enumerate(u):
            for j, val in enumerate(row):
                self.tb1.setItem(i, j, QTableWidgetItem(str(val)))
        self.tb2.setRowCount(len(p))
        self.tb2.setColumnCount(len(p[0]))
        for i, row in enumerate(p):
            for j, val in enumerate(row):
                self.tb2.setItem(i, j, QTableWidgetItem(str(val)))

class TextEdit(QMainWindow):
    def __init__(self, parent=None):
        super(TextEdit, self).__init__(parent)
        self.textEdit = QTextEdit(self)
        self.setCentralWidget(self.textEdit)

        widget = QWidget(self)
        vb = QHBoxLayout(widget)
        vb.setContentsMargins(0, 0, 0, 0)
        self.findText = QLineEdit(self)
        self.findText.setText('Введите сюда название эксперимента')
        findBtn = QPushButton('Сохранить', self)
        findBtn.clicked.connect(self.sochtest)
        vb.addWidget(self.findText)
        vb.addWidget(findBtn)

        tb = QToolBar(self)
        tb.addWidget(widget)
        self.addToolBar(tb)
        self.textEdit.setPlainText("Опишите здесь результаты эксперимента")

    def sochtest(self):
        nazv = self.findText.text() + ".txt"
        my_file = open(nazv, "w+")
        my_file.write(self.textEdit.toPlainText())
        my_file.close()
        os.path.isfile("/Laboratoria1.0/UI/" + nazv)
        os.rename("C:/Users/astra/PycharmProjects/Laboratoria1.0/UI/" + nazv, "C:/Users/astra/PycharmProjects/Laboratoria1.0/resour/experementi/" + nazv)
        tobd = "C:/Users/astra/PycharmProjects/Laboratoria1.0/resour/experementi/" + nazv
        try:
            connection = psycopg2.connect(dbname='Laboratoria', user='postgres',
                                password='astrafaz99', host='127.0.0.1', port="5432")
            cursor = connection.cursor()

            postgres_insert_query = """ INSERT INTO experements (accountid, way) VALUES (%s,%s)"""
            my_file = open('Temp.txt', "r")
            idd = my_file.read()
            my_file.close()
            record_to_insert = (idd, tobd)
            cursor.execute(postgres_insert_query, record_to_insert)

            connection.commit()
            count = cursor.rowcount
            print(count, "Данные записаны в базу данных")

        except (Exception, psycopg2.Error) as error:
            print("Не получилось подключиться к таблице", error)

        finally:
            # closing database connection.
            if connection:
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")



class ClassM(QDialog):
    def __init__(self):
        super(ClassM,self).__init__()
        loadUi("formuli/ClassM.ui", self)
        self.tm1.clicked.connect(self.transponm)
        self.tm1_3.clicked.connect(self.oprmat)
        self.tm1_4.clicked.connect(self.obrmat)
        self.tm1_9.clicked.connect(self.tepl)#-
        self.tm1_5.clicked.connect(self.lin1)
        self.tm1_6.clicked.connect(self.lin2) #-
        self.tm1_7.clicked.connect(self.polo)
        self.tm1_8.clicked.connect(self.treug)
        self.tm1_20.clicked.connect(self.obprob) # Проверить до конца, с точки зрения математики, вывод только собственных значений
        self.tm1_21.clicked.connect(self.obprob2)# Вывод некрасивый, но правильный
        self.tm1_24.clicked.connect(self.obprob3)
        self.tm1_27.clicked.connect(self.obprob4) #Не проверял
        self.tm1_25.clicked.connect(self.diogobprob) #Всё хорошо
        self.tm1_28.clicked.connect(self.lu) #A = P L U
        self.tm1_15.clicked.connect(self.luf) #Не работает!! Проблема Shapes of lu (4, 4) and b (1, 4) are incompatible
        self.tm1_16.clicked.connect(self.singr) #Протестировано, работает
        self.tm1_26.clicked.connect(self.singv) #Проверено
        self.tm1_18.clicked.connect(self.sigM)#Проверено работает
        self.tm1_22.clicked.connect(self.OrtsigM) #Проверено
        self.tm1_23.clicked.connect(self.LDTt) #Проверено, при необходимости добавить выбор между нижней и верхнй матрицей
        self.tm1_19.clicked.connect(self.holec) #Проверено
        self.tm1_17.clicked.connect(self.pdc) #Проверено, вывод перепроверить
        self.tm1_29.clicked.connect(self.qrdec)




    def oprmat(self):
        self.OneMatr2 = OneMatr2()
        self.OneMatr2.show()


    def transponm(self):
        self.OneMatr1 = OneMatr1()
        self.OneMatr1.show()

    def obrmat(self):
        self.OneMatr3 = OneMatr3()
        self.OneMatr3.show()

    def tepl(self):
        self.Teplic = Teplic()
        self.Teplic.show()

    def lin1(self):
        self.Liner1 = Liner1()
        self.Liner1.show()

    def lin2(self):
        self.Liner2 = Liner2()
        self.Liner2.show()

    def polo(self):
        self.Poloj = Poloj()
        self.Poloj.show()

    def treug(self):
        self.treugM = treugM()
        self.treugM.show()

    def obprob(self):
        self.OneMatrObProb = OneMatrObProb()
        self.OneMatrObProb.show()

    def obprob2(self):
        self.OneMatrObProb2 = OneMatrObProb2()
        self.OneMatrObProb2.show()

    def obprob3(self):
        self.OneMatrObProb3 = OneMatrObProb3()
        self.OneMatrObProb3.show()

    def obprob4(self):
        self.OneMatrObProb4 = OneMatrObProb4()
        self.OneMatrObProb4.show()

    def diogobprob(self):
        self.DiogObProb = DiogObProb()
        self.DiogObProb.show()

    def lu(self):
        self.LuM = LuM()
        self.LuM.show()

    def luf(self):
        self.LuMf = LuMf()
        self.LuMf.show()

    def singr(self):
        self.Sing = Sing()
        self.Sing.show()

    def singv(self):
        self.SingV = SingV()
        self.SingV.show()

    def sigM(self):
        self.SingMat = SingMat()
        self.SingMat.show()

    def OrtsigM(self):
        self.OrtMat = OrtMat()
        self.OrtMat.show()

    def LDTt(self):
        self.LDTtT = LDTtT()
        self.LDTtT.show()

    def holec(self):
        self.Holeck = Holeck()
        self.Holeck.show()

    def pdc(self):
        self.PolarDec = PolarDec()
        self.PolarDec.show()

    def qrdec(self):
        self.QRD = QRD()
        self.QRD.show()


class Pesoc(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Песочница")

        self.setGeometry(100, 100, 1500, 800)

        self.image = QImage(self.size(), QImage.Format_RGB32)

        self.image.fill(QColor(Qt.white))

        self.drawing = False
        self.brushSize = 2
        self.brushColor = QColor(Qt.black)

        self.lastPoint = QPoint()

        # creating menu bar
        mainMenu = self.menuBar()

        fileMenu = mainMenu.addMenu("Файл...")

        #fileOt = mainMenu.addMenu("Открыть ваши файлы...")

        b_size = mainMenu.addMenu("Изменить размер...")

        b_color = mainMenu.addMenu("Изменить цвет...")

        saveAction = QAction("Сохранить...", self)
        saveAction.setShortcut("Ctrl + S")
        fileMenu.addAction(saveAction)
        saveAction.triggered.connect(self.save)

        clearAction = QAction("Очистить...", self)
        clearAction.setShortcut("Ctrl + C")
        fileMenu.addAction(clearAction)
        clearAction.triggered.connect(self.clear)
        #FILE = QAction("Открыть мои файлы...", self)
        #fileOt.addAction(FILE)
        #FILE.triggered.connect(self.fileot)

        pix_4 = QAction("4px", self)
        b_size.addAction(pix_4)
        pix_4.triggered.connect(self.Pixel_4)

        pix_7 = QAction("7px", self)
        b_size.addAction(pix_7)
        pix_7.triggered.connect(self.Pixel_7)

        pix_9 = QAction("9px", self)
        b_size.addAction(pix_9)
        pix_9.triggered.connect(self.Pixel_9)

        pix_12 = QAction("12px", self)
        b_size.addAction(pix_12)
        pix_12.triggered.connect(self.Pixel_12)

        black = QAction("Чёрный", self)
        b_color.addAction(black)
        black.triggered.connect(self.blackColor)

        white = QAction("Белый", self)
        b_color.addAction(white)
        white.triggered.connect(self.whiteColor)

        green = QAction("Зелёный", self)
        b_color.addAction(green)
        green.triggered.connect(self.greenColor)

        yellow = QAction("Жёлтый", self)
        b_color.addAction(yellow)
        yellow.triggered.connect(self.yellowColor)

        red = QAction("Красный", self)
        b_color.addAction(red)
        red.triggered.connect(self.redColor)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.lastPoint = event.pos()

    # method for tracking mouse activity
    def mouseMoveEvent(self, event):
        if (event.buttons() & Qt.LeftButton) & self.drawing:
            painter = QPainter(self.image)
            painter.setPen(QPen(self.brushColor, self.brushSize,
                                Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.drawLine(self.lastPoint, event.pos())
            self.lastPoint = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False

    def paintEvent(self, event):
        canvasPainter = QPainter(self)
        canvasPainter.drawImage(self.rect(), self.image, self.image.rect())

    def save(self):
        filePath, _ = QFileDialog.getSaveFileName(self, "Сохранить", "",
                                                  "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")
        if filePath == "":
            return
        self.image.save(filePath)

    def clear(self):
        self.image.fill(Qt.white)
        self.update()

    def Pixel_4(self):
        self.brushSize = 4

    def Pixel_7(self):
        self.brushSize = 7

    def Pixel_9(self):
        self.brushSize = 9

    def Pixel_12(self):
        self.brushSize = 12

    def blackColor(self):
        self.brushColor = Qt.black

    def whiteColor(self):
        self.brushColor = Qt.white

    def greenColor(self):
        self.brushColor = Qt.green

    def yellowColor(self):
        self.brushColor = Qt.yellow

    def redColor(self):
        self.brushColor = Qt.red

    #def fileot(self):
        #self.FileOtobr = FileOtobr()
        #self.FileOtobr.show()

class DobTextPes(QDialog):
    def __init__(self):
        super(DobTextPes,self).__init__()
        loadUi("Pesochnica/Dobtext.ui", self)
        self.pushdobText.clicked.connect(self.dobavka)

    def dobavka(self):
        path = self.lineText.text()


'''class FileOtobr(QWidget):
    def __init__(self):
        super().__init__()
        hlay = QHBoxLayout(self)
        self.treeview = QTreeView()
        self.listview = QListView()
        hlay.addWidget(self.treeview)
        hlay.addWidget(self.listview)

        path = QDir.rootPath()
        path1 = setRootPath(None)
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
        with open("C:/Users/astra/PycharmProjects/Laboratoria1.0/resour/pesocData.txt", "a") as myfile:
            myfile.write(path+"\n")
        self.close() '''

app = QApplication(sys.argv)
mainW = Main()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainW)
widget.setFixedWidth(1120)
widget.setFixedHeight(900)
widget.show()
app.exec()
