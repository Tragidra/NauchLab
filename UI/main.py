import sys
from scipy import linalg
from PIL import ImageGrab
import numpy as np
import cv2
import os
import shutil
from PyQt5 import QtWidgets
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QMainWindow, QDialog, QApplication, QWidget, QScrollArea, \
    QVBoxLayout, QSizePolicy, QSpacerItem, QSystemTrayIcon, QStyle, QAction, QMenu, QTableWidgetItem, QPushButton, \
    QLineEdit, QInputDialog, QComboBox, QTableWidget
from PyQt5.uic import loadUi
import pyqtgraph as pg
from scipy.linalg import solve_toeplitz, solve_banded, solve_triangular

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
        self.pesochnica.triggered.connect(self.pesoc)
        self.formuli1.triggered.connect(self.formuli)
        self.experim1.triggered.connect(self.exper)


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
        os.remove('temp.txt')

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

    def pesoc(self):
        self.sapuskDoski = sapuskDoski()
        self.sapuskDoski.show()

    def formuli(self):
        self.Rachet = Rachet()
        self.Rachet.show()

    def exper(self):
        self.Exper = Exper()
        self.Exper.show()

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


class graphAnalysis(QDialog, Ui_Form):
    def __init__(self):
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
        self.tabWidget.addTab(tab1, 'Ваш график')

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

class sapuskDoski(QDialog):
    def __init__(self):
        super(sapuskDoski,self).__init__()
        loadUi("Pesochnica/vibordoska.ui", self)
        papka = 'C:/Users/astra/PycharmProjects/Laboratoria1.0/resour/proecti'
        files = os.listdir(papka)
        a = 0
        print(files)
        self.tableWidget.setRowCount(len(files))
        for i in files:
            self.tableWidget.setItem(a,0, QTableWidgetItem(i))
            a = a = 1
        self.pushButton33.clicked.connect(self.prildoska1)
        self.pushButton333.clicked.connect(self.prildoska2)
        self.pushButton30.clicked.connect(self.prildoska3)

    def prildoska1(self):
        tecfile = self.tableWidget.item(self.tableWidget.currentRow(), 0).text()
        print('C:/Users/astra/PycharmProjects/Laboratoria1.0/resour/proecti' + tecfile)
        self.close()
        self.Window = Window()
        self.Window.load(QUrl('C:/Users/astra/PycharmProjects/Laboratoria1.0/resour/proecti/' + tecfile))
        self.Window.show()

    def prildoska2(self):
        self.close()
        self.Nazvan = Nazvan()
        self.Nazvan.show()

    def prildoska3(self):
        tecfile = self.tableWidget.item(self.tableWidget.currentRow(), 0).text()
        tempdelete = 'C:/Users/astra/PycharmProjects/Laboratoria1.0/resour/proecti/' + tecfile
        os.remove(tempdelete)
        self.close()

class Exper(QDialog):
    def __init__(self):
        super(Exper, self).__init__()
        #loadUi("Exper/Exper.ui",self)
        #self.pushok.clicked.connect(self.click555)
        self.click555()

    def click555(self):
        self.close()
        self.Window = Window()
        self.Window.load(QUrl('C:/Users/astra/PycharmProjects/Laboratoria1.0/resour/cherteji/index.html'))
        self.Window.show()

class Rachet(QDialog):
    def __init__(self):
        super(Rachet,self).__init__()
        loadUi("formuli/Rachet.ui", self)
        self.classmath.clicked.connect(self.classicmath)
        self.geomet.clicked.connect(self.classicmath)
        self.stats.clicked.connect(self.classicmath)
        self.mashine.clicked.connect(self.classicmath)
        classicmath = ['Сложение матриц','Умножение матриц', 'Транспонирование матриц', 'Определитель матрицы','Обратная матрица','Solve equation a x = b. a is Hermitian positive-definite banded matrix'] #Линейная алгебра, scipy,pandas
        geometry = [] #матплот, керас и т.д.
        statistica = [] #statsmodel
        mashin = [] #Машинное обучение, skitlearn/pytorch [[1,2,3],[4,5,6]]

    def classicmath(self):
        self.ClassM = ClassM()
        self.ClassM.show()

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

app = QApplication(sys.argv)
mainW = Main()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainW)
widget.setFixedWidth(1700)
widget.setFixedHeight(800)
widget.show()
app.exec()
