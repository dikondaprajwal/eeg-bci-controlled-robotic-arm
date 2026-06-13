import numpy as np
from scipy.signal import butter, lfilter, iirnotch

def bandpass_filter(data, low=8, high=30, fs=250, order=4):
    nyq = 0.5 * fs
    low /= nyq
    high /= nyq
    b, a = butter(order, [low, high], btype='band')
    return lfilter(b, a, data)

def notch_filter(data, fs=250, freq=50):
    b, a = iirnotch(freq, 30, fs)
    return lfilter(b, a, data)

def preprocess(eeg_data):
    filtered = bandpass_filter(eeg_data)
    filtered = notch_filter(filtered)
    
    # normalize
    mean = np.mean(filtered, axis=1, keepdims=True)
    std = np.std(filtered, axis=1, keepdims=True)
    normalized = (filtered - mean) / (std + 1e-6)
    
    return normalized