from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import sqlite3 as sql
import os
from PyQt5.QtGui import *

dir = os.listdir(os.getcwd())
if "user.sqlite" not in dir:
    connection=sql.connect("user.sqlite",check_same_thread=False)
    q=connection.cursor()
    q.execute("CREATE TABLE Albums (id INTEGER PRIMARY KEY AUTOINCREMENT,Name varchar(40),Author varchar(40),Genre varchar(40)"
              ",Count int,Format varchar(40),Year int,Image Blob,Duration time,id_friend integer REFERENCES Users(id))")
    q.execute("CREATE TABLE Users(id INTEGER PRIMARY KEY AUTOINCREMENT, F varchar(40),I varchar(40),O varchar(40),"
              "Telephone varchar(40))")
    connection.commit()
    connection.close()

class Drag(QLineEdit):
    def __init__(self,parent,a,b,c,d):
        super().__init__()
        self.setParent(parent)
        self.setGeometry(a,b,c,d)
        self.setReadOnly(True)
        self.parent=parent
    def dropEvent(self,event):
        mimedata=event.mimeData()
        if mimedata.hasImage():
            print(mimedata.imageData)
            event.accept()
    def dragEnterEvent(self,event):
        mimedata=event.mimeData()
        event.accept()
    def dragMoveEvent(self,event):
        mimedata=event.mimeData()
        event.accept()
def takeAll():
    connection = sql.connect("user.sqlite", check_same_thread=False)
    q = connection.cursor()
    q.execute("SELECT * FROM Albums")
    result = q.fetchall()
    return result
    connection.commit()
    connection.close()
def Delete_User(id_user):
    if id_user !="":
        connection=sql.connect("user.sqlite",check_same_thread=False)
        q=connection.cursor()
        q.execute("DELETE FROM Users WHERE id = %s" % (id_user))
        connection.commit()
        connection.close()
        QMessageBox.information(del_user_window,"Успешно","Пользователь с индексом "+ id_user+" был удален")
    else:
        QMessageBox.warning(del_user_window,"Ошибка","Введите id пользователя")
        return
def Create_Album (Name,Author,Genre,Count,Format,Year,Image,Duration,id_friend):
    if Check_Album(Name) == False:
        if ( Name!="" and Author!="" and Genre!="" and Count!=""and Format!="" and Year!="" and Duration!=""):
            connection = sql.connect("user.sqlite", check_same_thread=False)
            q = connection.cursor()
            q.execute("INSERT INTO Albums (Name, Author, Genre, Count, Format, Year, Image, Duration, id_friend) VALUES ('%s', '%s', '%s','%s','%s', '%s', '%s','%s','%s')" % (Name, Author, Genre, Count, Format, Year, Image, Duration, id_friend))
            connection.commit()
            connection.close()
            QMessageBox.information(add_window,"Успешно","Албом внесен в базу данных")
        else:
            QMessageBox.warning(add_window,"Ошибка","Введены не все данные")
            return
    else:
        QMessageBox.warning(add_window,"Ошибка","Альбом с таким названием уже существует")
def Search (text):
    if text != "":
        connection = sql.connect("user.sqlite", check_same_thread=False)
        q = connection.cursor()
        q.execute("SELECT * FROM Albums WHERE Name = '%s' OR Author = '%s'" % (text,text))
        result = q.fetchall()
        res = result
        connection.commit()
        connection.close()
    else:
        connection = sql.connect("user.sqlite", check_same_thread=False)
        q = connection.cursor()
        q.execute("SELECT * FROM Albums")
        result = q.fetchall()
        res = result
        connection.commit()
        connection.close()

    Show(res)
def Delete (id):
    if id != "":
        connection = sql.connect("user.sqlite", check_same_thread=False)
        q = connection.cursor()
        q.execute("DELETE FROM Albums WHERE id = %s" % (id))
        connection.commit()
        connection.close()
        QMessageBox.information(del_window,"Успешно","Альбом успешно удален")
    else:
        QMessageBox.warning(del_window,"Ошибка","Не введен id Альбома")
        return
def Check_Album(name):
    connection=sql.connect("user.sqlite",check_same_thread=False)
    q=connection.cursor()
    q.execute("SELECT * FROM Albums WHERE Name = '%s'"%(name))
    result=q.fetchall()
    if len(result) == 0:
        return False
    else:
        return True
    connection.commit()
    connection.close()
def Show(res):
    table.clear()
    table.setHorizontalHeaderLabels(
        ["id","Название","Исполнитель","Жанр","Количество\n треков","Формат","Год","Обложка","Прод-ость",
         "Текущий \nобладатель"])
    table.setColumnCount(10)
    table.setRowCount(len(res))
    for i in range(0, len(res)):
        for j in range(0, 10):
            table.setItem(i, j, QTableWidgetItem(str(res[i][j])))
def Take_All_Users():
    connection = sql.connect("user.sqlite", check_same_thread=False)
    q = connection.cursor()
    q.execute("SELECT * FROM Users")
    result = q.fetchall()
    return result
    connection.commit()
    connection.close()
def Check_Telephone(num):
    connection=sql.connect("user.sqlite",check_same_thread=False)
    q=connection.cursor()
    q.execute("SELECT * FROM Users WHERE Telephone = '%s'"%(num))
    result=q.fetchall()
    if len(result) == 0:
        if num[0] == "8":
            num = "+7"+num[1:]
        elif num[0] == "+":
            num = "8" +num[2:]
    q.execute("SELECT * FROM Users WHERE Telephone = '%s'"%(num))
    result=q.fetchall()
    if len(result) == 0:
        return False
    else:
        return True
    connection.commit()
    connection.close()
def Create_User (Name,Surname,Ot,Telephone):
    if Check_Telephone(Telephone) == False:
        if Name != "" and Surname != "" and Ot != "" and Telephone != "":
            connection = sql.connect("user.sqlite", check_same_thread=False)
            q = connection.cursor()
            q.execute("INSERT INTO Users (F, I, O, Telephone) VALUES ('%s', '%s', '%s','%s')" % (Surname, Name, Ot, Telephone))
            connection.commit()
            connection.close()
            QMessageBox.information(create_window,"Успешно","Пользователь Добавлен")
        else:
            QMessageBox.warning(create_window,"Ошибка","Не все данные введены")
            return
    else:
        QMessageBox.warning(create_window,"Ошибка","Пользователь с таким номером\n телефона уже существует")

def check_user(id,num):
    connection=sql.connect("user.sqlite",check_same_thread=False)
    q=connection.cursor()
    q.execute("SELECT * FROM Users WHERE Telephone = '%s'"%(num))
    result=q.fetchall()
    if len(result)==0:
        if num[0]=="8":
            num="+7"+num[1:]
        elif num[0]=="+":
            num="8"+num[2:]
    else:
        q.execute("UPDATE Albums SET id_friend = '%s' WHERE id = '%s'"%(result[0][0],id))
        QMessageBox.information(Window2,"Успешно","Альбом выдан")
        connection.commit()
        connection.close()
        return
    q.execute("SELECT * FROM Users WHERE Telephone = '%s'"%(num))

    result=q.fetchall()

    if len(result)==0:
        QMessageBox.warning(Window2,"Ошибка","Не удалось выдать альбом")
        connection.commit()
        connection.close()
        return
    else:
        q.execute("UPDATE Albums SET id_friend = '%s' WHERE id = '%s'"%(result[0][0],id))
        QMessageBox.information(Window2,"Успешно","Альбом выдан")
        connection.commit()
        connection.close()
        return
def returnAlbum(id):
    connection=sql.connect("user.sqlite",check_same_thread=False)
    q=connection.cursor()
    q.execute("UPDATE Albums SET id_friend = '%s' WHERE id = '%s'" %('0',id))
    QMessageBox.information(return_window,"Успешно","Возврат альбома успешно записан")
    connection.commit()
    connection.close()

def AcceptWindow():
    global Window2
    Window2 = QDialog()
    Window2.setGeometry(400,400,400,300)
    telLine = QLineEdit(Window2)
    telLine.setGeometry(150,100,180,30)
    idTxt = QLabel("id Альбома",Window2)
    idTxt.move(45,70)
    telTxt = QLabel("Тел.номер берущего",Window2)
    telTxt.move(155,70)
    acceptBtn=QPushButton("Выдать",Window2)
    idLine = QLineEdit(Window2)
    idLine.setGeometry(40,100,80,30)
    acceptBtn.setGeometry(40,170,150,60)
    acceptBtn.clicked.connect(lambda:check_user(idLine.text(),telLine.text()))
    Window2.setWindowTitle("Выдать Альбом")
    Window2.setModal(True)
    Window2.exec_()
def ReturnWindow():
    global return_window
    return_window = QDialog()
    return_window.setGeometry(300,300,400,300)
    return_window.setWindowTitle("Вернуть Альбом")
    return_window.setModal(True)
    idTxt = QLabel("Введите id \nвозвращаемого альбома",return_window)
    idTxt.setGeometry(45,40,150,30)
    retBtn = QPushButton("Вернуть",return_window)
    retBtn.setGeometry(40,150,150,60)
    idLine=QLineEdit(return_window)
    idLine.setGeometry(40,80,100,30)
    retBtn.clicked.connect(lambda:returnAlbum(idLine.text()))
    return_window.exec_()
def AddAlbumWindow():
    global add_window
    add_window = QDialog()
    add_window.setGeometry(300,300,400,400)
    nameLine = QLineEdit(add_window)
    nameLine.setGeometry(40,40,150,30)
    nameLab = QLabel("Название Альбома",add_window)
    nameLab.setGeometry(45,10,100,20)
    authorLine=QLineEdit(add_window)
    authorLine.setGeometry(210,40,150,30)
    authorLab = QLabel("Исполнитель",add_window)
    authorLab.setGeometry(215,10,100,20)
    genreLine=QLineEdit(add_window)
    genreLine.setGeometry(40,110,100,30)
    genreLab=QLabel("Жанр",add_window)
    genreLab.setGeometry(45,80,100,20)
    countLine=QLineEdit(add_window)
    countLine.setGeometry(160,110,70,30)
    countLab=QLabel("Кол-во треков",add_window)
    countLab.setGeometry(160,80,100,20)
    formatLine=QLineEdit(add_window)
    formatLine.setGeometry(250,110,70,30)
    formatLab=QLabel("Формат",add_window)
    formatLab.setGeometry(255,80,100,20)
    lenLine =  QLineEdit(add_window)
    lenLine.setGeometry(40,180,100,30)
    lenLab=QLabel("Длительность(мин)",add_window)
    lenLab.setGeometry(40,150,100,20)
    yearLine=QLineEdit(add_window)
    yearLine.setGeometry(40,250,100,30)
    yearLab=QLabel("Год выпуска",add_window)
    yearLab.setGeometry(40,220,100,20)
    #imgDrag =Drag(add_window,210,180,150,80)
    #Недоделанный Drug, не  скидывает изображения
    acBtn = QPushButton("Внести Альбом",add_window)
    acBtn.setGeometry(40,300,150,70)
    acBtn.clicked.connect(lambda:Create_Album(nameLine.text(),authorLine.text(),genreLine.text(),countLine.text()
                                              ,formatLine.text(),yearLine.text(),"",lenLine.text(),0))
    add_window.setModal(True)
    add_window.exec_()
def delAlbumWindow():
    global del_window
    del_window = QDialog()
    del_window.setGeometry(300,300,400,300)
    idLine = QLineEdit(del_window)
    idLine.setGeometry(40,100,150,30)
    idLabel = QLabel("Введите id",del_window)
    idLabel.setGeometry(40,60,100,20)
    delBtn = QPushButton("Удалить Альбом",del_window)
    delBtn.clicked.connect(lambda:Delete(idLine.text()))
    delBtn.setGeometry(40,180,150,70)
    del_window.setModal(True)
    del_window.exec_()
def CreateUserWindow():
    global create_window
    create_window = QDialog()
    create_window.setGeometry(300,300,400,300)
    nameLine = QLineEdit(create_window)
    nameLine.setGeometry(40,40,150,30)
    nameLab = QLabel("Имя",create_window)
    nameLab.setGeometry(45,10,100,20)
    surnameLine=QLineEdit(create_window)
    surnameLine.setGeometry(210,40,150,30)
    nameLab=QLabel("Фамилия",create_window)
    nameLab.setGeometry(215,10,100,20)
    otLine=QLineEdit(create_window)
    otLine.setGeometry(40,110,150,30)
    otLab=QLabel("Отчество",create_window)
    otLab.setGeometry(45,80,100,20)
    telLine=QLineEdit(create_window)
    telLine.setGeometry(210,110,150,30)
    telLab = QLabel("Номер Телефона",create_window)
    telLab.setGeometry(215,80,100,20)
    acBtn = QPushButton("Добавить Пользователя",create_window)
    acBtn.clicked.connect(lambda:Create_User(nameLine.text(),surnameLine.text(),otLine.text(),telLine.text()))
    acBtn.setGeometry(40,180,150,60)
    create_window.setModal(True)
    create_window.exec_()
def DelUserWindow():
    global del_user_window
    del_user_window = QDialog()
    del_user_window.setGeometry(300,300,400,300)
    idLine = QLineEdit(del_user_window)
    idLine.setGeometry(40,40,150,30)
    idLab=QLabel("id пользователя",del_user_window)
    idLab.setGeometry(45,10,100,20)
    acBtn = QPushButton("Удалить",del_user_window)
    acBtn.clicked.connect(lambda:Delete_User(idLine.text()))
    acBtn.setGeometry(40,150,150,60)
    del_user_window.setModal(True)
    del_user_window.exec_()
def ShowWindow():
    global show_window
    show_window = QDialog()
    show_window.setWindowTitle("Пользователи")
    show_window.setGeometry(300,300,500,400)
    table = QTableWidget(show_window)
    table.setGeometry(0,0,500,400)
    res = Take_All_Users()
    table.setColumnCount(5)
    table.setRowCount(len(res))
    table.setHorizontalHeaderLabels(["id","Имя","Фамилия","Отчество","Тел. номер"])
    for i in range(0,len(res)):
        for j in range(0,5):
            table.setItem(i,j,QTableWidgetItem(str(res[i][j])))



    show_window.exec_()



app = QApplication(sys.argv)
root= QMainWindow()
root.setWindowTitle("Библиотека альбомов")
root.setGeometry(300,300,800,600)
searchBtn = QPushButton("Искать",root)
searchBtn.clicked.connect(lambda: Search(searchLine.text()))
searchBtn.setGeometry(450,10,120,30)
func = QLabel("ВЫДАТЬ/ВЕРНУТЬ",root)
func.setGeometry(620,10,120,30)
addBtn = QPushButton("Выдать",root)
addBtn.clicked.connect(AcceptWindow)
addBtn.setGeometry(580,50,150,50)
delBtn = QPushButton("Вернуть",root)
delBtn.clicked.connect(ReturnWindow)
delBtn.setGeometry(580,110,150,50)
albFunc = QLabel("АЛЬБОМЫ",root)
albFunc.setGeometry(630,165,150,30)
takeBtn = QPushButton("Добавить Альбом",root)
takeBtn.clicked.connect(AddAlbumWindow)
takeBtn.setGeometry(580,200,150,50)
returnBtn = QPushButton("Удалить Альбом",root)
returnBtn.clicked.connect(delAlbumWindow)
returnBtn.setGeometry(580,260,150,50)
userFunc=QLabel("ПОЛЬЗОВАТЕЛИ",root)
userFunc.setGeometry(615,320,150,30)
addUserBtn = QPushButton("Добавить Пользователя",root)
addUserBtn.clicked.connect(CreateUserWindow)
addUserBtn.setGeometry(580,350,150,50)
delUserBtn = QPushButton("Удалить Пользователя",root)
delUserBtn.clicked.connect(DelUserWindow)
delUserBtn.setGeometry(580,410,150,50)
redUserBtn = QPushButton("Список пользователей",root)
redUserBtn.clicked.connect(ShowWindow)
redUserBtn.setGeometry(580,470,150,50)
searchLine = QLineEdit(root)
searchLine.setGeometry(20,10,420,30)
res=takeAll()
view = QWidget(root)
view.setGeometry(20,50,550,550)
table = QTableWidget(view)
table.setColumnCount(10)
table.setRowCount(len(res))
table.setHorizontalHeaderLabels(["id","Название","Исполнитель","Жанр","Количество\n треков","Формат","Год","Обложка",
                                 "Прод-ость","Текущий \nобладатель"])
Show(res)
table.setGeometry(0,0,550,550)
root.show()
sys.exit(app.exec_())

