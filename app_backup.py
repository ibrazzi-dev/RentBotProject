# ---------- Load model + mappings ----------
import streamlit as st
import pandas as pd
import joblib
from pathlib import Path

st.set_page_config(page_title="RentBot – Kigali Rent Predictor", layout="wide")

try:
    model = joblib.load("rent_model.pkl")
    mappings = joblib.load("mappings.pkl")
except Exception as e:
    st.error(f"Could not load model/mappings: {e}")
    st.stop()

# Handle both "amenity" and "main_amenity" keys safely
if "main_amenity" in mappings:
    amenity_key = "main_amenity"
elif "amenity" in mappings:
    amenity_key = "amenity"
else:
    st.error("Amenity mapping not found in mappings.pkl (expected 'amenity' or 'main_amenity'). Re-run train_dummy_model.py.")
    st.stop()

district_map = mappings["district"]
house_type_map = mappings["house_type"]
amenity_map = mappings[amenity_key]

districts = ["--Select--"] + list(district_map.keys())
house_types = ["--Select--"] + list(house_type_map.keys())
amenities = ["--Select--"] + list(amenity_map.keys())

# ---------- UI ----------
st.title("RentBot")
st.write("AI-powered rent prediction for Kigali (Gasabo, Kicukiro, Nyarugenge).")

st.header("Enter Property Details")
district = st.selectbox("District", districts, index=0)
house_type = st.selectbox("House Type", house_types, index=0)
bedrooms = st.number_input("Bedrooms", min_value=1, max_value=10, step=1)
bathrooms = st.number_input("Bathrooms", min_value=1, max_value=10, step=1)
amenity = st.selectbox("Main Amenity", amenities, index=0)

if st.button("Predict Rent"):
    errors = []
    if district == "--Select--":
        errors.append("Choose a district.")
    if house_type == "--Select--":
        errors.append("Choose a house type.")
    if amenity == "--Select--":
        errors.append("Choose an amenity.")
    if errors:
        for e in errors:
            st.warning(e)
    else:
        X = [[
            district_map[district],
            house_type_map[house_type],
            int(bedrooms),
            int(bathrooms),
            amenity_map[amenity]
        ]]
        try:
            y_pred = model.predict(X)[0]
            st.success(f"Estimated Monthly Rent: **{y_pred:,.0f} RWF**")
        except Exception as e:
            st.error(f"Prediction error: {e}")
