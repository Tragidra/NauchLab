#pyuic5 UI/Login.ui -o LoginMain.py

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox,QApplication,QDialog
from PyQt5.uic import loadUi
import psycopg2
import sys
from psycopg2 import Error
from PyQt5.QtCore import QUrl, QFile, QIODevice, QByteArray #Нужно для работы видеофиксации
from PyQt5.QtWebEngineCore import QWebEngineUrlSchemeHandler, \
    QWebEngineUrlRequestInterceptor, QWebEngineUrlScheme
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile

class Login(QDialog):
    def __init__(self):
        super(Login, self).__init__()
        loadUi("Login.ui",self)
        self.vvod.clicked.connect(self.loginfunction)


    def loginfunction(self):
        login = self.loginText.text()
        parol = self.ParolText.text()
        self.label.setText("Вы нажали на кнопку!")

        if (not login) or (not parol):
            msg = QMessageBox.information(self, 'Внимание!', 'Вы не заполнили все поля.')
            return

        try:
            conn = psycopg2.connect(dbname='labpril', user='postgres',
                                password='astrafaz99', host='127.0.0.1', port="5432")
            cursor = conn.cursor()
            cursor.execute('SELECT login FROM account ')
            res = cursor.fetchone()
            flag1 = False
            flag2 = False
            for i in res:
                if i == login:
                   flag1 = True
            cursor.execute('SELECT password FROM account ')
            res2 = cursor.fetchone()
            for i in res2:
                if i == parol:
                    flag2 = True
            if (flag1 == False and flag2 == False) or (flag1 == True and flag2 == False) or (flag1 == False and flag2 == True):
                print("Данного пользователя не сущетсвует. Проверьте введённые данные.")
            elif flag1 == True and flag2 == True:
                print("Вы успешно вошли в аккаунт под логином: " + login)
                from UI.main import Main
                self.Main = Main()
                self.Main.show()
                self.close()
        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
        finally:
            if conn:
                cursor.close()
                conn.close()
                print("Соединение с PostgreSQL закрыто")



app = QApplication(sys.argv)
mainW = Login()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainW)
widget.setFixedWidth(500)
widget.setFixedHeight(400)
widget.show()
app.exec()