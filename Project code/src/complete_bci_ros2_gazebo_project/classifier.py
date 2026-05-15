from sklearn.svm import SVC
from joblib import dump, load

MODEL_PATH = "svm_model.joblib"

class EEGClassifier:

    def __init__(self):

        self.model = SVC(
            kernel='rbf',
            probability=True,
            gamma='scale'
        )

    def train(self, X, y):

        self.model.fit(X, y)

        dump(self.model, MODEL_PATH)

    def load_model(self):

        self.model = load(MODEL_PATH)

    def predict(self, features, threshold=0.65):

        probs = self.model.predict_proba(features)[0]

        pred = probs.argmax()

        confidence = probs[pred]

        if confidence < threshold:
            return None, confidence

        return pred, confidence
