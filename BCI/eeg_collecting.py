import brainflow
import time
import numpy as np
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
from brainflow.ml_model import MLModel, BrainFlowMetrics, BrainFlowClassifiers, BrainFlowModelParams
import sys, os, json, csv

import keyboard


from BCI.psd_indexes import (approach_withdrawal_score,
                                        choice_score, cognitive_load_score,
                                        valence_score)


def eeg(com_port, eeg_queue):
    '''
    Setting parameters for board connection. Connect to board. Receiving data from board and put it into the queue.

    Args:
        com_port(str): name of the COM_port the board is connected to.
        eeg_queue (Queue): Queue where we put board data.

    Returns:
        Nothing. Function is in cycle.
    
    '''
    BoardShim.enable_dev_board_logger()

    params = BrainFlowInputParams()
    params.serial_port = com_port
    board_id = BoardIds.CYTON_DAISY_BOARD.value
    board = BoardShim(board_id, params)
    sampling_rate = BoardShim.get_sampling_rate(board_id)   
    eeg_channels = BoardShim.get_eeg_channels(board_id)

    connect_to_cyton(board)
    while True:
        openbci_data = collecting_data(board, board_id, sampling_rate, eeg_channels)
        eeg_queue.put(openbci_data)

    


def connect_to_cyton(board):
    '''
    Connects to board and preparing session.

    Args:
        board(BoardShim): board object.

    Returns:
        Bool: True in case connection is successfull. Otherwise you will see endless error with connection in the terminal.
    '''
    while True:
        try:
            board.prepare_session()
            board.start_stream(45000, 'file://cyton_data.csv:w')
            time.sleep(2)
            if board.get_current_board_data(100).any():
                print("Launching board was succeful")
                return True
            else:
                print("Launching board wasn't succeful")
                pass
        except:
            print("Oops!", sys.exc_info()[0], "occurred.")
            print("Failed loading board")
            # board.stop_stream()
            # board.release_session()
            time.sleep(2)
            pass


def collecting_data(board, board_id, sampling_rate, eeg_channels):
    '''
    Collects data from the board.

    Args:
        board(BoardShim): board object.
        board_id(int): an id of the board which app connects to.
        sampling_rate(int): sampling rate of the board.
        eeg_channels(list): list of channels indexes 1-16 channels.

    Returns:
        Dict: Dictionary with all collected and processed data from board.

    '''
    try:
        not_connected_channel = 0
        is_empty = False
        time.sleep(1) 
        data = board.get_current_board_data(125) 
        for i in range(1, 17):
            if (data[i][2] - data[i][3]) <= 2 and (data[i][2] - data[i][3]) >= -2:
                time.sleep(0.025)
                data_temp = board.get_current_board_data(4)
                if (data_temp[i][2] - data_temp[i][3]) <= 2 and (data_temp[i][2] - data_temp[i][3]) >= -2:
                    is_empty = True
                    not_connected_channel = i
                    print(i)
                    break
            DataFilter.remove_environmental_noise(data[i], board.get_sampling_rate(board_id), 0)
            #DataFilter.remove_environmental_noise(data[i], board.get_sampling_rate(board_id), 1)
        data_concentration = board.get_current_board_data(625)
        bands = DataFilter.get_avg_band_powers(data_concentration, eeg_channels, sampling_rate, True)
        feature_vector = np.concatenate((bands[0], bands[1]))
        concentration_params = BrainFlowModelParams(BrainFlowMetrics.CONCENTRATION.value, BrainFlowClassifiers.REGRESSION.value)
        concentration = MLModel(concentration_params)
        concentration.prepare()
        concentration_score = concentration.predict(feature_vector)
        if concentration_score >= 0.7:
            concentration_meaning = "Concentrated"
        elif concentration_score > 0.35 and concentration_score < 0.7:
            concentration_meaning = "Distrait"
        else:
            concentration_meaning = "Relaxed"
        #print('Concentration: %f' % concentration.predict(feature_vector))
        concentration.release()


        aw = approach_withdrawal_score(data[11, :], data[12, :])
        if aw <= -0.2:
            aw_meaning = "Strong Negative Motivation"
        elif aw > -0.2 and aw < 0:
            aw_meaning = "Negative Motivation"
        elif aw > 0 and aw < 0.3:
            aw_meaning = "Positive Motivation"
        else:
            aw_meaning = "Strong Positive Motivation"


        choise = choice_score(data[3, :], data[4, :])
        # print(data[3, :], data[4, :])
        if choise >= 0.2:
            choise_meaning = "Strong Interest"
        elif choise > 0 and choise < 0.2:
            choise_meaning = "Interest in the Object"
        else:
            choise_meaning = "Not Interesting"


        cogn_load = cognitive_load_score(data[11, :], data[12, :], data[5, :], data[6, :])
        if cogn_load >= 15:
            cogn_load_meaning = "Highly Loaded"
        elif cogn_load > 0.35 and cogn_load < 0.7:
            cogn_load_meaning = "Loaded"
        else:
            cogn_load_meaning = "Lightly Loaded"


        valence = valence_score(data[11, :], data[12, :]) 
        if valence <= -0.1:
            valence_meaning = "Negative Emotions"
        elif valence > -0.1 and valence < 0.2:
            valence_meaning = "Neutral Emotions"
        else:
            valence_meaning = "Positive Emotions"


        
        if is_empty:
            aw = 0
            choise = 0
            cogn_load = 0
            valence = 0
            concentration_score = 0
            aw_meaning = "{} channel is not connected".format(not_connected_channel)
            choise_meaning = "{} channel is not connected".format(not_connected_channel)
            cogn_load_meaning = "{} channel is not connected".format(not_connected_channel)
            valence_meaning = "{} channel is not connected".format(not_connected_channel)
            concentration_meaning = "{} channel is not connected".format(not_connected_channel)
        #print("AW: ", aw, "; Choice Score: ", choise, '; Cognit Load: ', cogn_load, '; Valence: ', valence, "\n\n")
        
        openbci_data = {"Approach_Withdrawal": [aw, aw_meaning], "Interest": [choise, choise_meaning], "Cognitive_Load": [cogn_load, cogn_load_meaning], \
        "Valence": [valence, valence_meaning], "Concentration": [concentration_score, concentration_meaning]}
        
        return openbci_data
    except:
        print("Data from BCI was not connected!", sys.exc_info()[0])
        openbci_data = {"Approach_Withdrawal": [0, "Data from BCI was not connected!"], "Interest": [0, "Data from BCI was not connected!"], "Cognitive_Load": [0, "Data from BCI was not connected!"], \
        "Valence": [0, "Data from BCI was not connected!"], "Concentration": [0, "Data from BCI was not connected!"]}
        return openbci_data
