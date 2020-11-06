from ui_functions import *
from PySide2.QtWidgets import *
import os
import sys
import platform
import sqlite3
import youtube_dl
from PySide2.QtSql import *
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient, QIntValidator)

from ui_main import Ui_MainWindow

from ui_styles import Style


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.mythread = Run()
        self.url = None
        self.download_folder = None
        self.con = sqlite3.connect("history_db.sqlite")
        self.cur = self.con.cursor()
        self.mythread.mysignal.connect(self.handler)
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('history_db.sqlite')
        db.open()

        view = self.ui.tableView
        model = QSqlTableModel(self, db)
        model.setTable('history')
        model.select()

        view.setModel(model)
        view.resize(441, 571)

        UIFunctions.removeTitleBar(...)

        self.setWindowTitle('Main Window - Python Base')
        UIFunctions.labelTitle(self, 'Основное Окно - Загрузчик')
        UIFunctions.labelDescription(self, 'Описание')

        startSize = QSize(1000, 720)
        self.resize(startSize)
        self.setMinimumSize(startSize)

        self.ui.btn_toggle_menu.clicked.connect(lambda: UIFunctions.toggleMenu(self, 220, True))

        self.ui.stackedWidget.setMinimumWidth(20)
        UIFunctions.addNewMenu(self, "ГЛАВНАЯ", "btn_home", "url(:/16x16/icons/16x16/cil-home.png)", True)
        UIFunctions.addNewMenu(self, "YTDownloader", "btn_ytdown",
                               "url(C:/Users/pc/Desktop/OMGDUUUDE/icons/16x16/youtube.png)", True)
        UIFunctions.addNewMenu(self, "ИСТОРИЯ", "btn_widgets", "url(C:/Users/pc/PycharmProjects/OMGWHY/icons/16x16/history.png)",
                               False)

        UIFunctions.selectStandardMenu(self, "btn_home")

        self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)

        self.ui.pushButton_2.clicked.connect(lambda: Functions.get_folder(self))
        self.ui.pushButton_3.clicked.connect(lambda: Functions.start(self))

        UIFunctions.userIcon(self, "М.А", "", True)

        def moveWindow(event):
            if UIFunctions.returStatus(self) == 1:
                UIFunctions.maximize_restore(self)

            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()

        self.ui.frame_label_top_btns.mouseMoveEvent = moveWindow

        UIFunctions.uiDefinitions(self)



        self.show()

    def Button(self):
        btnWidget = self.sender()

        if btnWidget.objectName() == "btn_home":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)
            UIFunctions.resetStyle(self, "btn_home")
            UIFunctions.labelPage(self, "Главная")
            btnWidget.setStyleSheet(UIFunctions.selectMenu(btnWidget.styleSheet()))

        if btnWidget.objectName() == "btn_ytdown":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_ytdown)
            UIFunctions.resetStyle(self, "btn_ytdown")
            UIFunctions.labelPage(self, "Загрузки")
            btnWidget.setStyleSheet(UIFunctions.selectMenu(btnWidget.styleSheet()))

        if btnWidget.objectName() == "btn_widgets":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_widgets)
            UIFunctions.resetStyle(self, "btn_widgets")
            UIFunctions.labelPage(self, "Всякие Плюхи")
            btnWidget.setStyleSheet(UIFunctions.selectMenu(btnWidget.styleSheet()))

    def eventFilter(self, watched, event):
        if watched == self.le and event.type() == QtCore.QEvent.MouseButtonDblClick:
            print("pos: ", event.pos())

    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()
        if event.buttons() == Qt.LeftButton:
            print('МЫШЬ: Левая')
        if event.buttons() == Qt.RightButton:
            print('МЫШЬ: Правая')
        if event.buttons() == Qt.MidButton:
            print('МЫШЬ: Колесо')

    def resizeEvent(self, event):
        self.resizeFunction()
        return super(MainWindow, self).resizeEvent(event)

    def resizeFunction(self):
        print('Высота: ' + str(self.height()) + ' | Длинна: ' + str(self.width()))

    def handler(self, value):
        if value == 'finish':
            self.locker(False)

        else:
            self.ui.plainTextEdit_2.appendPlainText(value)

    def locker(self, lock_value):
        pass


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    QtGui.QFontDatabase.addApplicationFont('fonts/segoeui.ttf')
    QtGui.QFontDatabase.addApplicationFont('fonts/segoeuib.ttf')
    window = MainWindow()
    sys.exit(app.exec_())
