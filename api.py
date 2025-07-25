from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
import os

app = Flask(__name__)
CORS(app)  # allow calls from your HTML (different port)

# -------- Load model + encoders ----------
def must_load(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing file: {path} (check your training step & filenames)")
    return joblib.load(path)

try:
    model = must_load("model.pkl")
    location_encoder = must_load("location_encoder.pkl")
    category_encoder = must_load("category_encoder.pkl")
    amenity_encoder = must_load("amenity_encoder.pkl")
    scaler = must_load("scaler.pkl")
    print("✅ Model & encoders loaded")
except Exception as e:
    print("❌ Startup load error:", e)

# -------- Health check ----------
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "RentBot API is running. Use POST /predict"})

# -------- Predict ----------
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        print("📩 Incoming:", data)

        district = location_encoder.transform([data["District"]])[0]
        house_type = category_encoder.transform([data["HouseType"]])[0]
        bedrooms = int(data["Bedrooms"])
        bathrooms = int(data["Bathrooms"])
        amenity = amenity_encoder.transform([data["Amenity"]])[0]

        X = np.array([[district, house_type, bedrooms, bathrooms, amenity]])
        Xs = scaler.transform(X)

        y = model.predict(Xs)[0]
        print("🎯 Predicted:", y)

        return jsonify({"predicted_rent": float(y)})
    except Exception as e:
        print("❌ Error:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
