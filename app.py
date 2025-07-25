import streamlit as st
import joblib
import numpy as np
import pandas as pd

# ======================
# Load Model (dummy or your own)
# ======================
@st.cache_resource
def load_model():
    # Uses your dummy/regression model trained via train_dummy_model.py
    return joblib.load("rent_model.pkl")

model = load_model()

# ======================
# Page config
# ======================
st.set_page_config(page_title="RentBot - AI Rent Prediction", page_icon="🏠", layout="centered")

# ======================
# Global CSS (background + styling)
# ======================
st.markdown(
    """
    <style>
        /* Faded city image background */
        .stApp::before {
            content: "";
            background-image: url('https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?q=80&w=2070&auto=format&fit=crop');
            background-size: cover;
            background-position: center center;
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            opacity: 0.15;   /* fade it */
            z-index: -1;
        }

        /* Hero section */
        .hero {
            text-align: center;
            padding: 2rem 1rem;
            background: linear-gradient(135deg, rgba(74,144,226,0.95), rgba(20,92,164,0.95));
            color: #fff;
            border-radius: 14px;
            margin-bottom: 1.5rem;
            box-shadow: 0 10px 24px rgba(0,0,0,0.1);
        }
        .hero h1 {
            font-size: 2.6rem;
            margin: 0 0 .4rem 0;
        }
        .hero p {
            font-size: 1.1rem;
            margin: 0.3rem 0;
            opacity: 0.95;
        }

        /* Buttons */
        .stButton>button {
            background-color: #007BFF !important;
            color: #FFFFFF !important;
            border-radius: 8px !important;
            padding: 0.6rem 1.2rem !important;
            font-weight: 600 !important;
            border: none !important;
        }
        .stButton>button:hover {
            background-color: #0056b3 !important;
        }

        /* Cards */
        .prediction-card {
            background: rgba(255,255,255,0.95);
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 0 15px rgba(0,0,0,0.08);
            text-align: center;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# ======================
# Hero Header
# ======================
st.markdown(
    """
    <div class="hero">
        <img src="https://cdn-icons-png.flaticon.com/512/25/25694.png" width="85" alt="RentBot logo" />
        <h1>RentBot</h1>
        <p>Your AI-powered assistant for smarter rent predictions in Rwanda.</p>
        <p>Fill in the property details below to get an instant estimate.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# ======================
# Input Form
# ======================
st.header("Property Details")

col1, col2 = st.columns(2)
with col1:
    district = st.selectbox("Select District:", ["Nyarugenge", "Gasabo", "Kicukiro"])
    bedrooms = st.number_input("Number of Bedrooms:", min_value=1, max_value=10, value=2)
with col2:
    house_type = st.selectbox("House Type:", ["Apartment", "House", "Studio"])
    bathrooms = st.number_input("Number of Bathrooms:", min_value=1, max_value=5, value=1)

amenities = st.multiselect(
    "Amenities:",
    ["Balcony", "Parking", "Garden", "Swimming Pool", "Security"]
)

# ======================
# Predict
# ======================
if st.button("🔮 Predict Rent"):
    # build a simple feature representation for the dummy model:
    # [bedrooms, bathrooms, number_of_amenities]
    features = np.array([[bedrooms, bathrooms, len(amenities)]])
    base_rent = model.predict(features)[0]

    # district adjustment factors (example logic)
    district_factor = {"Nyarugenge": 1.20, "Gasabo": 1.10, "Kicukiro": 1.00}
    final_rent = int(base_rent * district_factor[district])

    st.markdown(
        f"""
        <div class="prediction-card">
            <h3>💰 Predicted Monthly Rent</h3>
            <h2 style="color:#007BFF;">{final_rent:,} RWF</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ======================
    # Comparison Bar Chart
    # ======================
    st.subheader("Comparison across districts")
    comp_df = pd.DataFrame({
        "District": ["Nyarugenge", "Gasabo", "Kicukiro"],
        "Predicted Rent (RWF)": [
            int(base_rent * district_factor["Nyarugenge"]),
            int(base_rent * district_factor["Gasabo"]),
            int(base_rent * district_factor["Kicukiro"]),
        ],
    }).set_index("District")

    st.bar_chart(comp_df)

# ======================
# Footer
# ======================
st.markdown("---")
st.markdown("**RentBot © 2025** • Built by IBRAZZI for the Rwanda Gov & IHS Towers Hackathon 💡")
