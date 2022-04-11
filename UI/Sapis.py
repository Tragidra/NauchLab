import codecs
import fileinput
import io
import json
import os
import shutil
from tempfile import mkstemp

from PyQt5 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets, QtWebChannel


def replace(file_path, pattern, subst):
    #Create temp file
    fh, abs_path = mkstemp()
    with os.fdopen(fh, 'w', encoding='utf8') as new_file:
        with io.open(file_path,encoding="utf-8") as old_file:
            for line in old_file:
                new_file.write(line.replace(pattern, subst))
    #Copy the file permissions from the old file to the new file
    shutil.copymode(file_path, abs_path)
    #Remove original file
    os.remove(file_path)
    #Move new file
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
        #backend.valueChanged.connect(self.label.setText)
        backend.valueChanged.connect(self.foo_function)
        self.channel = QtWebChannel.QWebChannel()
        self.channel.registerObject("backend", backend)
        self.webEngineView.page().setWebChannel(self.channel)

        path = "C:/Users/astra/PycharmProjects/Laboratoria1.0/resour/cherteji/index.html"
        self.webEngineView.setUrl(QtCore.QUrl.fromLocalFile(path))

    @QtCore.pyqtSlot(str)
    def foo_function(self, value):
        value = "var dataToImport = " + value
        shutil.copy('C:/Users/astra/PycharmProjects/Laboratoria1.0/resour/cherteji/basa.html', 'C:/Users/astra/PycharmProjects/Laboratoria1.0/resour/cherteji/index1.html')
        replace("C:/Users/astra/PycharmProjects/Laboratoria1.0/resour/cherteji/index1.html","var dataToImport",value)
        #os.remove("C:/Users/astra/PycharmProjects/Laboratoria1.0/resour/cherteji/index.html")
       # os.rename("C:/Users/astra/PycharmProjects/Laboratoria1.0/resour/cherteji/index1.html","C:/Users/astra/PycharmProjects/Laboratoria1.0/resour/cherteji/index.html")



if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = Widget()
    w.setFixedWidth(2000)
    w.setFixedHeight(2000)
    w.show()
    sys.exit(app.exec_())