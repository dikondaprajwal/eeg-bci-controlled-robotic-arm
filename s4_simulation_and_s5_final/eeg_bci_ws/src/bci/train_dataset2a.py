import mne
import joblib
import numpy as np
import os

from pathlib import Path

from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from mne.decoding import CSP


DATASET = f"{os.environ['EEG_BCI_DATASETS_DIR']}/BCI_IV_2a/A01T.gdf"
DATASET_MODEL_NAME="dataset2a_model"


def load_subject(filepath):

    print(f"\nLoading {filepath}")

    raw = mne.io.read_raw_gdf(
        filepath,
        preload=True
    )

    raw.filter(
        l_freq=8.0,
        h_freq=30.0
    )

    events, event_dict = mne.events_from_annotations(raw)

    print("\nEvent Dictionary:")
    print(event_dict)

    epochs = mne.Epochs(
        raw,
        events,
        event_id={
            '769': 7,
            '770': 8,
            '771': 9,
            '772': 10
        },
        tmin=0.0,
        tmax=4.0,
        preload=True,
        baseline=None
    )

    X = epochs.get_data()

    y = epochs.events[:, -1]

    print(f"\nTrials: {X.shape}")
    print(f"Labels: {y.shape}")

    return X, y


def train_model():

    X, y = load_subject(DATASET)

    pipeline = Pipeline([
        (
            "csp",
            CSP(
                n_components=6,
                log=True
            )
        ),
        (
            "svm",
            SVC(
                kernel="rbf",
                probability=True
            )
        )
    ])

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    print("\nTraining model...")

    pipeline.fit(
        X_train,
        y_train
    )

    y_pred = pipeline.predict(
        X_test
    )

    acc = accuracy_score(
        y_test,
        y_pred
    )

    print(f"\nAccuracy = {acc*100:.2f}%")

    model_path = (
        f"{os.environ['EEG_BCI_MODELS_DIR']}/{DATASET_MODEL_NAME}.pkl"
    )

    joblib.dump(
        pipeline,
        model_path
    )

    print(f"\nModel saved to:\n{model_path}")


if __name__ == "__main__":
    train_model()
