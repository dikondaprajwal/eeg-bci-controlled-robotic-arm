# main.py

import numpy as np

# Import your modules
from preprocessing import preprocess
from features import extract_psd
from classifier import EEGClassifier

# ROS imports
import rclpy
from ros_control import RobotController


# -----------------------------
# STEP 1: Generate dummy data
# -----------------------------
def generate_dummy_data():
    X = []
    y = []

    for i in range(100):
        eeg = np.random.randn(8, 500)

        processed = preprocess(eeg)
        features = extract_psd(processed)

        X.append(features)
        y.append(i % 4)  # 4 classes

    return np.array(X), np.array(y)


# -----------------------------
# STEP 2: Train classifier
# -----------------------------
X, y = generate_dummy_data()

clf = EEGClassifier()
clf.train(X, y)


# -----------------------------
# STEP 3: ROS setup
# -----------------------------
rclpy.init()
robot = RobotController()


# -----------------------------
# STEP 4: Run loop
# -----------------------------
while True:
    eeg = np.random.randn(8, 500)

    processed = preprocess(eeg)
    features = extract_psd(processed)

    pred, prob = clf.predict(features)

    print("Prediction:", pred, "Confidence:", prob)

    if prob > 0.20:
        robot.send_command(pred)