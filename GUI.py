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
import sys, os, json, csv, time

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

resolution = (1920, 1080)

codec = cv2.VideoWriter_fourcc(*"XVID")

filename = "Recording2.avi"

fps = 24
out = cv2.VideoWriter(filename, codec, fps, resolution)


class Ui_MainWindow(object):

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

        self.graph_cognitive.setGeometry(QtCore.QRect(10, 720, 920, 220))
        self.graph_cognitive.setObjectName("graph_cognitive")
        self.graph_cognitive.setLimits(yMin=0, yMax=1)
        # self.graph_valence = pg.PlotWidget(self.centralwidget)
        # self.graph_valence.setLimits(yMin=-1, yMax=1)
        # self.graph_valence.setGeometry(QtCore.QRect(10, 300, 500, 250))
        # self.graph_valence.setObjectName("graph_valence")
        # self.graph_valence.setLabel('top', 'Valence')
        # self.graph_interest = pg.PlotWidget(self.centralwidget)
        # self.graph_interest.setGeometry(QtCore.QRect(10, 560, 500, 250))
        # self.graph_interest.setObjectName("graph_interest")
        # self.graph_interest.setLabel('top', 'Interest')
        # self.graph_interest.setLimits(yMin=-0.5, yMax=0.5)
        self.graph_approach = pg.PlotWidget(self.centralwidget)

        # self.graph_approach.setGeometry(QtCore.QRect(1200, 620, 600, 350))

        self.graph_approach.setGeometry(QtCore.QRect(950, 720, 960, 220))
        self.graph_approach.setObjectName("graph_approach")
        self.graph_approach.setLimits(yMin=-1, yMax=1)
        self.graph_approach.addLegend()
        self.graph_cognitive.addLegend()
        self.graph_approach.showGrid(x=True, y=True)
        self.graph_cognitive.showGrid(x=True, y=True)
        styles = {"color": "#f00", "font-size": "20px"}
        self.graph_approach.setLabel("bottom", "Approach and Valence", **styles)
        self.graph_cognitive.setLabel("bottom", "Cognitive load and Concentration", **styles)
        self.Screen = QtWidgets.QHBoxLayout(self.centralwidget)
        self.Feed = QtWidgets.QLabel(self.centralwidget)
        self.Screen.addWidget(self.Feed)

        self.Screen.setContentsMargins(5, 5, 500, 550)

        # self.Screen.setContentsMargins(600, 30, 1600, 800)

        self.Worker1 = ScreenRecorder()
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

        self.actionCreate_Project = QtWidgets.QAction(MainWindow)
        self.actionCreate_Project.setObjectName("actionCreate_Project")
        self.actionOpen_Project = QtWidgets.QAction(MainWindow)
        self.actionOpen_Project.setObjectName("actionOpen_Project")
        self.actionSave_Project = QtWidgets.QAction(MainWindow)
        self.actionSave_Project.setObjectName("actionSave_Project")
        self.menuRun.setObjectName("menuRun")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionConnect_devices = QtWidgets.QAction(MainWindow)
        self.actionConnect_devices.setObjectName("actionConnect_devices")
        self.actionStart_OpenBCI = QtWidgets.QAction(MainWindow)
        self.actionStart_OpenBCI.setObjectName("actionStart_OpenBCI")
        self.actionCreate_Project = QtWidgets.QAction(MainWindow)
        self.actionCreate_Project.setObjectName("actionCreate_Project")
        self.actionOpen_Project = QtWidgets.QAction(MainWindow)
        self.actionOpen_Project.setObjectName("actionOpen_Project")
        self.actionCalibrate_Eye_Traker = QtWidgets.QAction(MainWindow)
        self.actionCalibrate_Eye_Traker.setObjectName("actionCalibrate_Eye_Traker")
        self.actionRun = QtWidgets.QAction(MainWindow)
        self.actionRun.setObjectName("Run")
        self.actionSettings = QtWidgets.QAction(MainWindow)
        self.actionSettings.setObjectName("Settings")
        self.menuFile.addAction(self.actionCreate_Project)
        self.actionCreate_Project.setShortcut('Ctrl+N')
        self.actionCreate_Project.setStatusTip('New project')
        self.menuFile.addAction(self.actionOpen_Project)
        self.actionOpen_Project.setShortcut('Ctrl+O')
        self.actionOpen_Project.setStatusTip('Open project')
        self.menuFile.addAction(self.actionSave_Project)
        self.actionSave_Project.setShortcut('Ctrl+S')
        self.actionSave_Project.setStatusTip('Save project')
        self.menuSettings.addAction(self.actionSettings)
        self.menuStart.addAction(self.actionConnect_devices)
        self.menuSettings.addAction(self.actionStart_OpenBCI)
        self.menuSettings.addAction(self.actionCalibrate_Eye_Traker)
        self.menuFile.addAction(self.actionCreate_Project)
        self.menuFile.addAction(self.actionOpen_Project)
        self.menuRun.addAction(self.actionRun)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuStart.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menubar.addAction(self.menuRun.menuAction())
        self.startbutton = QtWidgets.QPushButton(self.centralwidget)
        self.startbutton.setMinimumSize(QtCore.QSize(0, 23))
        self.startbutton.setIconSize(QtCore.QSize(16, 25))
        self.startbutton.setObjectName("startbutton")
        self.actionCreate_Project.triggered.connect(self.create_project)
        self.actionOpen_Project.triggered.connect(self.open_project)
        self.actionSave_Project.triggered.connect(self.save_project)
        self.menuRun.triggered.connect(self.start_analysis)
        self.actionStart_OpenBCI.triggered.connect(self.popup_bsi)
        self.actionCalibrate_Eye_Traker.triggered.connect(self.popup_gaze)
        self.startbutton.clicked.connect(self.CancelFeed)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def create_project(self):
        #dir_ = QtWidgets.QFileDialog.getExistingDirectory(None, 'Select project folder:', 'C:\\', QtWidgets.QFileDialog.ShowDirsOnly)
        global created_file
        created_file = QFileDialog.getSaveFileName(None, "Create file", "", ".prj")
        print(created_file)
        self.current_file = open(created_file[0] + created_file[1], 'a', newline="")

    def open_project(self):
        self.opened_file = QFileDialog.getOpenFileName(None, "Open file")
        print(self.opened_file)
        self.current_file = open(self.opened_file[0], 'a', newline="")
        
    def save_project(self):
        self.current_file.close()

    def popup_bsi(self):
        print("Opening a new popup window...")
        self.settings_w = MyPopup('OpenBCI')
        self.button_calibration = QPushButton(self.settings_w)
        self.button_calibration.setText('Calibration')
        self.drop_down_ports = QComboBox(self.settings_w)
        self.label = QtWidgets.QLabel(self.settings_w)
        self.label.setGeometry(QtCore.QRect(10, 106, 60, 25))
        self.label.setText('COM ports')
        self.label1 = QtWidgets.QLabel(self.settings_w)
        self.label1.setGeometry(QtCore.QRect(10, 80, 100, 25))
        self.label1.setText('Type of connection')
        self.drop_down_ports.addItem('COM2')
        self.drop_down_ports.addItem('COM3')
        self.drop_down_conn = QComboBox(self.settings_w)
        self.drop_down_conn.addItem('Type_of_connection')
        self.drop_down_conn.addItem('WiFi')
        self.drop_down_conn.addItem('Dongle')
        self.button_channels1 = QPushButton(self.settings_w)
        self.button_channels2 = QPushButton(self.settings_w)
        self.button_channels1.setText('16 Channels')
        self.button_channels2.setText('8 Channels')
        self.button_calibration.setGeometry(QRect(10, 20, 60, 60))
        self.button_channels1.setGeometry(QRect(70, 20, 70, 60))
        self.button_channels2.setGeometry(QRect(140, 20, 70, 60))
        self.drop_down_conn.setGeometry(QRect(110, 80, 150, 25))
        self.drop_down_ports.setGeometry(QRect(80, 106, 150, 25))
        self.settings_w.setGeometry(QRect(100, 100, 400, 200))
        self.settings_w.show()

    def CancelFeed(self):
        self.Worker1.stop()

    def popup_gaze(self):
        self.settings_w = MyPopup('GazePoint')
        self.button_calibration = QPushButton(self.settings_w)
        self.button_vizualization = QPushButton(self.settings_w)
        self.button_screenselection = QPushButton(self.settings_w)
        self.button_audio = QPushButton(self.settings_w)
        self.button_calibration.setText('Calibration')
        self.button_vizualization.setText('Select visualization')
        self.button_screenselection.setText('Select screen')
        self.button_audio.setText('Audio')
        self.button_audio.setGeometry(QRect(10, 20, 60, 60))
        self.button_calibration.setGeometry(QRect(70, 20, 70, 60))
        self.button_screenselection.setGeometry(QRect(140, 20, 120, 60))
        self.button_vizualization.setGeometry(QRect(140, 80, 120, 60))
        self.settings_w.setGeometry(QRect(100, 100, 400, 200))
        self.settings_w.show()

    def start_analysis(self):
        """
            Call functions in case the button "Run" was clicked.

            Returns:
                Nothing.
        """

    

        global eye_tracker_queue, eeg_queue
        self.startbutton.setText("Stop Recording")
        depicting_gazepoint = Process(target=collect_eye_biometrics, args=(eye_tracker_queue,))

        depicting_gazepoint.start()

        # depicting_openbci = Process(target=eeg, args=(self.com_port, eeg_queue))
        # depicting_openbci.start()

        self.Worker1.start()
        self.x = list(range(60))  # 100 time points
        # temp_eeg = eeg_queue.get()
        # temp_eeg = eeg_queue.get()

        global created_file

        begin_time = time.time()

        with open(created_file[0] + "_eeg_data.csv", 'a', newline="") as file:
            writer = csv.writer(file)
            if os.stat(created_file[0] + "_eeg_data.csv").st_size == 0:
                writer.writerow(["time", "Approach_Withdrawal", "Interest", "Cognitive_Load", "Valence", "Concentration"])
            try:
                current_time_eeg = time.time() - begin_time
                writer.writerow([current_time_eeg])
                #temp_eeg["Approach_Withdrawal"][0], temp_eeg["Interest"][0], temp_eeg["Cognitive_Load"][0], temp_eeg["Valence"][0], temp_eeg["Concentration"][0]])
            except KeyError:
                print("something wrong with writing openbci")
            file.close()
        # if len(temp_eeg) > 1:
        #     self.y_interst = temp_eeg.get('Interest'[0])
        #     self.y_valence = temp_eeg.get('Valence'[0])
        #     self.y_interst = temp_eeg.get('Concentration'[0])
        #     self.y_interst = temp_eeg.get('Cognitive_Load'[0])
        #     self.y_interst = temp_eeg.get('Approach_Withdrawal'[0])
        # else:

        self.y_interst = [0] * 60  # 100 data points
        self.y_valence = [0] * 60  # 100 data points
        self.y_concentration = [0] * 60  # 100 data points
        self.y_cognitive = [0] * 60  # 100 data points
        self.y_approach = [0] * 60  # 100 data points

        pen_approach = pg.mkPen(style=QtCore.Qt.SolidLine, cosmetic=True, width=2.5, color=(0, 255, 0))
        pen_valence = pg.mkPen(style=QtCore.Qt.SolidLine, cosmetic=True, width=2.5, color=(255, 0, 255))
        pen_cognitive = pg.mkPen(style=QtCore.Qt.SolidLine, cosmetic=True, width=2.5, color=(0, 0, 255))
        pen_concentration = pg.mkPen(style=QtCore.Qt.SolidLine, cosmetic=True, width=2.5, color=(255, 0, 0))
        # self.graph_interest.addLegend()
        # self.data_line_interest = self.graph_interest.plot(self.x, self.y_interst, pen=pen)
        self.data_line_valence = self.graph_approach.plot(self.x, self.y_valence, antialias=True, pen=pen_valence,
                                                          name="Valence")
        self.data_line_cognitive = self.graph_cognitive.plot(self.x, self.y_cognitive, pen=pen_cognitive,
                                                             name="Cognitive", antialias=True)
        self.data_line_concentration = self.graph_cognitive.plot(self.x, self.y_concentration, pen=pen_concentration,
                                                                 name="Concentration", antialias=True)
        self.data_line_approach = self.graph_approach.plot(self.x, self.y_approach, antialias=True, pen=pen_approach,
                                                           name="Approach")
        self.timer = QtCore.QTimer()
        self.timer.setInterval(1000)

        self.timer.timeout.connect(self.update_plot_data_valence)
        self.timer.timeout.connect(self.update_plot_data_cognitive)
        self.timer.timeout.connect(self.update_plot_data_approach)
        self.timer.timeout.connect(self.update_plot_data_concentration)

        self.timer.start()
        # self.timer1.start()

    # def update_plot_data_interest(self):
    # temp_eeg = []
    # if len(temp_eeg) != 0:
    #     self.x = self.x[1:]  # Remove the first y element.
    #     self.x.append(self.x[-1] + 1)  # Add a new value 1 higher than the last.
    #
    #     self.y_interst = self.y_interst[1:]  # Remove the first
    #     self.y_interst.append(temp_eeg.get('Interest'[0]))  # Add a new random value.
    #
    #     self.data_line_interest.setData(self.x, self.y_interst)  # Update the data
    # else:
    #     self.x = self.x[1:]  # Remove the first y element.
    #     self.x.append(self.x[-1] + 1)  # Add a new value 1 higher than the last.
    #
    #     self.y_interst = self.y_interst[1:]  # Remove the first
    #     self.y_interst.append(random.uniform(-0.5, 0.5))  # Add a new random value.
    #
    #     self.data_line_interest.setData(self.x, self.y_interst)  # Update the data

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
        self.y_cognitive.append(random.uniform(0, 1))  # Add a new random value.

        self.data_line_cognitive.setData(self.x, self.y_cognitive)  # Update the data

    def update_plot_data_concentration(self):
        self.x = self.x[1:]  # Remove the first y element.
        self.x.append(self.x[-1] + 1)  # Add a new value 1 higher than the last.

        self.y_concentration = self.y_concentration[1:]  # Remove the first
        self.y_concentration.append(random.uniform(0, 1))  # Add a new random value.

        self.data_line_concentration.setData(self.x, self.y_concentration)  # Update the data

    def update_plot_data_approach(self):
        self.x = self.x[1:]  # Remove the first y element.
        self.x.append(self.x[-1] + 1)  # Add a new value 1 higher than the last.

        self.y_approach = self.y_approach[1:]  # Remove the first
        self.y_approach.append(random.uniform(-1, 1))  # Add a new random value.

        self.data_line_approach.setData(self.x, self.y_approach)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menuStart.setTitle(_translate("MainWindow", "Calibration"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuSettings.setTitle(_translate("MainWindow", "Settings"))
        self.menuRun.setTitle(_translate("MainWindow", "Run"))
        self.actionRun.setText(_translate("MainWindow", "Run"))
        self.startbutton.setText(_translate("MainWindow", "Start Recording"))
        self.actionSettings.setText(_translate("MainWindow", "Settings"))
        self.actionConnect_devices.setText(_translate("MainWindow", "Connect devices"))
        self.actionStart_OpenBCI.setText(_translate("MainWindow", "Calibrate BCI"))
        self.actionCreate_Project.setText(_translate("MainWindow", "Create Project"))
        self.actionOpen_Project.setText(_translate("MainWindow", "Open Project"))
        self.actionSave_Project.setText(_translate("MainWindow", "Save Project"))
        self.actionCalibrate_Eye_Traker.setText(_translate("MainWindow", "Calibrate Eye Tracker"))

    def ImageUpdateSlot(self, Image):
        self.Feed.setPixmap(QPixmap.fromImage(Image))

    def CancelFeed(self):
        self.Worker1.quit()


class MyPopup(QWidget):
    def __init__(self, name):
        QWidget.__init__(self)
        self.name = name
        self.setWindowTitle(self.name)



class ScreenRecorder(QThread):
        global eye_tracker_queue, begin_time
        ImageUpdate = pyqtSignal(QImage)

        def run(self):
            list_st = []
            ThreadActive = True
            radius = 10
            while ThreadActive:
                temp = eye_tracker_queue.get()
                print(eye_tracker_queue.qsize())
                temp_x = temp.get('eye_gaze_screen_fraction_x')
                temp_y = temp.get('eye_gaze_screen_fraction_y')
                with mss.mss() as mss_instance:
                    monitor_1 = mss_instance.monitors[1]
                    img = mss_instance.grab(monitor_1)
                    screen_frame = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
                    try:
                        if temp_x is None or temp_y is None:
                            raise TypeError
                        else:
                            list_st.append([temp_x * 1920, temp_y * 1080])
                    except TypeError:
                        print(" ")

                    if len(list_st) > 2:
                        if (list_st[len(list_st) - 1][0] - 5 < list_st[len(list_st) - 1][0] < list_st[len(list_st) - 2][
                            0] + 5 \
                            and list_st[len(list_st) - 1][1] - 5 < list_st[len(list_st) - 1][1] <
                            list_st[len(list_st) - 2][
                                1] + 5) or \
                                (list_st[len(list_st) - 1][0] == list_st[len(list_st) - 2][0] and
                                 list_st[len(list_st) - 1][
                                     1] == list_st[len(list_st) - 2][1]):
                            radius += 50
                        else:
                            radius = 10
                        circle = cv2.circle(screen_frame, (int(list_st[-1][0]), int(list_st[-1][1])), radius,
                                            (255, 255, 0),
                                            thickness=15)
                        cv2.line(circle, [int(list_st[len(list_st) - 2][0]), int(list_st[len(list_st) - 2][1])],
                                 [int(list_st[len(list_st) - 1][0]), int(list_st[len(list_st) - 1][1])], (0, 0, 0))
                        circle1 = cv2.cvtColor(circle, cv2.COLOR_BGR2RGB)
                        circle2 = cv2.cvtColor(circle1, cv2.COLOR_BGR2RGB)

                        out.write(cv2.cvtColor(circle2, cv2.COLOR_BGR2RGB))

                        ConvertToQtFormat = QImage(circle2.data, circle2.shape[1], circle2.shape[0],
                                                   QImage.Format_RGB888)
                        Pic = ConvertToQtFormat.scaled(1700, 600, Qt.KeepAspectRatio)
                        self.ImageUpdate.emit(Pic)