# app.py  — clean, judge-friendly UI
import streamlit as st
import pandas as pd
import joblib
from pathlib import Path

st.set_page_config(page_title="RentBot – Kigali Rent Predictor", layout="wide")

# ---------- Minimal styling ----------
st.markdown("""
<style>
/* remove default top padding */
.block-container {padding-top: 1rem;}
/* simple white card blocks */
.block {
    background: rgba(255,255,255,0.96);
    padding: 20px 22px;
    border-radius: 12px;
    box-shadow: 0 1px 2px rgba(0,0,0,.08);
    margin-bottom: 18px;
}
h1, h2, h3 {
    margin-top: 0.2rem;
}
.note {
    font-size: 0.9rem; 
    color: #666;
}
</style>
""", unsafe_allow_html=True)

# ---------- Header ----------
st.markdown("<div class='block'>", unsafe_allow_html=True)
st.title("RentBot")
st.write("AI-powered rent prediction for Kigali (Gasabo, Kicukiro, Nyarugenge).")
st.markdown("</div>", unsafe_allow_html=True)

# ---------- Load assets ----------
model_path = Path("rent_model.pkl")
map_path = Path("mappings.pkl")

if not (model_path.exists() and map_path.exists()):
    st.error("Model files not found. Please run `python train_dummy_model.py` first.")
    st.stop()

try:
    model = joblib.load(model_path)
    mappings = joblib.load(map_path)
except Exception as e:
    st.error(f"Could not load model/mappings: {e}")
    st.stop()

district_map = mappings["district"]
house_type_map = mappings["house_type"]
amenity_map = mappings["amenity"]

districts = ["Select District"] + list(district_map.keys())
house_types = ["Select House Type"] + list(house_type_map.keys())
amenities = ["Select Amenity"] + list(amenity_map.keys())

# ---------- Form ----------
st.markdown("<div class='block'>", unsafe_allow_html=True)
st.header("Enter Property Details")

with st.form("rent_form"):
    col1, col2 = st.columns(2)

    with col1:
        district = st.selectbox("District", districts, index=0)
        house_type = st.selectbox("House Type", house_types, index=0)

    with col2:
        bedrooms = st.number_input("Bedrooms", min_value=1, max_value=10, value=None, step=1, placeholder="e.g. 2")
        bathrooms = st.number_input("Bathrooms", min_value=1, max_value=5, value=None, step=1, placeholder="e.g. 1")

    amenity = st.selectbox("Main Amenity", amenities, index=0)

    submitted = st.form_submit_button("Predict Rent")

st.markdown("</div>", unsafe_allow_html=True)

# ---------- Predict ----------
if submitted:
    errors = []
    if district == "Select District":
        errors.append("Please choose a district.")
    if house_type == "Select House Type":
        errors.append("Please choose a house type.")
    if amenity == "Select Amenity":
        errors.append("Please choose an amenity.")
    if bedrooms is None:
        errors.append("Please provide bedrooms.")
    if bathrooms is None:
        errors.append("Please provide bathrooms.")

    if errors:
        for e in errors:
            st.warning(e)
    else:
        try:
            row = pd.DataFrame([[
                district_map[district],
                house_type_map[house_type],
                int(bedrooms),
                int(bathrooms),
                amenity_map[amenity]
            ]], columns=["district_code", "house_type_code", "bedrooms", "bathrooms", "amenity_code"])

            pred = model.predict(row)[0]
            st.success(f"Estimated Monthly Rent: **{pred:,.0f} RWF**")

            # ---- Show comparison chart ONLY after prediction
            st.markdown("<div class='block'>", unsafe_allow_html=True)
            st.subheader("Average Rent by District (Example)")
            comp_df = pd.DataFrame({
                "District": ["Gasabo", "Kicukiro", "Nyarugenge"],
                "Average Rent (RWF)": [450000, 400000, 500000]
            }).set_index("District")
            st.bar_chart(comp_df)
            st.markdown("</div>", unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Prediction error: {e}")

# Footer
st.markdown("<p class='note'>Built for the Rwanda AI & ML Hackathon — RentBot by Ibrazzi.</p>", unsafe_allow_html=True)
