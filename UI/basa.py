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
        self.registr.clicked.connect(self.reg)


    def reg(self):
        self.close()
        self.Registr = Registr()
        self.Registr.show()

    def loginfunction(self):
        login = self.loginText.text()
        parol = self.ParolText.text()
        self.label.setText("Вы нажали на кнопку!")

        if (not login) or (not parol):
            msg = QMessageBox.information(self, 'Внимание!', 'Вы не заполнили все поля.')
            return

        try:
            conn = psycopg2.connect(dbname='Laboratoria', user='postgres',
                                password='astrafaz99', host='127.0.0.1', port="5432")
            cursor = conn.cursor()
            cursor.execute('SELECT login FROM account ')
            res = cursor.fetchall()
            flag1 = False
            flag2 = False
            for i in range(len(res)):
                if res[i][0] == login:
                   flag1 = True
            cursor.execute('SELECT password FROM account ')
            res2 = cursor.fetchall()
            for i in range(len(res2)):
                if res2[i][0] == parol:
                    flag2 = True
            if (flag1 == False and flag2 == False) or (flag1 == True and flag2 == False) or (flag1 == False and flag2 == True):
                print("Данного пользователя не сущетсвует. Проверьте введённые данные.")
                msg = QMessageBox.information(self, 'Данного пользователя не сущетсвует',
                                              'Проверьте введённые данные')
                for i in range(len(res)):
                    if login == res[i]:
                        print(login)
                    print(res[i])
            elif flag1 == True and flag2 == True:
                print("Вы успешно вошли в аккаунт под логином: " + login)
                tt = "SELECT id FROM account WHERE login = %s AND password = %s"
                cursor.execute(tt, (self.loginText.text(),self.ParolText.text()))
                idd = cursor.fetchone()
                print(idd[0])
                my_file = open('Temp.txt', "w+")
                my_file.write(str(idd[0]))
                my_file.close()
                self.close()
                from UI.main import Main
        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
        finally:
            if conn:
                cursor.close()
                conn.close()
                print("Соединение с PostgreSQL закрыто")

class Registr(QDialog):
    def __init__(self):
        super(Registr, self).__init__()
        loadUi("Registr.ui",self)
        self.rgi.clicked.connect(self.regi)
        self.ochi.clicked.connect(self.ochis)

    def regi(self):
        login = self.rgl1.text()
        parol = self.rgl2.text()
        if parol != self.rgl3.text():
            msg = QMessageBox.information(self, 'Внимание!', 'Введённые вами пароли различаются. Попробуйте ещё раз.')
        else:
            try:
                conn = psycopg2.connect(dbname='Laboratoria', user='postgres',
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
                if (flag1 == False and flag2 == False) or (flag1 == False and flag2 == True):
                    try:
                        connection = psycopg2.connect(dbname='Laboratoria', user='postgres',
                                                  password='astrafaz99', host='127.0.0.1', port="5432")
                        cursor = connection.cursor()

                        postgres_insert_query = """ INSERT INTO account (login, password) VALUES (%s,%s)"""
                        record_to_insert = (login, parol)
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
                    msg = QMessageBox.information(self, 'Операция прошла успешно',
                                              'Вы успешно зарегистрировались.')
                    self.close()
                    self.Login = Login()
                    self.Login.show()
                elif (flag1 == True and flag2 == False):
                    msg = QMessageBox.information(self, 'Ошибка',
                                              'Пользователь с таким логином уже существует')
                elif flag1 == True and flag2 == True:
                    msg = QMessageBox.information(self, 'Ошибка',
                                              'Такой пользователь уже существует')
                    self.close()
                    self.Login = Login()
                    self.Login.show()
            except (Exception, Error) as error:
                print("Ошибка при работе с PostgreSQL", error)
            finally:
                if conn:
                    cursor.close()
                    conn.close()
                    print("Соединение с PostgreSQL закрыто")

    def ochis(self):
        self.rgl1.clear()
        self.rgl2.clear()
        self.rgl3.clear()

app = QApplication(sys.argv)
mainW = Login()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainW)
widget.setFixedWidth(500)
widget.setFixedHeight(400)
widget.show()
app.exec()