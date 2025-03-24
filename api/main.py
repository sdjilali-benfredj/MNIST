import numpy as np
from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, Counter, Gauge
from models import ImageInput, PredictionOutput
from cnn_model import cnn_model
from tensorflow import keras
from fastapi import Response
from PIL import Image

app = FastAPI()

IMAGE_SIZE = 28

# CORS Middleware (Adjust as needed for your setup)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Metrics setup
prediction_counter = Counter("prediction_count", "Number of predictions made")
model_load_time = Gauge("model_load_time", "Time to load the CNN model")
import time

start_time = time.time()
model = keras.models.load_model('cnn5r.keras')
end_time = time.time()

model_load_time.set(end_time - start_time)

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.post("/predict/", response_model=PredictionOutput)
async def predict(file: UploadFile):
    """
    Predicts the digit in the input image using the loaded CNN model.
    """
    image = Image.open(file.file).convert("L").resize((IMAGE_SIZE, IMAGE_SIZE))
    image = np.array(image).reshape(1, IMAGE_SIZE , IMAGE_SIZE) / 255.0

    predictions = cnn_model.predict(image)
    predicted_class = np.argmax(predictions, axis=1)[0]
    confidence = float(np.max(predictions, axis=1)[0])
    print("="*20)
    print("predicted_class", predicted_class)
    print("confidence", confidence)
    print("="*20)
    prediction_counter.inc()
    return PredictionOutput(prediction=int(predicted_class), confidence=confidence)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)