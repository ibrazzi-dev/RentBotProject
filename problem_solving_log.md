# 🛠 Problem-Solving Log – RentBot Hackathon

### **Day 1 – Setup**
- Created `RentBotProject` structure.
- Built `train_dummy_model.py` for quick ML model creation.
- Implemented Streamlit app (`app.py`) UI.

### **Day 2 – Data & Model**
- Collected and cleaned **sample_houses.csv** (10+ properties).
- Encoded categorical features (district, house_type, amenities).
- Saved model and mappings as `.pkl`.

### **Day 3 – Debugging**
- Fixed `ValueError: could not convert string to float`.
- Added district encoding and amenity mapping.
- Resolved scikit-learn installation issues (Python 3.11 switch).

### **Day 4 – UI Improvements**
- Added prediction form (district, house type, etc.).
- Added placeholder bar chart for average rent by district.
- Improved layout with cleaner design.

### **Day 5 – Documentation**
- Finalized `README.md`, `requirements.txt`.
- Added `responsible_ai.md` and this problem-solving log.
- Tested full workflow: `streamlit run app.py` → works!

---

**Remaining Next Steps (Post-Hackathon):**
- Add background image & advanced CSS themes.
- Train on **real Kigali rent dataset** for accurate predictions.
- Deploy app (Streamlit Cloud / Heroku).
