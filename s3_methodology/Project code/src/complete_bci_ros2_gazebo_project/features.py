import numpy as np
from scipy.signal import welch
from mne.decoding import CSP

FS = 250

class FeatureExtractor:

    def __init__(self):

        self.csp = CSP(
            n_components=4,
            reg=None,
            log=True
        )

    def fit(self, X, y):

        self.csp.fit(X, y)

    def transform(self, X):

        csp_features = self.csp.transform(X)

        psd_features = []

        for sample in X:

            sample_psd = []

            for channel in sample:

                _, psd = welch(
                    channel,
                    fs=FS,
                    nperseg=128
                )

                sample_psd.extend(psd[:20])

            psd_features.append(sample_psd)

        psd_features = np.array(psd_features)

        return np.concatenate(
            [csp_features, psd_features],
            axis=1
        )
