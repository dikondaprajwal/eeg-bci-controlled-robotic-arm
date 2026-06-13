from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

class EEGClassifier:
    def __init__(self):
        self.model = SVC(kernel='rbf', probability=True)

    def train(self, X, y):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        
        self.model.fit(X_train, y_train)
        preds = self.model.predict(X_test)
        
        acc = accuracy_score(y_test, preds)
        print("Accuracy:", acc)

    def predict(self, X):
        pred = self.model.predict([X])[0]
        prob = max(self.model.predict_proba([X])[0])
        return pred, prob