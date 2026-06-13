import numpy as np

from preprocessing import butter_bandpass_filter
from features import FeatureExtractor
from classifier import EEGClassifier

np.random.seed(42)

X = np.random.randn(120, 8, 250)

y = np.random.randint(0, 4, size=120)

for i in range(len(X)):
    X[i] = butter_bandpass_filter(X[i])

extractor = FeatureExtractor()

extractor.fit(X, y)

features = extractor.transform(X)

clf = EEGClassifier()

clf.train(features, y)

print("Training complete")
