import subprocess

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.Qt import *
from UI.Pesochnica.editor import Application as editor
import sys
import os
import shutil
import functools
import tkinter

class MyMainWindow(QMainWindow):

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.config_window()
        self.create_widgets()
        self.config_widgets()
        self.create_menubar()
        self.bind_widgets()
        self.show_widgets()

    def config_window(self):
        self.setWindowTitle('Менеджер файлов Лаборатория 1.0')
        self.setMinimumHeight(600)
        self.setMinimumWidth(1000)

    def create_widgets(self):
        self.central_widget = QWidget()
        self.main_layout = QGridLayout()
        self.moveup_button = QPushButton('Свернуть всё', self)
        self.goto_lineedit = QLineEdit('C:\\', self)
        self.goto_button = QPushButton('Перейти', self)
        self.folder_view = QTreeView(self)
        self.file_view = QTreeView(self)
        self.folder_model = QFileSystemModel(self)
        self.file_model = QFileSystemModel(self)

    def config_widgets(self):
        self.main_layout.addWidget(self.moveup_button, 0, 0)
        self.main_layout.addWidget(self.goto_lineedit, 0, 1, 1, 2)
        self.main_layout.addWidget(self.goto_button, 0, 3)
        self.main_layout.addWidget(self.folder_view, 1, 0, 1, 2)
        self.main_layout.addWidget(self.file_view, 1, 2, 1, 2)

        self.central_widget.setLayout(self.main_layout)

        # Кнопка "вверх"
        self.moveup_button.setMaximumWidth(100)

        # Кнопка "перейти"
        self.goto_button.setMaximumWidth(70)
        self.setCentralWidget(self.central_widget)
        # панелі
        self.folder_model.setRootPath(None)
        self.folder_model.setFilter(QDir.AllDirs | QDir.NoDotAndDotDot)
        self.folder_view.setModel(self.folder_model)
        self.folder_view.setRootIndex(self.folder_model.index(None))
        self.folder_view.clicked[QModelIndex].connect(self.clicked_onfolder)
        self.folder_view.hideColumn(1)
        self.folder_view.hideColumn(2)
        self.folder_view.hideColumn(3)

        self.file_model.setFilter(QDir.Files)
        self.file_view.setModel(self.file_model)
        self.file_model.setReadOnly(False)
        self.file_view.setColumnWidth(0,200)
        self.file_view.setSelectionMode(QAbstractItemView.ExtendedSelection)

    def clicked_onfolder(self, index):
        selection_model = self.folder_view.selectionModel()
        index = selection_model.currentIndex()
        dir_path = self.folder_model.filePath(index)
        self.file_model.setRootPath(dir_path)
        self.file_view.setRootIndex(self.file_model.index(dir_path))

    def open_file(self):
        index = self.file_view.selectedIndexes()
        if not index:
            return
        else:
            index = index[0]
        file_path = self.file_model.filePath(index).replace('/', '\\')
        print(file_path)
        extention = os.path.splitext(file_path)[-1]
        print(extention)
        if extention in ['.txt', '.py']:
            editor.main(file_path)
        #else:
            #subprocess.Popen(file_path)
        self.file_view.update()


    def new_file(self):
        index = self.folder_view.selectedIndexes()
        if len(index) > 0:
            path = self.folder_model.filePath(index[0])
            for i in range(1, 9999999999999999):
                if not os.path.isfile(os.path.join(path, "newfile{}.txt".format(i))):
                    file_name = os.path.join(path, "newfile{}.txt".format(i))
                    break
            file_name = os.path.abspath(file_name)
            open(file_name, 'w').close()
        else:
            print("Пожалуйста, выберите папку")

    def delete_file(self):
        indexes = self.file_view.selectedIndexes()
        for i in indexes:
            self.file_model.remove(i)

    def rename_file(self):
        index = self.file_view.selectedIndexes()
        if not index:
            return
        else:
            index = index[0]
        self.file_view.edit(index)

    def copy_file(self):
        ask = QFileDialog.getExistingDirectory(self, "Выберите папку", "/home",
                                               QFileDialog.ShowDirsOnly |
                                               QFileDialog.DontResolveSymlinks)
        new_path = ask.replace('\\', '/')
        indexes = self.file_view.selectedIndexes()[::4]
        for i in indexes:
            new_filename = new_path + '/' + self.file_model.fileName(i)
            shutil.copy2(self.file_model.filePath(i), new_filename)

    def colapse(self):
        self.folder_view.collapseAll()

    def go_to(self):
        dir_path = self.goto_lineedit.text().replace('\\', '/')
        print(dir_path)
        self.file_model.setRootPath(dir_path)
        self.file_view.setRootIndex(self.file_model.index(dir_path))

        #self.file_model.setRootPath()

    def move_file(self):
        print("MOVE")
        ask = QFileDialog.getExistingDirectory(self, "Выберите папку", "/home",
                                               QFileDialog.ShowDirsOnly |
                                               QFileDialog.DontResolveSymlinks)
        if ask == '':
            return
        new_path = ask.replace('\\', '/')
        indexes = self.file_view.selectedIndexes()[::4]
        for i in indexes:
            new_filename = new_path + '/' + self.file_model.fileName(i)
            shutil.move(self.file_model.filePath(i), new_filename)

    def new_folder(self):
        index = self.folder_view.selectedIndexes()
        if len(index) > 0:
            path = self.folder_model.filePath(index[0])
            for i in range(1, 9999999999999999):
                if not os.path.isdir(os.path.join(path, "newfolder{}".format(i))):
                    file_name = os.path.join(path, "newfolder{}".format(i))
                    break
            file_name = os.path.abspath(file_name)
            os.mkdir(file_name)
        else:
            print("Please, select folder")

    def delete_folder(self):
        indexes = self.folder_view.selectedIndexes()
        for i in indexes:
            self.folder_model.remove(i)

    def rename_folder(self):
        index = self.folder_view.selectedIndexes()
        if not index:
            return
        else:
            index = index[0]
        self.folder_view.edit(index)

    def exit_application(self):
       self.close()

    def bind_widgets(self):
        self.open_file_action.triggered.connect(self.open_file)
        self.new_file_action.triggered.connect(self.new_file)
        self.delete_file_action.triggered.connect(self.delete_file)
        self.rename_file_action.triggered.connect(self.rename_file)
        self.copy_file_action.triggered.connect(self.copy_file)
        self.move_file_action.triggered.connect(self.move_file)
        self.exit_action.triggered.connect(self.exit_application)

        self.new_folder_action.triggered.connect(self.new_folder)
        self.delete_folder_action.triggered.connect(self.delete_folder)
        self.rename_folder_action.triggered.connect(self.rename_folder)

        self.goto_button.clicked.connect(functools.partial(self.go_to))
        self.moveup_button.clicked.connect(functools.partial(self.colapse))

    def create_menubar(self):

        self.exit_action = QAction('Выход...', self)
        self.exit_action.setShortcut('Ctrl+Q')

        self.new_file_action = QAction('Новый файл...', self)
        self.new_file_action.setShortcut('F4')

        self.open_file_action = QAction('Открыть файл...', self)
        self.open_file_action.setShortcut('F3')

        self.rename_file_action = QAction('Переименовать файл...', self)
        self.rename_file_action.setShortcut('F2')

        self.delete_file_action = QAction('Удалить файл...', self)
        self.delete_file_action.setShortcut(QKeySequence.Delete)

        self.copy_file_action = QAction('Копировать файл...', self)
        self.copy_file_action.setShortcut(QKeySequence.Copy)

        self.move_file_action = QAction('Переместить папку...', self)
        self.move_file_action.setShortcut(QKeySequence.Cut)

        self.new_folder_action = QAction('Новая папка...', self)
        self.new_folder_action.setShortcut('Ctrl+Shift+N')

        self.delete_folder_action = QAction('Удалить папку...', self)
        self.delete_folder_action.setShortcut('Ctrl+Shift+Del')

        self.rename_folder_action = QAction('Переименовать папку...', self)
        self.rename_folder_action.setShortcut('Ctrl+Shift+R')

        self.menubar = self.menuBar()
        self.file_menu = self.menubar.addMenu('Файл...')
        self.file_menu.addAction(self.new_file_action)
        self.file_menu.addAction(self.open_file_action)
        self.file_menu.addAction(self.rename_file_action)
        self.file_menu.addAction(self.delete_file_action)
        self.file_menu.addAction(self.copy_file_action)
        self.file_menu.addAction(self.move_file_action)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.exit_action)

        self.folder_menu = self.menubar.addMenu('Папка...')
        self.folder_menu.addAction(self.new_folder_action)
        self.folder_menu.addAction(self.delete_folder_action)
        self.folder_menu.addAction(self.rename_folder_action)

    def show_widgets(self):
        self.setLayout(self.main_layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MyMainWindow()
    mw.show()
    app.exec_()
    app.exit()
