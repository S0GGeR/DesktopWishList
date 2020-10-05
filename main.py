import sys
from interface import UiMainWindow
from PyQt5 import QtWidgets


class MainWindow(QtWidgets.QMainWindow, UiMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)  # Create app
    app.setStyle('Fusion')
    window = MainWindow(
        database='wishlist',
        table_name='wishlist',
        username='username',
        password='password',
        host='127.0.0.1'
    )
    window.show()
    app.exec_()  # Main loop
