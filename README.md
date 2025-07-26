#  RentBot – Smart Rent Price Prediction

RentBot is a **Streamlit-powered AI web app** that predicts rental prices based on property features such as location, size, and number of rooms.  
It was built for the **Hackathon Challenge** to showcase **AI + Real Estate** potential for Rwanda.

---

## ** Problem Statement**
Finding affordable and fair rental prices in Kigali and other districts is a major challenge for both tenants and property owners.  
RentBot uses machine learning to **predict rental prices** based on historical data, providing quick insights and transparency.

---

## ** Dataset Overview**
We use a **sample dataset (`sample_houses.csv`)** with 10+ entries containing:
- **District** (Nyarugenge, Gasabo, Kicukiro)
- **Bedrooms & Bathrooms**
- **House Size (m²)**
- **Base Rent Price (Frw)**

The dataset is used to train a **Linear Regression model** saved as `rent_model.pkl`.  
Encoders for district mapping are stored in `mappings.pkl`.

---

## ** Features of RentBot**
- **Predict Rental Prices** instantly.
- **Interactive Streamlit UI** with input sliders & select boxes.
- **Data Visualizations** (Price trends).
- **Simple ML Pipeline** (Scikit-learn + Joblib).
- **Hackathon-ready presentation** with screenshots.

---

## ** How to Run Locally**
1. **Clone this repo**:
   ```bash
   git clone https://github.com/ibrazzi-dev/RentBotProject.git
   cd RentBotProject
