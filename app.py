from flask import Flask, jsonify
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/weather/<city>')
def get_weather(city):
    api_key = os.getenv('WEATHER_API_KEY')
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    
    try:
        response = requests.get(url)
        data = response.json()
        weather_data = {
            "city": city,
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"]
        }
        return jsonify(weather_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

@app.route('/version')
def version():
    return jsonify({"version": "1.0.1", "status": "running"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)