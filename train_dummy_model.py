# train_dummy_model.py
import pandas as pd
import joblib
from sklearn.linear_model import LinearRegression

# ---- Synthetic fallback dataset ----
data = [
    ["Nyarugenge", "Apartment", 2, 1, "Balcony", 300000],
    ["Gasabo", "Bungalow", 3, 2, "Parking", 450000],
    ["Kicukiro", "Studio", 1, 1, "Wi-Fi", 200000],
    ["Gasabo", "Apartment", 2, 2, "Garden", 400000],
    ["Nyarugenge", "Villa", 4, 3, "Parking", 800000],
]

df = pd.DataFrame(data, columns=["district", "house_type", "bedrooms", "bathrooms", "amenity", "price"])

print("📊 Data Loaded!")
print(df.head())

# ---- Create simple mappings ----
districts = sorted(df["district"].unique())
house_types = sorted(df["house_type"].unique())
amenities = sorted(df["amenity"].unique())

district_map = {d: i for i, d in enumerate(districts)}
house_type_map = {h: i for i, h in enumerate(house_types)}
amenity_map = {a: i for i, a in enumerate(amenities)}

mappings = {
    "district": district_map,
    "house_type": house_type_map,
    "amenity": amenity_map
}

# ---- Encode ----
df["district_code"] = df["district"].map(district_map)
df["house_type_code"] = df["house_type"].map(house_type_map)
df["amenity_code"] = df["amenity"].map(amenity_map)

X = df[["district_code", "house_type_code", "bedrooms", "bathrooms", "amenity_code"]]
y = df["price"]

# ---- Train Model ----
model = LinearRegression()
model.fit(X, y)

# ---- Save Model and Mappings ----
joblib.dump(model, "rent_model.pkl")
joblib.dump(mappings, "mappings.pkl")

print("✅ Model saved as rent_model.pkl")
print("✅ Mappings saved as mappings.pkl")
