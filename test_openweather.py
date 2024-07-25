import requests

# Replace with your actual API key
API_KEY = 'YOUR_API_KEY'
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'
CITY = 'London'  # Replace with the city you want to check

# Parameters for the API request
params = {
    'q': CITY,
    'appid': API_KEY,
    'units': 'metric'  # or 'imperial' for Fahrenheit
}

# Make the API request
response = requests.get(BASE_URL, params=params)

# Check if the request was successful
if response.status_code == 200:
    print('Request successful')
    data = response.json()
    print('Weather data:', data)
else:
    print('Request failed')
    print('Status code:', response.status_code)
    print('Response:', response.text)
