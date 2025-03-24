from catboost import CatBoostClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import pickle
import os 

def train_and_evaluate(X_train, y_train, X_test, y_test, model_name="catboost"):
    model = CatBoostClassifier(verbose=0)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    model_path = os.path.join("models", f"{model_name}.pkl")
    pickle.dump(model, open(model_path, 'wb'))
    print(f"Model {model_name} saved to {model_path}")
    return {
        'accuracy': accuracy_score(y_test, y_pred),
        'precision': precision_score(y_test, y_pred, average='weighted'),
        'recall': recall_score(y_test, y_pred, average='weighted'),
        'f1_score': f1_score(y_test, y_pred, average='weighted')
    }

