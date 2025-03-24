import tensorflow as tf

def load_cnn_model(model_path="cnn5r.keras"):
    """Loads the pre-trained CNN model."""
    return tf.keras.models.load_model(model_path)

cnn_model = load_cnn_model()