from main import *
from runing import Run
from ui_main import Ui_MainWindow
import datetime
import sqlite3
from PySide2 import QtCore


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
