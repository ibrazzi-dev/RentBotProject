import streamlit as st
import joblib
import pandas as pd

# --- PAGE CONFIG ---
st.set_page_config(page_title="RentBot - Smart Rent Predictor", layout="wide")

# --- CUSTOM CSS for background ---
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://images.unsplash.com/photo-1508057198894-247b23fe5ade?ixlib=rb-4.0.3&auto=format&fit=crop&w=1740&q=80");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}
[data-testid="stHeader"] {
    background-color: rgba(0,0,0,0);
}
.hero {
    background: rgba(0, 0, 0, 0.6);
    padding: 30px;
    border-radius: 12px;
    text-align: center;
    color: white;
    margin-bottom: 20px;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# --- HERO SECTION ---
st.markdown(
    """
    <div class='hero'>
        <h1>🏠 RentBot</h1>
        <h3>Smart AI-Powered Rent Price Predictor for Kigali</h3>
    </div>
    """,
    unsafe_allow_html=True
)

# --- Load Model ---
model = joblib.load("rent_model.pkl")

# --- FORM ---
st.subheader("🔍 Predict Rent Price")
district = st.selectbox("Select District", ["Gasabo", "Kicukiro", "Nyarugenge"])
house_type = st.selectbox("House Type", ["Apartment", "Bungalow", "Villa"])
bedrooms = st.slider("Number of Bedrooms", 1, 10, 3)
bathrooms = st.slider("Number of Bathrooms", 1, 5, 2)
amenities = st.multiselect("Amenities", ["Parking", "Garden", "Wi-Fi", "Security"])

if st.button("Predict"):
    features = pd.DataFrame([[district, house_type, bedrooms, bathrooms, len(amenities)]],
                            columns=["district", "house_type", "bedrooms", "bathrooms", "amenities"])
    prediction = model.predict(features)[0]
    st.success(f"Estimated Rent Price: **{prediction:,.0f} RWF**")

# --- RENT PRICE COMPARISON ---
st.subheader("📊 Rent Comparison by District")
rent_data = pd.DataFrame({
    "District": ["Gasabo", "Kicukiro", "Nyarugenge"],
    "Average Rent": [450000, 400000, 500000]
})
st.bar_chart(rent_data.set_index("District"))
