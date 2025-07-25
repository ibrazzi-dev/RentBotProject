import requests

url = "http://127.0.0.1:5000/predict"
payload = {
    "District": "Gasabo",
    "HouseType": "Studio",
    "Bedrooms": 1,
    "Bathrooms": 1,
    "Amenity": "Balcony"
}

print("🔍 Sending request to:", url)
print("📦 Payload:", payload)

try:
    response = requests.post(url, json=payload)
    print("✅ Status Code:", response.status_code)
    print("🔍 Response Text:", response.text)
except Exception as e:
    print("❌ Error sending request:", e)
