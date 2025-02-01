from flask import Flask, render_template, request
import joblib
import requests

app = Flask(__name__)

# Load the trained model
MODEL_PATH = 'weather_model.pkl'
model = joblib.load(MODEL_PATH)

# OpenWeatherMap API configuration
API_KEY = 'Enter your API Key'  # Replace with your actual API key
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'
FORECAST_URL = 'https://api.openweathermap.org/data/2.5/forecast'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        city = request.form['city']  # Get city from user input

        # Fetch current weather data
        weather_data = get_current_weather(city)
        if 'error' in weather_data:
            return render_template('result.html', error=weather_data['error'])

        # Prepare data for prediction
        temperature = weather_data['temperature']
        humidity = weather_data['humidity']

        # Make a prediction using the trained model
        prediction = model.predict([[temperature, humidity]])[0]

        # Fetch weather forecast for the next day
        forecast_data = get_weather_forecast(city)

        return render_template('result.html', prediction=prediction, weather_data=weather_data, forecast_data=forecast_data)

def get_current_weather(city):
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        return {
            'temperature': data['main']['temp'],
            'weather': data['weather'][0]['description'],
            'humidity': data['main']['humidity']
        }
    else:
        return {'error': f"Error: {response.status_code} - {response.text}"}

def get_weather_forecast(city):
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'
    }

    response = requests.get(FORECAST_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        # Extract forecast for the next day (24 hours later)
        forecast_list = [entry for entry in data['list'] if '12:00:00' in entry['dt_txt']]
        if len(forecast_list) > 0:
            next_day_forecast = forecast_list[0]
            return {
                'temperature': next_day_forecast['main']['temp'],
                'weather': next_day_forecast['weather'][0]['description']
            }
        else:
            return {'error': 'No forecast data available for the next day'}
    else:
        return {'error': f"Error: {response.status_code} - {response.text}"}

if __name__ == "__main__":
    app.run(debug=True)
