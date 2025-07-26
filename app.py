# app.py  — FINAL, SAFE, HACKATHON VERSION
import os
from pathlib import Path
import numpy as np
import pandas as pd
import streamlit as st

# Optional (only if you really need it)
try:
    import joblib
except Exception:
    joblib = None

# -----------------------------
# ---------- CONFIG -----------
# -----------------------------
st.set_page_config(
    page_title="Smart RentBot",
    page_icon="🏠",
    layout="centered"
)

# Light CSS + optional background (won’t crash if file missing)
BG_IMG = "screenshots/bg.jpg"  # change if you have another name/path
css = f"""
<style>
    .stApp {{
        background: {'url("'+BG_IMG+'") no-repeat center/cover fixed' if Path(BG_IMG).exists() else '#0f172a'};
        color: white;
    }}
    /* White cards */
    .stMarkdown, .stSelectbox, .stNumberInput, .stButton>button {{
        color: black !important;
    }}
    .hero {{
        padding: 2rem 1rem;
        background: rgba(0,0,0,0.55);
        border-radius: 14px;
        text-align: center;
        margin-bottom: 1.2rem;
    }}
    .footer-note {{
        opacity:.6; font-size:0.8rem; margin-top:2rem;
    }}
</style>
"""
st.markdown(css, unsafe_allow_html=True)

# -----------------------------
# ------- SAFE LOADERS --------
# -----------------------------
MODEL_PATH = Path("rent_model.pkl")
MAP_PATH   = Path("mappings.pkl")
DATA_PATH  = Path("sample_houses.csv")

model = None
mappings = None

def safe_load_assets():
    global model, mappings
    ok = True
    # model
    if joblib and MODEL_PATH.exists():
        try:
            model = joblib.load(MODEL_PATH)
        except Exception as e:
            st.warning(f"⚠️ Could not load ML model ({e}). Falling back to baseline rule.")
            ok = False
    else:
        ok = False

    # mappings
    if MAP_PATH.exists():
        try:
            mappings = joblib.load(MAP_PATH) if joblib else None
        except Exception as e:
            st.warning(f"⚠️ Could not load mappings ({e}). Falling back to defaults.")
            ok = False
    else:
        ok = False

    # If anything failed -> set defaults
    if not ok or mappings is None:
        default_mappings = {
            "district": {"--Select--": -1, "Gasabo": 0, "Kicukiro": 1, "Nyarugenge": 2},
            "house_type": {"--Select--": -1, "Apartment": 0, "Bungalow": 1, "Villa": 2},
            "main_amenity": {"--Select--": -1, "Balcony": 0, "Parking": 1, "Garden": 2},
        }
        return False, default_mappings
    return True, mappings

model_ok, mappings = safe_load_assets()

# -----------------------------
# ---------- DATA -------------
# -----------------------------
def load_avg_rents():
    """Return a Series with average rents by district."""
    if DATA_PATH.exists():
        try:
            df = pd.read_csv(DATA_PATH)
            if {"district","rent_rwf"}.issubset(df.columns):
                return df.groupby("district")["rent_rwf"].mean().round()
        except Exception:
            pass
    # fallback fake numbers
    return pd.Series(
        {"Gasabo": 450000, "Kicukiro": 420000, "Nyarugenge": 480000},
        name="avg_rent_rwf"
    )

avg_rent_by_district = load_avg_rents()

# -----------------------------
# ------- HERO SECTION --------
# -----------------------------
st.markdown(
    """
<div class="hero">
    <h1>🏠 Smart RentBot</h1>
    <p>AI-powered rent prediction for Kigali (Gasabo, Kicukiro, Nyarugenge).</p>
</div>
""",
    unsafe_allow_html=True
)

# Let user know if we’re on fallback
if not model_ok:
    st.info("ℹ️ Running in **fallback (rule-based) mode** because the trained model/mappings were not found or failed to load.")

# -----------------------------
# ---------- FORM -------------
# -----------------------------
st.subheader("🔍 Enter property details")

col1, col2 = st.columns(2)
with col1:
    district = st.selectbox(
        "District",
        ["--Select--"] + [d for d in mappings["district"].keys() if d != "--Select--"]
    )
    bedrooms = st.number_input("Bedrooms", min_value=0, max_value=10, value=None, step=1, placeholder="e.g., 2")
with col2:
    house_type = st.selectbox(
        "House Type",
        ["--Select--"] + [h for h in mappings["house_type"].keys() if h != "--Select--"]
    )
    bathrooms = st.number_input("Bathrooms", min_value=0, max_value=10, value=None, step=1, placeholder="e.g., 1")

main_amenity = st.selectbox(
    "Main Amenity",
    ["--Select--"] + [a for a in mappings["main_amenity"].keys() if a != "--Select--"]
)

predict_btn = st.button("💡 Predict Rent", use_container_width=True)

# -----------------------------
# ----- PREDICTION LOGIC ------
# -----------------------------
def fallback_predict(district, house_type, bedrooms, bathrooms, main_amenity):
    """Very simple rule engine if ML model not loaded."""
    base = 300_000
    if district == "Nyarugenge": base += 80_000
    if district == "Gasabo":     base += 40_000
    if district == "Kicukiro":   base += 20_000

    if house_type == "Villa":     base += 120_000
    if house_type == "Bungalow":  base += 60_000
    if house_type == "Apartment": base += 30_000

    base += (bedrooms or 0) * 40_000
    base += (bathrooms or 0) * 30_000

    if main_amenity == "Parking": base += 20_000
    if main_amenity == "Garden":  base += 30_000
    if main_amenity == "Balcony": base += 10_000
    return float(base)

def ml_predict(district, house_type, bedrooms, bathrooms, main_amenity):
    # encode
    d  = mappings["district"].get(district, -1)
    ht = mappings["house_type"].get(house_type, -1)
    am = mappings["main_amenity"].get(main_amenity, -1)
    # basic guard
    if -1 in [d, ht, am] or None in [bedrooms, bathrooms]:
        raise ValueError("Please select all fields correctly before predicting.")
    X = np.array([[d, ht, bedrooms, bathrooms, am]])
    return float(model.predict(X)[0])

if predict_btn:
    try:
        # validate first
        if (
            district == "--Select--"
            or house_type == "--Select--"
            or main_amenity == "--Select--"
            or bedrooms is None
            or bathrooms is None
        ):
            st.warning("⚠️ Please fill **all** fields before predicting.")
        else:
            if model_ok and model is not None:
                price = ml_predict(district, house_type, bedrooms, bathrooms, main_amenity)
            else:
                price = fallback_predict(district, house_type, bedrooms, bathrooms, main_amenity)

            st.success(f"💰 **Predicted Rent:** {int(price):,} RWF")

            # Show a comparison chart (district avg + current prediction)
            compare = avg_rent_by_district.copy()
            # Add current district predicted
            compare.loc[f"Your ({district})"] = price
            st.subheader("📊 Comparison: Your prediction vs. Avg rents")
            st.bar_chart(compare)
    except Exception as e:
        st.error(f"❌ Prediction error: {e}")

st.markdown(
    """
<div class="footer-note">
    Made for DTP Hackathon • Kigali, Rwanda 🇷🇼
</div>
""",
    unsafe_allow_html=True
)
