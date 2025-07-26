# app.py — final, stable UI (background fixed + bar chart after prediction)

import streamlit as st
import pandas as pd
import joblib
from pathlib import Path
import base64

st.set_page_config(page_title="RentBot – Kigali Rent Predictor", layout="wide")

# ---------- small helper: embed local bg.jpg if it exists ----------
def set_background():
    bg_path = Path("bg.jpg")
    if bg_path.exists():
        with open(bg_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        css = f"""
        <style>
        [data-testid="stAppViewContainer"] {{
            background: url("data:image/jpg;base64,{b64}") no-repeat center center fixed;
            background-size: cover;
        }}
        [data-testid="stHeader"] {{
            background: rgba(0,0,0,0);
        }}
        .card {{
            background: rgba(255,255,255,0.92);
            padding: 20px 24px;
            border-radius: 12px;
            box-shadow: 0 1px 2px rgba(0,0,0,.08);
            margin-bottom: 18px;
        }}
        </style>
        """
    else:
        # fallback gradient if bg.jpg not found
        css = """
        <style>
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #f2f6ff 0%, #ffffff 100%);
        }
        [data-testid="stHeader"] { background: rgba(0,0,0,0); }
        .card {
            background: rgba(255,255,255,0.96);
            padding: 20px 24px;
            border-radius: 12px;
            box-shadow: 0 1px 2px rgba(0,0,0,.08);
            margin-bottom: 18px;
        }
        </style>
        """
    st.markdown(css, unsafe_allow_html=True)

set_background()

# ---------- load model & mappings (robust to amenity key) ----------
try:
    model = joblib.load("rent_model.pkl")
    mappings = joblib.load("mappings.pkl")
except Exception as e:
    st.error(f"Could not load model/mappings: {e}")
    st.stop()

amenity_key = "amenity" if "amenity" in mappings else ("main_amenity" if "main_amenity" in mappings else None)
if amenity_key is None:
    st.error("Amenity mapping not found in mappings.pkl (expected 'amenity' or 'main_amenity'). Re-run train_dummy_model.py.")
    st.stop()

district_map = mappings["district"]
house_type_map = mappings["house_type"]
amenity_map = mappings[amenity_key]

districts = ["-- Select district --"] + list(district_map.keys())
house_types = ["-- Select house type --"] + list(house_type_map.keys())
amenities = ["-- Select amenity --"] + list(amenity_map.keys())

# ---------- UI ----------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.title("RentBot")
st.write("AI-powered rent prediction for Kigali (Gasabo, Kicukiro, Nyarugenge).")
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("Enter property details")

col1, col2 = st.columns(2)
with col1:
    district = st.selectbox("District", districts, index=0)
    house_type = st.selectbox("House Type", house_types, index=0)
with col2:
    bedrooms = st.number_input("Bedrooms", min_value=1, max_value=10, value=1, step=1)
    bathrooms = st.number_input("Bathrooms", min_value=1, max_value=5, value=1, step=1)

amenity = st.selectbox("Main Amenity", amenities, index=0)

predict = st.button("Predict rent")
st.markdown("</div>", unsafe_allow_html=True)

# ---------- Predict & show chart AFTER ----------
if predict:
    errors = []
    if district.startswith("--"):
        errors.append("Please select a District.")
    if house_type.startswith("--"):
        errors.append("Please select a House Type.")
    if amenity.startswith("--"):
        errors.append("Please select an Amenity.")

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
            st.session_state["show_chart"] = True
        except Exception as e:
            st.error(f"Prediction error: {e}")

# show bar chart only after prediction
if st.session_state.get("show_chart", False):
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Average Rent by District (Example)")
    comp = pd.DataFrame({
        "District": ["Gasabo", "Kicukiro", "Nyarugenge"],
        "Average Rent (RWF)": [450000, 400000, 500000]
    }).set_index("District")
    st.bar_chart(comp)
    st.markdown("</div>", unsafe_allow_html=True)
