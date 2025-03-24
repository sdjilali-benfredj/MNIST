from pydantic import BaseModel
from typing import List

class ImageInput(BaseModel):
    image_data: List[List[List[float]]]  # Assuming the input is a 28x28x1 image

class PredictionOutput(BaseModel):
    prediction: int
    confidence: float