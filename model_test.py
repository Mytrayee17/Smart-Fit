import torch
import requests
import json
from ai_model import recommend_size
from app import app

# Part 1: Test the AI Model Loading and Processing with Dummy Input
def test_model_loading():
    try:
        # Assuming your AI model is structured as `YourModelClass()`
        from your_model_file import YourModelClass  # Replace with actual model import
        model = YourModelClass()
        model.eval()  # Set model to evaluation mode

        # Create a dummy input (adjust shape to your model’s requirements)
        dummy_input = torch.randn(1, 3, 224, 224)  # Example for a 224x224 RGB image

        # Run the model on the dummy input
        output = model(dummy_input)
        print("Model ran successfully. Output:", output)
    except Exception as e:
        print("Error in model loading or processing:", e)

# Part 2: Test the Size Recommendation Function with Sample Data
def test_recommend_size():
    sample_measurements = {
        "Height": 65,
        "Weight": 130,
        "Chest/Bust": 34,
        "Waist": 29,
        "Hips": 36
    }
    gender = "female"
    recommended_size = recommend_size(gender, sample_measurements)
    print("Recommended size for test measurements:", recommended_size)

# Part 3: Test the API Endpoint for Uploading Image and Getting a Recommendation
def test_api_endpoint():
    # Using Flask's test client to test API without running server
    with app.test_client() as client:
        # Assuming the test image is available at 'test_image.jpg'
        data = {
            'gender': 'male',
            'height': '70',
            'weight': '160',
            'ref_length': '10',  # example reference object length
            'ref_width': '5'     # example reference object width
        }
        
        # Opening a test image file
        with open("test_image.jpg", "rb") as img_file:
            data['image'] = (img_file, "test_image.jpg")
            response = client.post('/upload-image', data=data, content_type='multipart/form-data')

            # Parsing and printing the response
            if response.status_code == 200:
                print("API Test Success. Response:", response.json)
            else:
                print("API Test Failed. Status code:", response.status_code, "Response:", response.json)

# Run all tests
if __name__ == "__main__":
    print("Running model loading test...")
    test_model_loading()
    
    print("\nRunning size recommendation test...")
    test_recommend_size()

    print("\nRunning API endpoint test...")
    test_api_endpoint()
