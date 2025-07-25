import streamlit as st
import joblib
import numpy as np

# === Load the trained model and encoders ===
@st.cache_resource
def load_assets():
    model = joblib.load("model.pkl")
    location_encoder = joblib.load("location_encoder.pkl")
    category_encoder = joblib.load("category_encoder.pkl")
    amenity_encoder = joblib.load("amenity_encoder.pkl")
    scaler = joblib.load("scaler.pkl")
    return model, location_encoder, category_encoder, amenity_encoder, scaler

model, location_encoder, category_encoder, amenity_encoder, scaler = load_assets()

# === Streamlit UI ===
st.set_page_config(page_title="RentBot – Rent Prediction", page_icon="🏠", layout="centered")
st.title("🏠 RentBot – AI Rent Prediction")

st.write("Fill in the housing details below to estimate the rent price:")

# Inputs
district = st.selectbox("District", location_encoder.classes_)
house_type = st.selectbox("House Type", category_encoder.classes_)
bedrooms = st.number_input("Bedrooms", min_value=1, max_value=10, value=2)
bathrooms = st.number_input("Bathrooms", min_value=1, max_value=10, value=1)
amenity = st.selectbox("Amenity", amenity_encoder.classes_)

# Predict button
if st.button("Predict Rent"):
    try:
        # Encode inputs
        district_encoded = location_encoder.transform([district])[0]
        house_type_encoded = category_encoder.transform([house_type])[0]
        amenity_encoded = amenity_encoder.transform([amenity])[0]

        features = np.array([[district_encoded, house_type_encoded, bedrooms, bathrooms, amenity_encoded]])
        features_scaled = scaler.transform(features)

        prediction = model.predict(features_scaled)[0]
        st.success(f"**Predicted Rent: {round(prediction, 0)} RWF**")
    except Exception as e:
        st.error(f"Prediction failed: {e}")
