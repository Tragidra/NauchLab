
import sys

from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtWidgets import QApplication, QTableWidget, QWidget


class ImageWidget(QWidget):

    def __init__(self, imagePath, parent):
        super(ImageWidget, self).__init__(parent)
        self.picture = QPixmap(imagePath)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.picture)


class TableWidget(QTableWidget):

    def setImage(self, row, col, imagePath):
        image = ImageWidget(imagePath, self)
        self.setCellWidget(row, col, image)

if __name__ == "__main__":
    app = QApplication([])
    tableWidget = TableWidget(10, 2)
    tableWidget.setImage(0, 1, "C:/Users/astra/Desktop/RPG Character Builder.url")
    tableWidget.show()
    sys.exit(app.exec_())