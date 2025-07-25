import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="RentBot", layout="wide")

# --- Styling (background hero) ---
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://images.unsplash.com/photo-1508057198894-247b23fe5ade?ixlib=rb-4.0.3&auto=format&fit=crop&w=1740&q=80");
    background-size: cover;
}
.hero {
    background: rgba(0,0,0,0.6);
    padding: 24px 32px;
    border-radius: 12px;
    color: white;
    margin-bottom: 24px;
    text-align: center;
}
.block {
    background: rgba(255,255,255,0.9);
    padding: 20px;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>🏠 RentBot</h1>
    <h3>AI-powered rent prediction for Kigali</h3>
    <p>Enter your property details and get a fair rent estimate instantly.</p>
</div>
""", unsafe_allow_html=True)

# --- Load model + mappings ---
try:
    model = joblib.load("rent_model.pkl")
    mappings = joblib.load("mappings.pkl")
    st.success("✅ Model & mappings loaded")
except Exception as e:
    st.error(f"❌ Could not load model/mappings: {e}")
    st.stop()

district_map = mappings["district"]
house_type_map = mappings["house_type"]
amenity_map = mappings["amenity"]

# --- Reverse maps (for selectboxes) ---
districts = list(district_map.keys())
house_types = list(house_type_map.keys())
amenities_list = list(amenity_map.keys())

# --- Form ---
st.markdown("<div class='block'>", unsafe_allow_html=True)
st.subheader("🔍 Predict Rent")

col1, col2 = st.columns(2)

with col1:
    district = st.selectbox("District", districts)
    house_type = st.selectbox("House Type", house_types)

with col2:
    bedrooms = st.number_input("Bedrooms", min_value=1, max_value=10, value=2, step=1)
    bathrooms = st.number_input("Bathrooms", min_value=1, max_value=5, value=1, step=1)

amenities_selected = st.multiselect("Amenities", amenities_list)

if st.button("💡 Predict"):
    try:
        district_code = district_map[district]
        house_type_code = house_type_map[house_type]

        # For now just count amenities, or you can encode the first selected one
        amenity_code = amenity_map[amenities_selected[0]] if amenities_selected else 0

        X = pd.DataFrame([[
            district_code,
            house_type_code,
            int(bedrooms),
            int(bathrooms),
            int(amenity_code)
        ]], columns=["district_code", "house_type_code", "bedrooms", "bathrooms", "amenity_code"])

        y_pred = model.predict(X)[0]
        st.success(f"🎯 Estimated Rent: **{y_pred:,.0f} RWF**")
    except Exception as e:
        st.error(f"Prediction error: {e}")

st.markdown("</div>", unsafe_allow_html=True)

# --- Comparison chart (dummy values to display something nice) ---
st.subheader("📊 Rent Comparison by District (example)")
comparison_df = pd.DataFrame({
    "District": ["Nyarugenge", "Gasabo", "Kicukiro"],
    "Average Rent (RWF)": [500000, 450000, 400000]
}).set_index("District")
st.bar_chart(comparison_df)
