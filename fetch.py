import numpy as np
import mysql.connector
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from PIL import Image
import io
from collections import Counter

# Load the trained model
model = load_model(r'c:\Users\kagra\Downloads\archive\AutismDataset\models\resnet_124x124.h5')  # Replace with the path to your .h5 model

# Database connection setup
db = mysql.connector.connect(
    host="localhost",
    user="flask_user",      # Replace with your MySQL username
    password="flask_password",  # Replace with your MySQL password
    database="flask_app_db"    # Replace with your MySQL database name
)

cursor = db.cursor()

# Function to load and preprocess an image
def preprocess_image(img_data, target_size=(124, 124)):  # Resize to 124x124
    img = Image.open(io.BytesIO(img_data))  # Convert LONGBLOB to an image
    img = img.resize(target_size)  # Resize image to 124x124
    img_array = np.array(img)
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    img_array = img_array / 255.0  # Normalize the image
    return img_array

# Function to fetch all images from the database and classify them
def classify_images_from_db():
    results = []
    
    # Query to fetch all images and associated metadata
    cursor.execute("SELECT id, image FROM CapturedImages")
    images = cursor.fetchall()
    
    for img_id, img_data in images:
        # Preprocess the image
        img_array = preprocess_image(img_data)

        # Get model prediction
        prediction = model.predict(img_array)

        # Assuming binary classification (output shape of [1, 1]):
        # Use `prediction[0][0]` for binary classification (probability for "autistic")
        result = 'autistic' if prediction[0][0] > 0.5 else 'non-autistic'
        results.append(result)

        print(f"Image ID: {img_id}, Prediction: {result}")
    
    return results

# Function to calculate the majority result
def calculate_majority(results):
    result_counts = Counter(results)
    majority_result = result_counts.most_common(1)[0][0]
    return majority_result, result_counts

# Classify all images in the database
results = classify_images_from_db()

# Calculate majority result
majority_result, result_counts = calculate_majority(results)

# Display results
print("\nResults Summary:")
print(f"Autistic Count: {result_counts['autistic']}")
print(f"Non-Autistic Count: {result_counts['non-autistic']}")
print(f"Majority Result: {majority_result}")
