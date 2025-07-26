import streamlit as st
import pandas as pd
import joblib

# =========================
# Load Model and Mappings
# =========================
try:
    model = joblib.load("rent_model.pkl")
    mappings = joblib.load("mappings.pkl")
    st.session_state["model_loaded"] = True
except Exception as e:
    st.error(f"❌ Could not load model/mappings: {e}")
    st.stop()

# =========================
# Custom Page Config
# =========================
st.set_page_config(page_title="RentBot - Kigali Rent Prediction", layout="wide")

# =========================
# CSS for Background & Styling
# =========================
st.markdown("""
<style>
body {
    background: url('bg.jpg') no-repeat center center fixed;
    background-size: cover;
}
.block-container {
    padding-top: 1rem;
}
.form-container {
    background: rgba(255, 255, 255, 0.9);
    padding: 20px 22px;
    border-radius: 12px;
    box-shadow: 0 1px 2px rgba(0,0,0,.08);
    margin-bottom: 18px;
}
h1, h2, h3 {
    margin-top: 0.2rem;
}
</style>
""", unsafe_allow_html=True)

# =========================
# App Header
# =========================
st.title("🏠 RentBot")
st.write("AI-powered rent prediction for **Kigali (Gasabo, Kicukiro, Nyarugenge)**.")

# =========================
# Property Form
# =========================
st.markdown("### 🔍 Enter property details")

district = st.selectbox("District", ["--Select--"] + list(mappings["district"].keys()))
house_type = st.selectbox("House Type", ["--Select--"] + list(mappings["house_type"].keys()))
bedrooms = st.number_input("Bedrooms", min_value=0, max_value=10, step=1)
bathrooms = st.number_input("Bathrooms", min_value=0, max_value=10, step=1)
main_amenity = st.selectbox("Main Amenity", ["--Select--"] + list(mappings["main_amenity"].keys()))

# =========================
# Prediction Button
# =========================
if st.button("Predict Rent"):
    if district == "--Select--" or house_type == "--Select--" or main_amenity == "--Select--":
        st.warning("Please fill all fields before predicting.")
    else:
        features = [[
            mappings["district"][district],
            mappings["house_type"][house_type],
            bedrooms,
            bathrooms,
            mappings["main_amenity"][main_amenity]
        ]]
        prediction = model.predict(features)[0]
        st.success(f"💰 Estimated Rent: **{int(prediction)} RWF**")

# =========================
# Chart (Optional, Only on Click)
# =========================
if st.checkbox("Show Example: Average Rent by District"):
    chart_data = pd.DataFrame({
        'District': list(mappings["district"].keys()),
        'Avg Rent': [300000, 400000, 350000]
    })
    st.bar_chart(chart_data.set_index("District"))
    
# Footer
st.markdown("<p class='note'>Built for the Rwanda AI & ML Hackathon — RentBot by Ibrazzi.</p>", unsafe_allow_html=True)
