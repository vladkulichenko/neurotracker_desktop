# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'app2.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import random

import mss as mss
import numpy
from PIL import Image
import sys

import pyqtgraph as pg
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import pyautogui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import cv2

from multiprocessing import Process, Queue

from BCI.eeg_collecting import eeg
from tracker.collect_eye_biometric_data import collect_eye_biometrics

eye_tracker_queue = Queue()
eeg_queue = Queue()


class Ui_MainWindow(object):
    '''
    Interface of the application.
    '''
    def setupUi(self, MainWindow, com_port):
        '''
        Setting parameters for the interface and creating window.

        Args:
            MainWindow(MainWindow object): object of the MainWindow class.
            com_port(str): name of the COM_port the board is connected to.

        Returns:
            Nothing.
    
        '''
        self.com_port = com_port
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1920, 1080)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        pg.setConfigOption('background', 'w')
        self.centralwidget.setObjectName("centralwidget")
        self.graph_cognitive = pg.PlotWidget(self.centralwidget)
        self.graph_cognitive.setGeometry(QtCore.QRect(10, 30, 500, 250))
        self.graph_cognitive.setObjectName("graph_cognitive")
        self.graph_cognitive.setLimits(yMin=0, yMax=20)
        self.graph_cognitive.setLabel('top', 'Cognitive')
        self.graph_valence = pg.PlotWidget(self.centralwidget)
        self.graph_valence.setLimits(yMin=-1, yMax=1)
        self.graph_valence.setGeometry(QtCore.QRect(10, 300, 500, 250))
        self.graph_valence.setObjectName("graph_valence")
        self.graph_valence.setLabel('top', 'Valence')
        self.graph_interest = pg.PlotWidget(self.centralwidget)
        self.graph_interest.setGeometry(QtCore.QRect(10, 560, 500, 250))
        self.graph_interest.setObjectName("graph_interest")
        self.graph_interest.setLabel('top', 'Interest')
        self.graph_interest.setLimits(yMin=-0.5, yMax=0.5)
        self.graph_concentration = pg.PlotWidget(self.centralwidget)
        self.graph_concentration.setGeometry(QtCore.QRect(550, 620, 600, 350))
        self.graph_concentration.setObjectName("graph_concentration")
        self.graph_concentration.setLabel('top', 'Concentration')
        self.graph_concentration.setLimits(yMin=0, yMax=1)
        self.graph_approach = pg.PlotWidget(self.centralwidget)
        self.graph_approach.setGeometry(QtCore.QRect(1200, 620, 600, 350))
        self.graph_approach.setObjectName("graph_approach")
        self.graph_approach.setLimits(yMin=-1, yMax=1)
        self.graph_approach.setLabel('top', 'Approach')
        self.Screen = QtWidgets.QHBoxLayout(self.centralwidget)
        self.Feed = QtWidgets.QLabel(self.centralwidget)
        self.Screen.addWidget(self.Feed)
        self.Screen.setContentsMargins(600, 30, 1600, 800)
        self.Worker1 = Worker1()
        self.Worker1.ImageUpdate.connect(self.ImageUpdateSlot)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1130, 26))
        self.menubar.setObjectName("menubar")
        self.menuStart = QtWidgets.QMenu(self.menubar)
        self.menuStart.setObjectName("menuStart")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuSettings = QtWidgets.QMenu(self.menubar)
        self.menuSettings.setObjectName("menuSettings")
        self.menuRun = QtWidgets.QMenu(self.menubar)
        self.menuRun.setObjectName("menuRun")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionConnect_devices = QtWidgets.QAction(MainWindow)
        self.actionConnect_devices.setObjectName("actionConnect_devices")
        self.actionStart_services = QtWidgets.QAction(MainWindow)
        self.actionStart_services.setObjectName("actionStart_services")
        self.actionCreate_Project = QtWidgets.QAction(MainWindow)
        self.actionCreate_Project.setObjectName("actionCreate_Project")
        self.actionOpen_Project = QtWidgets.QAction(MainWindow)
        self.actionOpen_Project.setObjectName("actionOpen_Project")
        self.actionSave_Project = QtWidgets.QAction(MainWindow)
        self.actionSave_Project.setObjectName("actionSave_Project")
        self.actionCalibrate_Eye_Traker = QtWidgets.QAction(MainWindow)
        self.actionCalibrate_Eye_Traker.setObjectName("actionCalibrate_Eye_Traker")
        self.actionRun = QtWidgets.QAction(MainWindow)
        self.menuStart.addAction(self.actionConnect_devices)
        self.menuStart.addAction(self.actionStart_services)
        self.menuStart.addAction(self.actionCalibrate_Eye_Traker)
        self.menuFile.addAction(self.actionCreate_Project)
        self.actionCreate_Project.setShortcut('Ctrl+N')
        self.actionCreate_Project.setStatusTip('New project')
        self.menuFile.addAction(self.actionOpen_Project)
        self.actionOpen_Project.setShortcut('Ctrl+O')
        self.actionOpen_Project.setStatusTip('Open project')
        self.menuFile.addAction(self.actionSave_Project)
        self.actionSave_Project.setShortcut('Ctrl+S')
        self.actionSave_Project.setStatusTip('Save project')
        self.menuRun.addAction(self.actionRun)
        self.actionRun.setObjectName("Run")
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuStart.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menubar.addAction(self.menuRun.menuAction())

        self.menuRun.triggered.connect(self.clicked)
        self.actionCreate_Project.triggered.connect(self.create_project)
        self.actionOpen_Project.triggered.connect(self.open_project)
        self.actionSave_Project.triggered.connect(self.save_project)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def create_project(self):
        #dir_ = QtWidgets.QFileDialog.getExistingDirectory(None, 'Select project folder:', 'C:\\', QtWidgets.QFileDialog.ShowDirsOnly)
        self.created_file_name = QFileDialog.getSaveFileName(None, "Create file", "", ".prj")
        print(self.created_file_name)
        self.current_file = open(self.created_file_name[0] + self.created_file_name[1], 'a', newline="")

    def open_project(self):
        self.opened_file_name = QFileDialog.getOpenFileName(None, "Open file")
        print(self.opened_file_name)
        self.current_file = open(self.opened_file_name[0], 'a', newline="")
        
    def save_project(self):
        self.current_file.close()
        


    def clicked(self):
        '''
            Call functions in case the button "Run" was clicked.

            Returns:
                Nothing.
    
        '''
        global eye_tracker_queue, eeg_queue

        depicting_gazepoint = Process(target=collect_eye_biometrics, args=(eye_tracker_queue,))
        depicting_gazepoint.start()

        depicting_openbci = Process(target=eeg, args=(self.com_port, eeg_queue))
        depicting_openbci.start()

        self.Worker1.start()
        self.x = list(range(100))  # 100 time points
        # temp_eeg = eeg_queue.get()
        # if len(temp_eeg) > 1:
        #     self.y_interst = temp_eeg.get('Interest'[0])
        #     self.y_valence = temp_eeg.get('Valence'[0])
        #     self.y_interst = temp_eeg.get('Concentration'[0])
        #     self.y_interst = temp_eeg.get('Cognitive_Load'[0])
        #     self.y_interst = temp_eeg.get('Approach_Withdrawal'[0])
        # else:
        self.y_interst = [0] * 100  # 100 data points
        self.y_valence = [0] * 100  # 100 data points
        self.y_concentration = [0] * 100  # 100 data points
        self.y_cognitive = [0] * 100  # 100 data points
        self.y_approach = [0] * 100  # 100 data points

        pen = pg.mkPen(color=(255, 0, 0))
        self.data_line_interest = self.graph_interest.plot(self.x, self.y_interst, pen=pen)
        self.data_line_valence = self.graph_valence.plot(self.x, self.y_valence, pen=pen)
        self.data_line_cognitive = self.graph_cognitive.plot(self.x, self.y_cognitive, pen=pen)
        self.data_line_concentration = self.graph_concentration.plot(self.x, self.y_concentration, pen=pen)
        self.data_line_approach = self.graph_approach.plot(self.x, self.y_approach, pen=pen)
        self.timer = QtCore.QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_plot_data_interest)
        self.timer.timeout.connect(self.update_plot_data_valence)
        self.timer.timeout.connect(self.update_plot_data_cognitive)
        self.timer.timeout.connect(self.update_plot_data_approach)
        self.timer.timeout.connect(self.update_plot_data_concentration)

        self.timer.start()
        # self.timer1.start()

    def update_plot_data_interest(self):
        temp_eeg = []
        if len(temp_eeg) != 0:
            self.x = self.x[1:]  # Remove the first y element.
            self.x.append(self.x[-1] + 1)  # Add a new value 1 higher than the last.

            self.y_interst = self.y_interst[1:]  # Remove the first
            self.y_interst.append(temp_eeg.get('Interest'[0]))  # Add a new random value.

            self.data_line_interest.setData(self.x, self.y_interst)  # Update the data
        else:
            self.x = self.x[1:]  # Remove the first y element.
            self.x.append(self.x[-1] + 1)  # Add a new value 1 higher than the last.

            self.y_interst = self.y_interst[1:]  # Remove the first
            self.y_interst.append(random.uniform(-0.5, 0.5))  # Add a new random value.

            self.data_line_interest.setData(self.x, self.y_interst)  # Update the data

    def update_plot_data_valence(self):
        self.x = self.x[1:]  # Remove the first y element.
        self.x.append(self.x[-1] + 1)  # Add a new value 1 higher than the last.

        self.y_valence = self.y_valence[1:]  # Remove the first
        self.y_valence.append(random.uniform(-1, 1))  # Add a new random value.

        self.data_line_valence.setData(self.x, self.y_valence)  # Update the data

    def update_plot_data_cognitive(self):
        self.x = self.x[1:]  # Remove the first y element.
        self.x.append(self.x[-1] + 1)  # Add a new value 1 higher than the last.

        self.y_cognitive = self.y_cognitive[1:]  # Remove the first
        self.y_cognitive.append(random.uniform(0, 20))  # Add a new random value.

        self.data_line_cognitive.setData(self.x, self.y_cognitive)  # Update the data

    def update_plot_data_concentration(self):
        self.x = self.x[1:]  # Remove the first y element.
        self.x.append(self.x[-1] + 1)  # Add a new value 1 higher than the last.

        self.y_concentration = self.y_concentration[1:]  # Remove the first
        self.y_concentration.append(random.uniform(0, 1))  # Add a new random value.

        self.data_line_concentration.setData(self.x, self.y_concentration)  # Update the data

    def update_plot_data_cognitive(self):
        self.x = self.x[1:]  # Remove the first y element.
        self.x.append(self.x[-1] + 1)  # Add a new value 1 higher than the last.

        self.y_cognitive = self.y_cognitive[1:]  # Remove the first
        self.y_cognitive.append(random.uniform(0, 20))  # Add a new random value.

        self.data_line_cognitive.setData(self.x, self.y_cognitive)  # Update the data

    def update_plot_data_approach(self):
        self.x = self.x[1:]  # Remove the first y element.
        self.x.append(self.x[-1] + 1)  # Add a new value 1 higher than the last.

        self.y_approach = self.y_approach[1:]  # Remove the first
        self.y_approach.append(random.uniform(-1, 1))  # Add a new random value.

        self.data_line_approach.setData(self.x, self.y_approach)  # Update the data

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menuStart.setTitle(_translate("MainWindow", "Calibration"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuSettings.setTitle(_translate("MainWindow", "Settings"))
        self.menuRun.setTitle(_translate("MainWindow", "Run"))
        self.actionRun.setText(_translate("MainWindow", "Run"))
        self.actionConnect_devices.setText(_translate("MainWindow", "Connect devices"))
        self.actionStart_services.setText(_translate("MainWindow", "Calibrate BCI"))
        self.actionCreate_Project.setText(_translate("MainWindow", "Create Project"))
        self.actionOpen_Project.setText(_translate("MainWindow", "Open Project"))
        self.actionSave_Project.setText(_translate("MainWindow", "Save Project"))
        self.actionCalibrate_Eye_Traker.setText(_translate("MainWindow", "Calibrate Eye Tracker"))

    def ImageUpdateSlot(self, Image):
        self.Feed.setPixmap(QPixmap.fromImage(Image))

    def CancelFeed(self):
        self.Worker1.stop()


class Worker1(QThread):
    global eye_tracker_queue
    ImageUpdate = pyqtSignal(QImage)

    def run(self):
        list_st = []
        ThreadActive = True
        while ThreadActive:
            temp = eye_tracker_queue.get()
            radius = 10
            temp_x = temp.get('eye_gaze_screen_fraction_x')
            temp_y = temp.get('eye_gaze_screen_fraction_y')
            with mss.mss() as mss_instance:
                monitor_1 = mss_instance.monitors[2]
                img = mss_instance.grab(monitor_1)
                screen_frame = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
                if len(temp) > 1:
                    list_st.append([temp_x * 1920, temp_y * 1080])

                if len(list_st) > 2:
                    if (list_st[len(list_st) - 1][0] - 5 < list_st[len(list_st) - 1][0] < list_st[len(list_st) - 2][0] + 5 \
                            and list_st[len(list_st) - 1][1] - 5 < list_st[len(list_st) - 1][1] < list_st[len(list_st) - 2][
                        1] + 5) or \
                            (list_st[len(list_st) - 1][0] == list_st[len(list_st) - 2][0] and list_st[len(list_st) - 1][1] == list_st[len(list_st) - 2][1]):
                        radius += 50
                    circle = cv2.circle(screen_frame, (int(list_st[-1][0]), int(list_st[-1][1])), radius, (255, 255, 0), thickness=15)
                    cv2.line(circle, [int(list_st[len(list_st) - 2][0]), int(list_st[len(list_st) - 2][1])], [int(list_st[len(list_st) - 1][0]), int(list_st[len(list_st) - 1][1])], (0, 0, 0))
                    circle1 = cv2.cvtColor(circle, cv2.COLOR_BGR2RGB)
                    circle2 = cv2.cvtColor(circle1, cv2.COLOR_BGR2RGB)

                    print(list_st[len(list_st) - 2], list_st[len(list_st) - 1])
                    ConvertToQtFormat = QImage(circle2.data, circle2.shape[1], circle2.shape[0],
                                               QImage.Format_RGB888)
                    Pic = ConvertToQtFormat.scaled(1600, 550, Qt.KeepAspectRatio)
                    self.ImageUpdate.emit(Pic)


# if __name__ == "__main__":
#     import sys
#
#     com_port = 'COM3'
#
#     app = QtWidgets.QApplication(sys.argv)
#     MainWindow = QtWidgets.QMainWindow()
#     ui = Ui_MainWindow()
#     ui.setupUi(MainWindow, com_port=com_port)
#     MainWindow.showMaximized()
#     sys.exit(app.exec_())
