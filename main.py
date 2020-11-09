#from ui_functions import *
from PySide2.QtWidgets import *
import os
import sys
import platform
import sqlite3
import datetime
import youtube_dl
from PySide2.QtSql import *
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient, QIntValidator)

from ui_main import Ui_MainWindow

from ui_styles import Style
from runing import Run

count = 1

GLOBAL_STATE = 0
GLOBAL_TITLE_BAR = True

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
        view.resizeColumnsToContents()
        view.resizeRowsToContents()

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

class downloader(MainWindow, Ui_MainWindow):
    def __init__(self, parent=MainWindow):
        super(downloader).__init__(parent)
        self.url = None

    def init_args(self, url):
        self.url = url


class Functions(MainWindow, Ui_MainWindow):
    def __init__(self, parent=MainWindow):
        super(Functions, self).__init__(parent)
        self.setupUi(self)

    def start(self):
        if len(self.ui.lineEdit_2.text()) > 5:
            if self.download_folder is not None:
                qlink = self.ui.lineEdit_2.text()
                dataas = (datetime.datetime.now(), qlink)
                self.cur.execute('INSERT INTO history VALUES (?,?)', dataas)
                self.con.commit()
                self.con.close()
                self.mythread.init_args(qlink)
                self.mythread.run()
                self.locker(False)
            else:
                QtWidgets.QMessageBox.warning(self, "Ошибка", "Вы не выбрали папку")
        else:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Ссылка на видео не Указана")

    def get_folder(self):
        self.download_folder = QtWidgets.QFileDialog.getExistingDirectory(None, 'Выбрать папку для сохранения')
        os.chdir(self.download_folder)

    def handler(self, value):
        if value == 'finish':
            self.locker(False)

        else:
            self.ui.plainTextEdit_2.appendPlainText(value)

class UIFunctions(MainWindow):
    GLOBAL_STATE = 0
    GLOBAL_TITLE_BAR = True

    def maximize_restore(self):
        global GLOBAL_STATE
        status = GLOBAL_STATE
        if status == 0:
            self.showMaximized()
            GLOBAL_STATE = 1
            self.ui.horizontalLayout.setContentsMargins(0, 0, 0, 0)
            self.ui.btn_maximize_restore.setToolTip("Restore")
            self.ui.btn_maximize_restore.setIcon(QtGui.QIcon(u":/16x16/icons/16x16/cil-window-restore.png"))
            self.ui.frame_top_btns.setStyleSheet("background-color: rgb(27, 29, 35)")
            self.ui.frame_size_grip.hide()
        else:
            GLOBAL_STATE = 0
            self.showNormal()
            self.resize(self.width() + 1, self.height() + 1)
            self.ui.horizontalLayout.setContentsMargins(10, 10, 10, 10)
            self.ui.btn_maximize_restore.setToolTip("Maximize")
            self.ui.btn_maximize_restore.setIcon(QtGui.QIcon(u":/16x16/icons/16x16/cil-window-maximize.png"))
            self.ui.frame_top_btns.setStyleSheet("background-color: rgba(27, 29, 35, 200)")
            self.ui.frame_size_grip.show()

    def returStatus(self):
        return GLOBAL_STATE

    def setStatus(status):
        global GLOBAL_STATE
        GLOBAL_STATE = status

    def enableMaximumSize(self, width, height):
        if width != '' and height != '':
            self.setMaximumSize(QSize(width, height))
            self.ui.frame_size_grip.hide()
            self.ui.btn_maximize_restore.hide()

    def toggleMenu(self, maxWidth, enable):
        if enable:
            width = self.ui.frame_left_menu.width()
            maxExtend = maxWidth
            standard = 70

            if width == 70:
                widthExtended = maxExtend
            else:
                widthExtended = standard

            self.animation = QPropertyAnimation(self.ui.frame_left_menu, b"minimumWidth")
            self.animation.setDuration(300)
            self.animation.setStartValue(width)
            self.animation.setEndValue(widthExtended)
            self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animation.start()

    def removeTitleBar(status):
        global GLOBAL_TITLE_BAR
        GLOBAL_TITLE_BAR = status

    def labelTitle(self, text):
        self.ui.label_title_bar_top.setText(text)

    def labelDescription(self, text):
        self.ui.label_top_info_1.setText(text)

    def addNewMenu(self, name, objName, icon, isTopMenu):
        font = QFont()
        font.setFamily(u"Segoe UI")
        button = QPushButton(str(count), self)
        button.setObjectName(objName)
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(button.sizePolicy().hasHeightForWidth())
        button.setSizePolicy(sizePolicy3)
        button.setMinimumSize(QSize(0, 70))
        button.setLayoutDirection(Qt.LeftToRight)
        button.setFont(font)
        button.setStyleSheet(Style.style_bt_standard.replace('ICON_REPLACE', icon))
        button.setText(name)
        button.setToolTip(name)
        button.clicked.connect(self.Button)

        if isTopMenu:
            self.ui.layout_menus.addWidget(button)
        else:
            self.ui.layout_menu_bottom.addWidget(button)

    def selectMenu(getStyle):
        select = getStyle + ("QPushButton { border-right: 7px solid rgb(44, 49, 60); }")
        return select

    def deselectMenu(getStyle):
        deselect = getStyle.replace("QPushButton { border-right: 7px solid rgb(44, 49, 60); }", "")
        return deselect

    def selectStandardMenu(self, widget):
        for w in self.ui.frame_left_menu.findChildren(QPushButton):
            if w.objectName() == widget:
                w.setStyleSheet(UIFunctions.selectMenu(w.styleSheet()))

    def resetStyle(self, widget):
        for w in self.ui.frame_left_menu.findChildren(QPushButton):
            if w.objectName() != widget:
                w.setStyleSheet(UIFunctions.deselectMenu(w.styleSheet()))

    def labelPage(self, text):
        newText = '| ' + text.upper()
        self.ui.label_top_info_2.setText(newText)

    def userIcon(self, initialsTooltip, icon, showHide):
        if showHide:
            self.ui.label_user_icon.setText(initialsTooltip)

            if icon:
                style = self.ui.label_user_icon.styleSheet()
                setIcon = "QLabel { background-image: " + icon + "; }"
                self.ui.label_user_icon.setStyleSheet(style + setIcon)
                self.ui.label_user_icon.setText('')
                self.ui.label_user_icon.setToolTip(initialsTooltip)
        else:
            self.ui.label_user_icon.hide()

    def uiDefinitions(self):
        def dobleClickMaximizeRestore(event):
            if event.type() == QtCore.QEvent.MouseButtonDblClick:
                QtCore.QTimer.singleShot(250, lambda: UIFunctions.maximize_restore(self))

        if GLOBAL_TITLE_BAR:
            self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
            self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
            self.ui.frame_label_top_btns.mouseDoubleClickEvent = dobleClickMaximizeRestore
        else:
            self.ui.horizontalLayout.setContentsMargins(0, 0, 0, 0)
            self.ui.frame_label_top_btns.setContentsMargins(8, 0, 0, 5)
            self.ui.frame_label_top_btns.setMinimumHeight(42)
            self.ui.frame_icon_top_bar.hide()
            self.ui.frame_btns_right.hide()
            self.ui.frame_size_grip.hide()

        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(17)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 150))
        self.ui.frame_main.setGraphicsEffect(self.shadow)

        self.sizegrip = QSizeGrip(self.ui.frame_size_grip)
        self.sizegrip.setStyleSheet("width: 20px; height: 20px; margin 0px; padding: 0px;")

        self.ui.btn_minimize.clicked.connect(lambda: self.showMinimized())

        self.ui.btn_maximize_restore.clicked.connect(lambda: UIFunctions.maximize_restore(self))

        self.ui.btn_close.clicked.connect(lambda: self.close())

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    QtGui.QFontDatabase.addApplicationFont('fonts/segoeui.ttf')
    QtGui.QFontDatabase.addApplicationFont('fonts/segoeuib.ttf')
    window = MainWindow()
    sys.exit(app.exec_())
