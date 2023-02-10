import sys
import requests
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel

SCREEN_SIZE = [600, 450]

if hasattr(Qt, 'AA_EnableHighDpiScaling'):
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)


class Example(QWidget):
    SCALE_INITIAL = 0.002
    SCALE_COEFF = 2
    SCALE_MIN = 0.000125
    SCALE_MAX = 65.536

    LONGITUDE_INITIAL = 37.530887
    LATITUDE_INITIAL = 55.703118

    def __init__(self):
        super().__init__()

        self.scale = self.SCALE_INITIAL
        self.longitude = self.LONGITUDE_INITIAL
        self.latitude = self.LATITUDE_INITIAL

        self.initUI()
        self.getImage()

    def getImage(self):
        url = "http://static-maps.yandex.ru/1.x/"
        params = {
            'll': f"{self.longitude},{self.latitude}",
            'spn': f'{self.scale},{self.scale}',
            'l': 'map'
        }
        response = requests.get(url, params=params)

        if not response:
            print("Ошибка выполнения запроса:")
            print(response.url)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        self.pixmap.loadFromData(response.content, "PNG")
        self.image.clear()
        self.image.setPixmap(self.pixmap)

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')
        self.pixmap = QPixmap()
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(*SCREEN_SIZE)
        self.image.setPixmap(self.pixmap)

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        binded_keys = {
            Qt.Key_PageUp, Qt.Key_PageDown,
            Qt.Key_Up, Qt.Key_Down, Qt.Key_Left, Qt.Key_Right
        }

        is_update = event.key() in binded_keys
        match event.key():
            case  Qt.Key_PageUp:
                self.scale /= self.SCALE_COEFF
            case  Qt.Key_PageDown:
                self.scale *= self.SCALE_COEFF
            case  Qt.Key_Up:
                self.latitude += self.scale
            case  Qt.Key_Down:
                self.latitude -= self.scale
            case  Qt.Key_Left:
                self.longitude -= self.scale
            case  Qt.Key_Right:
                self.longitude += self.scale
        if self.scale > self.SCALE_MAX:
            self.scale = self.SCALE_MAX
        elif self.scale < self.SCALE_MIN:
            self.scale = self.SCALE_MIN
        if is_update:
            self.getImage()


sys._excepthook = sys.excepthook


def exception_hook(exctype, value, traceback):
    print(exctype, value, traceback)
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)


sys.excepthook = exception_hook

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
