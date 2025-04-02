import tensorflow as tf
from tensorflow import keras

def load_cnn_model(model_path="cnn5r.keras"):
    """Loads the pre-trained CNN model."""
    try:
        model = keras.models.load_model(model_path)
        return model
    except OSError:
        print(f"Error: Model file '{model_path}' not found. Make sure it exists in the correct location.")
        return None

cnn_model = load_cnn_model()

if cnn_model is None:
    print("CNN model loading failed. API will likely not work.")