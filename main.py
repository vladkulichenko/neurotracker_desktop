from multiprocessing import Process, Queue

import sys

from PyQt5 import QtWidgets

from BCI import eeg
from tracker import eye_tracker
from screen_capturing import screen_capturing

from test_app_2 import Ui_MainWindow



if __name__ == '__main__':
    eye_tracker_queue = Queue()
    eeg_queue = Queue()
    monitor_queue = Queue()

    com_port = 'COM3'
    monitor_id = 1

    depicting_gazepoint = Process(target=eye_tracker, args=(eye_tracker_queue, ))
    depicting_gazepoint.start()

    depicting_openbci = Process(target=eeg, args=(com_port, eeg_queue))
    depicting_openbci.start()

    capturing_screen = Process(target=screen_capturing, args=(monitor_id, monitor_queue))
    capturing_screen.start()

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

