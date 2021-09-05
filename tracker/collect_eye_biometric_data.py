import socket
import time
import sys, os, json, csv

# Host machine IP
HOST = '127.0.0.1'
# Gazepoint Port
PORT = 4242
ADDRESS = (HOST, PORT)

data_fields_mapping = {'HR': 'heart_rate_pulse', 'GSR': 'GSR',
                       'DIAL': 'dial', 'CX': 'cursor_pos_x', 'CY': 'cursor_pos_y',
                       'FPOGY': 'eye_gaze_screen_fraction_y', 'FPOGX': 'eye_gaze_screen_fraction_x',
                       'LPMM': 'left_pupil_diameter', 'RPMM': 'right_pupil_diameter'}
# data_fields_mapping = {'LPMM': 'left_pupil_diameter', 'RPMM': 'right_pupil_diameter',
#                        'FPOGY': 'eye_gaze_screen_fraction_y',
#                        'FPOGX': 'eye_gaze_screen_fraction_x',
#                        'HRP': 'heart_rate_pulse', 'GSR': 'GSR'}


def process_biometrics(data):
    """Processes raw xml responce form biometrics server

    Args:
        data (xml string): Server response with the data

    Returns:
        dict: gazepoint data in a formatted dict
    """
    result = {}
    try:
        if 'REC' in data:
            data_dict = {item.split('=')[0]: item.split(
                '=')[1] for item in data.split(' ') if '=' in item}
            for abbr, name in data_fields_mapping.items():
                # print(data_dict[abbr].strip('\'"'))

                if data_dict[abbr].strip('\'"') in ("", " "):
                    result[name] = None
                else:
                    result[name] = float(data_dict[abbr].strip('\'"'))
    except ValueError:
        print('ValueError')

    return result


def collect_eye_biometrics(biometrics_queue):
    """Reads gazepoint's data and sends it through the given queue

    Args:
        biometrics_queue (Queue): Queue where we put gazepoint data.

    Returns:
        Nothing: Endles cycle which puts gazepoint data into the queue.
    """

    # connecting to the TCP/IP local socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(ADDRESS)

    # subscribing to the needed data streams
    s.send(str.encode('<SET ID="ENABLE_SEND_DATA" STATE="1" />\r\n'))
    s.send(str.encode('<SET ID="ENABLE_SEND_CURSOR" STATE="1" />\r\n'))
    s.send(str.encode('<SET ID="ENABLE_SEND_TIME" STATE="1" />\r\n'))
    s.send(str.encode('<SET ID="ENABLE_SEND_POG_FIX" STATE="1" />\r\n'))
    s.send(str.encode('<SET ID="ENABLE_SEND_DATA" STATE="1" />\r\n'))
    s.send(str.encode('<SET ID="ENABLE_SEND_GSR" STATE="1" />\r\n'))
    s.send(str.encode('<SET ID="ENABLE_SEND_HR" STATE="1" />\r\n'))
    s.send(str.encode('<SET ID="ENABLE_SEND_DIAL" STATE="1" />\r\n'))
    s.send(str.encode('<SET ID="ENABLE_SEND_PUPILMM" STATE="1" />\r\n'))

    while True:
        rxdat = s.recv(1024)
        data = process_biometrics(bytes.decode(rxdat))
        biometrics_queue.put(data)
        # just to slow-down  sampling rate for nice vizualization
        time.sleep(0.065)
        biometrics_queue.put(process_biometrics(bytes.decode(rxdat)))
        # just to slow-down  sampling rate for nice visualization

