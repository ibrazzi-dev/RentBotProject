# RentBotProject 🏠

AI-powered rental price predictor and dashboard built with **Streamlit** and **Scikit-learn**.  
This project was developed for a hackathon challenge to help Rwandans easily predict fair rental prices and compare options.

---

## **Problem Statement**
Finding affordable and fair rental housing in Kigali is challenging due to price variations and lack of transparency. **RentBot** predicts house rental prices based on location, house type, amenities, and other features, giving users an easy way to compare costs.

---

## **Data Summary**
- **Dataset:** `rent_data_csv.csv`
- **Features:**
  - District (e.g., Gasabo, Nyarugenge)
  - House Type (e.g., Apartment, Bungalow)
  - Bedrooms, Bathrooms
  - Amenities (e.g., Garden, Parking)
  - Price (target variable)
- Data cleaned, encoded, and normalized using **scikit-learn** pipelines.

---

## **Key Features**
- **Hero Section** with logo and tagline.
- **Interactive Form** (District, House Type, Bedrooms, Bathrooms, Amenities).
- **AI Price Prediction** using a trained regression model (`rent_model.pkl`).
- **Bar Chart Comparison** of predicted price vs average market price (via `st.bar_chart`).
- **Clean UI** with a faded Kigali city background image.
- **Hackathon Ready** – Fast, user-friendly, and impactful.

---

## **How to Run**

### **1. Clone the repo**
```bash
git clone https://github.com/ibrazzi-dev/RentBotProject.git
cd RentBotProject
