
import joblib
from sklearn.linear_model import LinearRegression
import numpy as np

# Dummy training data for rent prediction
# Format: [bedrooms, bathrooms, has_balcony]
X = np.array([[1, 1, 1], [2, 1, 1], [2, 2, 1], [3, 2, 0]])
y = np.array([200000, 300000, 350000, 400000])

# Train a simple Linear Regression model
model = LinearRegression()
model.fit(X, y)

# Save the model to rent_model.pkl
joblib.dump(model, "rent_model.pkl")
print("✅ Dummy model saved as rent_model.pkl")
