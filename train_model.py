import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import joblib

# Load your dataset
data = pd.read_csv('weather_data.csv')

# Prepare your features (X) and target (y)
X = data[['temperature', 'humidity']]  # Features
y = data['target']  # Target variable

# Split the dataset into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# Initialize and train the model
model = LinearRegression()
model.fit(X_train, y_train)

# Save the model to a file
MODEL_PATH = 'weather_model.pkl'
joblib.dump(model, MODEL_PATH)

print(f"Model saved to {MODEL_PATH}")
