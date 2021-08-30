from multiprocessing import Process, Queue

import sys

from PyQt5 import QtWidgets

from BCI.eeg_collecting import eeg
from tracker.collect_eye_biometric_data import collect_eye_biometrics
# from screen_capturing.screen_capturing import screen_capturing

from GUI import Ui_MainWindow



if __name__ == '__main__':
    com_port = 'COM3'

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow, com_port)
    MainWindow.show()
    sys.exit(app.exec_())

