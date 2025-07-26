import pandas as pd
import joblib
from sklearn.linear_model import LinearRegression

df = pd.read_csv("sample_houses.csv")

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
df["district_code"] = df["district"].map(district_map)
df["house_type_code"] = df["house_type"].map(house_type_map)
df["amenity_code"] = df["amenity"].map(amenity_map)

X = df[["district_code", "house_type_code", "bedrooms", "bathrooms", "amenity_code"]]
y = df["price"]

model = LinearRegression()
model.fit(X, y)

joblib.dump(model, "rent_model.pkl")
joblib.dump(mappings, "mappings.pkl")

print("✅ rent_model.pkl & mappings.pkl saved")
