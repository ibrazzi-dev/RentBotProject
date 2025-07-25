# 🏠 RentBot – Your AI-powered Rent Prediction Assistant

RentBot is an AI-powered web application designed to predict rental prices for properties in Kigali, Rwanda. Inspired by platforms like Zillow, it leverages machine learning to provide **smart, data-driven rent estimates** based on district, property type, and amenities.

---

## 🚀 Problem Statement

Finding accurate rental prices in Rwanda is challenging due to a lack of centralized housing data. Many tenants overpay because they rely on brokers or guesswork.

**RentBot solves this by:**

- Predicting **fair rental prices** using ML.
- Providing a **simple Streamlit web interface**.
- Comparing **rent across districts** for better decision-making.

---

## 📊 Data Summary

- **Dataset:** Synthetic & curated sample data from Kigali districts.
- **Target Variable:** Rent price (RWF).
- **Features Used:**
  - `district` (Gasabo, Kicukiro, Nyarugenge)
  - `house_type` (Apartment, Studio, Bungalow, etc.)
  - `bedrooms`, `bathrooms`
  - `amenities` (Balcony, Parking, Garden, etc.)
- **Preprocessing:** Label encoding, feature scaling, and simple feature engineering.
- **Model:** Linear Regression (exported to `rent_model.pkl` with `joblib`).

---

## ✨ Features

- **Hero Header & Modern UI** (Zillow-style).
- **Interactive Form** – Select district, property type, bedrooms, bathrooms, and amenities.
- **Instant AI Rent Prediction** – Returns price in RWF.
- **📊 Bar Chart Comparison** – Compare across Nyarugenge, Gasabo, and Kicukiro.
- **Lightweight model** – Easy to deploy and extend.

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit
- **Backend/ML:** Python, scikit-learn, pandas, numpy, joblib
- **Visualization:** Streamlit’s native `st.bar_chart`
- **Version Control:** Git + GitHub

---

## 💻 How to Run Locally

### 1) Clone the Repository

```bash
git clone https://github.com/ibrazzi-dev/RentBotProject.git
cd RentBotProject
