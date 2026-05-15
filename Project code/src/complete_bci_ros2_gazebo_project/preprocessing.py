from scipy.signal import butter, filtfilt
from mne.preprocessing import ICA
import mne

FS = 250

def butter_bandpass_filter(data, lowcut=8, highcut=30, fs=FS, order=4):

    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq

    b, a = butter(order, [low, high], btype='band')

    return filtfilt(b, a, data, axis=-1)

def apply_ica(eeg_data):

    ch_names = [f"EEG{i}" for i in range(eeg_data.shape[0])]

    info = mne.create_info(
        ch_names=ch_names,
        sfreq=FS,
        ch_types='eeg'
    )

    raw = mne.io.RawArray(eeg_data, info)

    ica = ICA(
        n_components=min(10, eeg_data.shape[0]),
        random_state=42
    )

    ica.fit(raw)

    cleaned = ica.apply(raw.copy())

    return cleaned.get_data()
