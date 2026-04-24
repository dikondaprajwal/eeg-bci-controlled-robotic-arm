import numpy as np
from scipy.signal import welch

def extract_psd(eeg_data, fs=250):
    features = []
    for ch in eeg_data:
        f, Pxx = welch(ch, fs=fs)
        
        # alpha (8–13 Hz)
        alpha = np.mean(Pxx[(f >= 8) & (f <= 13)])
        
        # beta (13–30 Hz)
        beta = np.mean(Pxx[(f >= 13) & (f <= 30)])
        
        features.extend([alpha, beta])
    
    return np.array(features)




from mne.decoding import CSP

def train_csp(X, y):
    csp = CSP(n_components=4)
    X_csp = csp.fit_transform(X, y)
    return csp, X_csp

def apply_csp(csp, X):
    return csp.transform(X)