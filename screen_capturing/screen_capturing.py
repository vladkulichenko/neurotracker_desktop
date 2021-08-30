from PIL import Image  # Will need to make sure PIL is installed
import mss
import base64
from io import BytesIO
# from time import time
from flask import Flask, render_template
from flask_socketio import SocketIO, emit, send
# import cv2
  
import cv2 as cv
import numpy as np
import os
from time import time
from windowcapture import WindowCapture

# Change the working directory to the folder this script is in.
# Doing this because I'll be putting the files from each video in their own folder on GitHub
# os.chdir(os.path.dirname(os.path.abspath(__file__)))

loop_time = time()
# initialize the WindowCapture class
wincap = WindowCapture()


def start_server_capturing():
    global loop_time
    app = Flask(__name__)
    app.config['SEKRET_KEY'] = 'secret'

    socketio_3 = SocketIO(app, cors_allowed_origins="*")
    loop_time = time()
    @socketio_3.on('message')
    def handleMessage(msg):
        global loop_time
        begin_time = time()
        bytes_io = BytesIO()
        with mss.mss() as mss_instance:
            # print('This frame {} .'.format(time()-begin_time))
            monitor_1 = mss_instance.monitors[2]
            # print('This frame {} .'.format(time()-begin_time))
            screenshot = mss_instance.grab(monitor_1)
            # print('This frame {} .'.format(time()-begin_time))
            img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")  # Convert to PIL.Image
            # print('This frame {} .'.format(time()-begin_time))
            img = img.resize((960, 540))
            # print('This frame {} .'.format(time()-begin_time))
            img.save(bytes_io, "JPEG", optimize = True, 
                quality = 80)
            # print('This frame {} .'.format(time()-begin_time))
            img_str = str(base64.b64encode(bytes_io.getvalue()))[2:-1]
            # img_str = str(base64.b64encode(screenshot.bgra))[2:-1]
            emit("screen", img_str)
            # print('FPS {}'.format(1 / (time() - loop_time)))
            loop_time = time()

        # global loop_time
        # if msg == "screen":
        #     global wincap
        #     begin_time = time()
        #     screenshot = wincap.get_screenshot()
        #     print('This frame {} .'.format(time()-begin_time))
        #     #cv.imshow('Computer Vision', screenshot)

        #     emit("screen", screenshot)
        #     print('This frame {} .'.format(time()-begin_time))
        #     print('FPS {}'.format(1 / (time() - loop_time)))
        #     loop_time = time()

    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses
            # if cv.waitKey(1) == ord('q'):
            #     cv.destroyAllWindows()



            # begin_time = time()
            # bytes_io = BytesIO()
            # with mss.mss() as mss_instance:
            #     print('This frame {} .'.format(time()-begin_time))
            #     monitor_1 = mss_instance.monitors[0]
            #     print('This frame {} .'.format(time()-begin_time))
            #     screenshot = mss_instance.grab(monitor_1)
            #     print('This frame {} .'.format(time()-begin_time))
            #     img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")  # Convert to PIL.Image
            #     print('This frame {} .'.format(time()-begin_time))
            #     #img = img.resize((960, 540))
            #     print('This frame {} .'.format(time()-begin_time))
            #     img.save(bytes_io, "JPEG", optimize = True, 
            #      quality = 8)
            #     print('This frame {} .'.format(time()-begin_time))
            #     img_str = str(base64.b64encode(bytes_io.getvalue()))[2:-1]
            #     # img_str = str(base64.b64encode(screenshot.bgra))[2:-1]
            #     emit("screen", img_str)
            #     print('This frame takes {} seconds.'.format(time()-begin_time))

    socketio_3.run(app, port=5003)