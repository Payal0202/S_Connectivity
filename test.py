import mysql.connector
import cv2
import numpy as np

# Connect to the MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="flask_user",
    password="flask_password",
    database="flask_app_db"
)

cursor = db.cursor()

# Fetch the image data
query = "SELECT image FROM CapturedImages WHERE id = %s"
image_id = 210  # Replace with the desired image ID
cursor.execute(query, (image_id,))
result = cursor.fetchone()

if result:
    img_data = result[0]  # Binary data of the image

    # Convert the binary data to a NumPy array
    img_array = np.frombuffer(img_data, dtype=np.uint8)

    # Decode the image
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    # Display the image using OpenCV
    cv2.imshow(f"Image ID: {image_id}", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print(f"No image found with ID: {image_id}")

# Close the connection
cursor.close()
db.close()
