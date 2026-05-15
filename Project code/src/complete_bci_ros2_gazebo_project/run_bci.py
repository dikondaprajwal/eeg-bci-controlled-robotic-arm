import numpy as np
import time

from preprocessing import butter_bandpass_filter
from features import FeatureExtractor
from classifier import EEGClassifier

COMMANDS = {
    0: 'LEFT',
    1: 'RIGHT',
    2: 'GRASP',
    3: 'RELEASE'
}

extractor = FeatureExtractor()

X_train = np.random.randn(40, 8, 250)

y_train = np.random.randint(0, 4, size=40)

extractor.fit(X_train, y_train)

clf = EEGClassifier()

clf.load_model()

while True:

    eeg_window = np.random.randn(8, 250)

    eeg_window = butter_bandpass_filter(eeg_window)

    features = extractor.transform(
        eeg_window.reshape(1, 8, 250)
    )

    prediction, confidence = clf.predict(features)

    if prediction is not None:

        print(
            f"Command: {COMMANDS[prediction]} | "
            f"Confidence: {confidence:.2f}"
        )

    else:

        print(f"Low confidence: {confidence:.2f}")

    time.sleep(0.25)
