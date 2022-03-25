import sys
# Класс QUrl предоставляет удобный интерфейс для работы с Urls
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QWidget
# Класс QQuickView предоставляет возможность отображать QML файлы.
from PyQt5.QtQuick import QQuickView

if __name__ == '__main__':

    app = QApplication(sys.argv)
    # Объект QQuickView, в который грузится UI для отображения
    view = QQuickView()
    view.setSource(QUrl('view.qml'))
    view.show()
    app.exec_()
    sys.exit()