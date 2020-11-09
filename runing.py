from PyQt5 import QtCore
import youtube_dl

import time
from PySide2 import QtWidgets


class Run(QtCore.QThread):
    mysignal = QtCore.pyqtSignal(str)

    def run(self):
        print('Начал')
        self.mysignal.emit('Процесс скачивания запущен!')

        for i in range(1000):
            pass

        with youtube_dl.YoutubeDL({}) as ydl:
            print('Все супер')
            ydl.download([self.url])

        self.mysignal.emit('Процесс скачивания завершен!')
        self.mysignal.emit('finish')

    def init_args(self, url):
        self.url = url


