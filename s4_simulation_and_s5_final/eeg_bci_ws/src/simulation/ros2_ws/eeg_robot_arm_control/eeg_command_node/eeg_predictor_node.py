import rclpy
import joblib
import mne
import os
import numpy as np

from pathlib import Path
from rclpy.node import Node
from std_msgs.msg import String


DATASET_MODEL_NAME="dataset2a_model"

MODEL_PATH = (
    f"{os.environ['EEG_BCI_MODELS_DIR']}/{DATASET_MODEL_NAME}.pkl"
)

DATASET_PATH = (
    f"{os.environ['EEG_BCI_DATASETS_DIR']}/BCI_IV_2a/A01T.gdf"
)

CLASS_MAP = {
    7: "LEFT",
    8: "RIGHT",
    9: "FORWARD",
    10: "HOME"
}


class EEGPredictorNode(Node):

    def __init__(self):

        super().__init__('eeg_predictor_node')

        self.publisher = self.create_publisher(
            String,
            '/eeg_command',
            10
        )

        self.status_publisher = self.create_publisher(
            String,
            '/eeg_status',
            10
        )

        self.model = joblib.load(
            MODEL_PATH
        )

        self.trials = self.load_trials()

        self.trial_index = 0

        self.timer = self.create_timer(
            3.0,
            self.predict_and_publish
        )

    def load_trials(self):

        raw = mne.io.read_raw_gdf(
            DATASET_PATH,
            preload=True
        )

        raw.filter(
            8,
            30
        )

        events, _ = mne.events_from_annotations(
            raw
        )

        epochs = mne.Epochs(
            raw,
            events,
            event_id={
                '769':7,
                '770':8,
                '771':9,
                '772':10
            },
            tmin=0,
            tmax=4,
            preload=True,
            baseline=None
        )

        return epochs.get_data()

    def predict_and_publish(self):

        trial = self.trials[
            self.trial_index
        ]

        prediction = self.model.predict(
            trial[np.newaxis,:,:]
        )[0]

        probability = self.model.predict_proba(
            trial[np.newaxis,:,:]
        )

        confidence = np.max(
            probability
        )

        if confidence < 0.70:

            self.get_logger().info(
                f"Rejected confidence={confidence:.2f}"
            )

            self.trial_index += 1

            if self.trial_index >= len(self.trials):
                self.trial_index = 0

            return

        command = CLASS_MAP[
            prediction
        ]

        msg = String()
        msg.data = command
        
        self.publisher.publish(
            msg
        )
        
        status = String()
        status.data = (
            f"Trial={self.trial_index} "
            f"Prediction={prediction} "
            f"Command={command} "
            f"Confidence={confidence:.2f}"
        )
        
        self.status_publisher.publish(
            status
        )

        self.get_logger().info(
            f"Prediction={prediction} "
            f"Command={command} "
            f"Confidence={confidence:.2f}"
        )

        self.trial_index += 1

        if self.trial_index >= len(
            self.trials
        ):
            self.trial_index = 0


def main(args=None):

    rclpy.init(args=args)

    node = EEGPredictorNode()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == "__main__":
    main()
