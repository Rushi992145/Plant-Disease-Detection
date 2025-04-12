from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from PIL import Image
import os

app = Flask(__name__)  # Corrected here
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

model_path = "Transfer_ResNet50.keras"  # Ensure the model is in your project directory
model = load_model(model_path)


def preprocess_image(img):
    img = Image.open(img)
    img = img.resize((224, 224))
    img = np.array(img) / 255.0
    img = np.expand_dims(img, axis=0)
    return img


class_names = ['Apple_Apple_scab', 'Apple_Black_rot', 'Apple_Cedar_apple_rust', 'Apple_healthy', 'Blueberry_healthy',
               'Cherry(including_sour)Powdery_mildew', 'Cherry(including_sour)healthy',
               'Corn(maize)Cercospora_leaf_spot Gray_leaf_spot', 'Corn(maize)Common_rust',
               'Corn(maize)Northern_Leaf_Blight', 'Corn(maize)healthy', 'Grape_Black_rot', 'Grape_Esca(Black_Measles)',
               'Grape_Leaf_blight(Isariopsis_Leaf_Spot)', 'Grapehealthy', 'Orange_Haunglongbing(Citrus_greening)',
               'PeachBacterial_spot', 'Peach_healthy', 'Pepper,_bell_Bacterial_spot', 'Pepper,_bell_healthy',
               'Potato_Early_blight', 'Potato_Late_blight', 'Potato_healthy', 'Raspberry_healthy', 'Soybean_healthy',
               'Squash_Powdery_mildew', 'Strawberry_Leaf_scorch', 'Strawberry_healthy', 'Tomato_Bacterial_spot',
               'Tomato_Early_blight', 'Tomato_Late_blight', 'Tomato_Leaf_Mold', 'Tomato_Septoria_leaf_spot',
               'Tomato_Spider_mites Two-spotted_spider_mite', 'Tomato_Target_Spot',
               'Tomato_Tomato_Yellow_Leaf_Curl_Virus', 'Tomato_Tomato_mosaic_virus', 'Tomato_healthy']

class_indices = {i: name for i, name in enumerate(class_names)}


@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    img = preprocess_image(file)
    prediction = model.predict(img)
    predicted_class = int(np.argmax(prediction, axis=1)[0])
    predicted_class_name = class_indices[predicted_class]
    return jsonify({"predicted_class": predicted_class_name})


if __name__ == '__main__':  # Corrected here
    app.run(debug=True)
