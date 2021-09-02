import numpy as np
from mne.time_frequency import psd_array_welch
from scipy.integrate import simps

from scipy.special import logsumexp


"""
Mappings from indexes in eeg trials matrix to electrodes names for GAMEEMO Dataset
    AF3 [3, :]
    AF4 [4, :]
    F3 [11, :]
    F4 [12, :]
    F7 [9, :]
    F8 [10, :]
    P7 [5, :]
    P8 [6, :]
"""


def compute_signal_band_power(signal, f_low, f_high, sfreq=125):
    """Computes spectral band power for a given signal and frequency rannge

    Args:
        signal (array): One dimensional array of signal recording
        low (int, optional): Lower frequency boundary.
        high (int, optional): Upper frequency boundary.
        sfreq (int, optional): Signal frequency.

    Returns:
        float: PSD estimate of a signal for a given spectral range
    """

    psds, freqs = psd_array_welch(
        signal, n_fft=sfreq, sfreq=sfreq, fmin=f_low, fmax=f_high, verbose='WARNING')

    # Find intersecting values in frequency vector
    idx_delta = np.logical_and(freqs >= f_low, freqs <= f_high)

    # Frequency resolution
    freq_res = freqs[1] - freqs[0]

    # Compute the absolute power by approximating the area under the curve
    band_power = simps(psds[idx_delta], dx=freq_res)
    return band_power


def approach_withdrawal_score(f3_channel, f4_channel):
    """Computes approach_withdrawal score.

    Args:
        f3_channel (array): One dimensional array of F3 signal recording.
        f4_channel (array): One dimensional array of F4 signal recording.

    Returns:
        float: Returns approach_withdrawal score.
    """

    f3_score = compute_signal_band_power(
        f3_channel, sfreq=125, f_low=8, f_high=13)
    f4_score = compute_signal_band_power(
        f4_channel, sfreq=125, f_low=8, f_high=13)

    if f4_score == 0.0 or f3_score == 0.0:
        return 0

    try:    
        aw = np.log(f4_score/f3_score)
    except:
        aw = 0    
    return aw


def valence_score(f3_channel, f4_channel):
    """Computes valence score.

    Args:
        f3_channel (array): One dimensional array of F3 signal recording.
        f4_channel (array): One dimensional array of F4 signal recording.

    Returns:
        float: Returns valence score.
    """

    f3_alpha_score = compute_signal_band_power(f3_channel, f_low=8, f_high=13)
    f3_beta_score = compute_signal_band_power(
        f3_channel, f_low=13, f_high=22)
    f4_alpha_score = compute_signal_band_power(f4_channel, f_low=8, f_high=13)
    f4_beta_score = compute_signal_band_power(
        f4_channel, f_low=13, f_high=22)
    
    if f3_alpha_score == 0.0 or f3_beta_score == 0.0 or f4_alpha_score == 0.0 or f4_beta_score == 0.0:
        return 0

    try:    
        valence = (f4_alpha_score/f4_beta_score) - (f3_alpha_score/f3_beta_score)
    except:
        valence = 0    
    return valence



def cognitive_load_score(f3_channel, f4_channel, p7_channel, p8_channel):
    """Computes cognitive_load score.

    Args:
        f3_channel (array): One dimensional array of F3 signal recording.
        f4_channel (array): One dimensional array of F4 signal recording.
        p7_channel (array): One dimensional array of P7 signal recording.
        p8_channel (array): One dimensional array of P8 signal recording.

    Returns:
        float: Returns cognitive score.
    """

    p7_alpha_score = compute_signal_band_power(p7_channel, f_low=8, f_high=12)
    p8_alpha_score = compute_signal_band_power(
        p8_channel, f_low=8, f_high=12)

    f3_theta_score = compute_signal_band_power(
        f3_channel, f_low=3.5, f_high=8)
    f4_theta_score = compute_signal_band_power(
        f4_channel, f_low=3.5, f_high=8)

    if p7_alpha_score == 0.0 or p8_alpha_score == 0.0 or f3_theta_score == 0.0 or f4_theta_score == 0.0:
        return 0

    try:    
        cognitive_load = (f3_theta_score + f4_theta_score) / (p7_alpha_score + p8_alpha_score)
    except:
        cognitive_load = 0    
    return cognitive_load 


def choice_score(af3_channel, af4_channel):
    """Computes choice score.

    Args:
        af3_channel (array): One dimensional array of AF3 signal recording.
        af4_channel (array): One dimensional array of AF4 signal recording.

    Returns:
        float: Returns choice score.
    """

    # af3_gamma_score = compute_signal_band_power(
    #     af3_channel, f_low=25, f_high=40)
    # af4_gamma_score = compute_signal_band_power(
    #     af4_channel, f_low=25, f_high=40)

    af3_gamma_score = compute_signal_band_power(
        af3_channel, f_low=22, f_high=30)
    af4_gamma_score = compute_signal_band_power(
        af4_channel, f_low=22, f_high=30)

    if af3_gamma_score == 0.0 or af4_gamma_score == 0.0:
        print("Choise score is 0")
        return 0


    try:    
        choice_score = (np.log(af3_gamma_score) - np.log(af4_gamma_score)) / (np.log(af3_gamma_score) + np.log(af4_gamma_score))
    except:
        choice_score = 0    
    return choice_score  
