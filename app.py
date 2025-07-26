import numpy as np
import pandas as pd
import streamlit as st
from pathlib import Path

try:
    import joblib
except Exception:
    joblib = None

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Smart RentBot", page_icon="🏠", layout="centered")

# ---------------- DEFAULT MAPPINGS ----------------
DEFAULT_MAPPINGS = {
    "district": {"--Select--": -1, "Gasabo": 0, "Kicukiro": 1, "Nyarugenge": 2},
    "house_type": {"--Select--": -1, "Apartment": 0, "Bungalow": 1, "Villa": 2},
    "main_amenity": {"--Select--": -1, "Balcony": 0, "Parking": 1, "Garden": 2},
}

MODEL_PATH = Path("rent_model.pkl")
MAP_PATH = Path("mappings.pkl")
DATA_PATH = Path("sample_houses.csv")

model = None
mappings = DEFAULT_MAPPINGS.copy()

# ---------------- LOAD MODEL & MAPPINGS ----------------
def load_assets():
    global model, mappings
    # Load model
    if joblib and MODEL_PATH.exists():
        try:
            model = joblib.load(MODEL_PATH)
        except Exception:
            model = None

    # Load mappings
    if joblib and MAP_PATH.exists():
        try:
            loaded = joblib.load(MAP_PATH)
            if isinstance(loaded, dict):
                # Ensure all keys exist
                for k, v in DEFAULT_MAPPINGS.items():
                    mappings[k] = loaded.get(k, v)
        except Exception:
            mappings = DEFAULT_MAPPINGS.copy()

load_assets()

def mget(key):
    return mappings.get(key, DEFAULT_MAPPINGS[key])

# ---------------- LOAD AVG RENT DATA ----------------
def load_avg_rents():
    if DATA_PATH.exists():
        try:
            df = pd.read_csv(DATA_PATH)
            if {"district", "rent_rwf"}.issubset(df.columns):
                return df.groupby("district")["rent_rwf"].mean().round()
        except Exception:
            pass
    return pd.Series({"Gasabo": 450000, "Kicukiro": 420000, "Nyarugenge": 480000})

avg_rent_by_district = load_avg_rents()

# ---------------- UI ----------------
st.markdown(
    """
    <div style="text-align:center; padding: 10px; background-color:#F0F0F0; border-radius:10px;">
        <h1>🏠 Smart RentBot</h1>
        <p>AI-powered rent prediction for Kigali.</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.subheader("🔍 Enter property details")
col1, col2 = st.columns(2)

with col1:
    district = st.selectbox("District", ["--Select--"] + [d for d in mget("district") if d != "--Select--"])
    bedrooms = st.number_input("Bedrooms", min_value=0, max_value=10, step=1)
with col2:
    house_type = st.selectbox("House Type", ["--Select--"] + [h for h in mget("house_type") if h != "--Select--"])
    bathrooms = st.number_input("Bathrooms", min_value=0, max_value=10, step=1)

main_amenity = st.selectbox("Main Amenity", ["--Select--"] + [a for a in mget("main_amenity") if a != "--Select--"])
predict_btn = st.button("💡 Predict Rent", use_container_width=True)

# ---------------- PREDICTION ----------------
def fallback_predict(district, house_type, bedrooms, bathrooms, main_amenity):
    base = 300000
    if district == "Nyarugenge": base += 80000
    if district == "Gasabo": base += 40000
    if district == "Kicukiro": base += 20000
    if house_type == "Villa": base += 120000
    if house_type == "Bungalow": base += 60000
    if house_type == "Apartment": base += 30000
    base += (bedrooms or 0) * 40000
    base += (bathrooms or 0) * 30000
    if main_amenity == "Parking": base += 20000
    if main_amenity == "Garden": base += 30000
    if main_amenity == "Balcony": base += 10000
    return base

def ml_predict(district, house_type, bedrooms, bathrooms, main_amenity):
    d = mget("district").get(district, -1)
    ht = mget("house_type").get(house_type, -1)
    am = mget("main_amenity").get(main_amenity, -1)
    X = np.array([[d, ht, bedrooms, bathrooms, am]])
    return float(model.predict(X)[0])

if predict_btn:
    if "--Select--" in [district, house_type, main_amenity]:
        st.warning("⚠️ Please fill all fields.")
    else:
        price = ml_predict(district, house_type, bedrooms, bathrooms, main_amenity) if model else fallback_predict(
            district, house_type, bedrooms, bathrooms, main_amenity
        )
        st.success(f"💰 **Predicted Rent:** {int(price):,} RWF")
        compare = avg_rent_by_district.copy()
        compare.loc[f"Your ({district})"] = price
        st.bar_chart(compare)
