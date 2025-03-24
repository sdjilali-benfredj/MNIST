from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_predict_endpoint():
    # Example input data (a 28x28x1 image)
    test_image = [
        [[0.0] for _ in range(28)] for _ in range(28)
    ]
    # Simulate a "1" image
    test_image[10][14] = [1.0]

    response = client.post(
        "/predict/",
        json={"image_data": test_image},
    )
    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data
    assert "confidence" in data
    # Basic check to ensure the model outputs a digit between 0 and 9
    assert 0 <= data["prediction"] <= 9